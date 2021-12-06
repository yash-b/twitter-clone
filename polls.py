import boto3
import hug
from boto3.dynamodb.conditions import Key, Attr
import time
import requests

#Constants
TABLE_NAME = "Polls"

db = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

@hug.startup()
def onStart(api):
    requests.post("http://localhost:5300/addservice", data={"serviceName":"polls", "urls":"http://localhost:5200", "healthcheckPath":"/results/1"})

@hug.authentication.basic
def checkUserAuthorization(username, password):
    r = requests.get("http://localhost:5400/verify/", data={"username":str(username),"password":str(password)})
    print(r.text)
    if "true" in r.text:
        return True
    else:
        return False

@hug.directive()
def pollsdb(**kwargs):
    table = db.Table(TABLE_NAME)
    return table
    
# Vote on a poll
@hug.post("/vote", requires=checkUserAuthorization)
def vote(response, pollId: hug.types.number, voteOption: hug.types.text, username: hug.types.text, hug_pollsdb):
    try:
        hug_pollsdb.put_item(
            Item = {
                "PK":"USER#{}".format(username),
                "SK":"POLL#{}".format(pollId),
                "Username":str(username),
                "VoteOption":str(voteOption)
            },
            ConditionExpression="attribute_not_exists(PK) AND attribute_not_exists(SK)"
        )
    except Exception as e:
        response.status = hug.falcon.HTTP_204
        return {"success":"false", "message":"You have already voted in the poll"}
    dbresponse = None
    try:
        dbresponse = hug_pollsdb.get_item(
            Key = {
                "PK":"OPTION#{}".format(voteOption),
                "SK":"POLL#{}".format(pollId)
            }
        )
    except Exception as e:
        pass
    try:
        if len(dbresponse)==0 or dbresponse==None or not "Item" in dbresponse:
            hug_pollsdb.put_item(
                Item={
                    "PK":"OPTION#{}".format(voteOption),
                    "SK":"POLL#{}".format(pollId),
                    "TotalCount":1
                }
            )
            response.status = hug.falcon.HTTP_201
            return {"success":"true", "message":"created"}
        else:
            vc = dbresponse["Item"]
            currentVoteCount = vc["TotalCount"] + 1
            hug_pollsdb.update_item(
                Key = {
                    "PK":"OPTION#{}".format(voteOption),
                    "SK":"POLL#{}".format(pollId)
                },
                UpdateExpression="set TotalCount = :t",
                ExpressionAttributeValues={
                    ":t": currentVoteCount
                },
                ReturnValues="UPDATED_NEW"
            )
            response.status = hug.falcon.HTTP_201
            return {"success": "true"}
    except Exception as e:
        response.status = hug.falcon.HTTP_204
        return {"success":"false"}

# Create a poll
@hug.post("/create/poll", requires=checkUserAuthorization)
def createPOLL(response, username: hug.types.text, question: hug.types.text, options: hug.types.delimited_list(","), pollId: hug.types.number, hug_pollsdb):
    if len(options) > 4:
        return {"success":"false","message":"Options limit exceeded"}
    try:
        listDict = []
        for option in options:
            listDict.append({"option":str(option)})
        databaseResponse = hug_pollsdb.put_item(
            Item={
                "PK":"AUTHOR#{}".format(username),
                "SK":"POLL#{}".format(pollId),
                "Question":str(question),
                "Options":listDict
            }
        )
        response.status = hug.falcon.HTTP_201
        return {"success": "true"}
    except Exception as e:
        response.status = hug.falcon.HTTP_204
        return {"success": "false", "message":str(e)}

# Get poll results
@hug.get("/results/{pollId}")
def viewPOLLResults(response, pollId: hug.types.number, hug_pollsdb):
    table = hug_pollsdb
    while True:
        if not table.global_secondary_indexes or table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
            print('Waiting for index to backfill...')
            time.sleep(5)
            table.reload()
        else:
            break
    dbresponse = hug_pollsdb.query(
        IndexName="QueryIndex",
        KeyConditionExpression=Key("SK").eq("POLL#{}".format(pollId)) & Key("PK").begins_with("AUTHOR#")
    )
    returnResponse = {}
    optionsList = []
    for option in dbresponse["Items"][0]["Options"]:
        loopDict = {}
        optionString = option["option"]
        loopDict["option"] = optionString
        try:
            optionQuery = hug_pollsdb.query(
                IndexName="QueryIndex",
                KeyConditionExpression=Key("SK").eq("POLL#{}".format(pollId)) & Key("PK").eq("OPTION#{}".format(optionString))
            )
            if "Items" in optionQuery:
                loopDict["totalCount"] = str(optionQuery["Items"][0]["TotalCount"])
        except Exception as e:
            loopDict["totalCount"] = str(0)
        optionsList.append(loopDict)
    returnResponse["Options"] = optionsList
    returnResponse["Question"] = str(dbresponse["Items"][0]["Question"])
    return returnResponse
            
        
    

