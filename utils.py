import boto3
from boto3.dynamodb.conditions import Key, Attr

localdynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
DYNAMODB_TABLE_NAME = "Polls"

# Returns true if the given poll id exists
def checkIfPollIdIsValid(pollId):
    pollsdb = localdynamodb.Table(DYNAMODB_TABLE_NAME)
    dbresponse = pollsdb.query(
        IndexName="QueryIndex",
        KeyConditionExpression=Key("SK").eq("POLL#{}".format(str(pollId))) & Key("PK").begins_with("AUTHOR#")
    )
    return dbresponse["Count"] > 0