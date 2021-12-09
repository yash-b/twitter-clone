import configparser
import greenstalk
import json
import logging.config
import sqlite_utils
import time
import traceback
import boto3
from boto3.dynamodb.conditions import Key, Attr
from polls import pollsdb

config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers= False)

localdynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
DYNAMODB_TABLE_NAME = "Polls"

def createPost(post_info, db):
    try:
        db["posts"].insert(post_info)
    except Exception as e:
        print("DB Insert error: ")
        print(e)
        return False
    return True

# Should return True if job is complete and should be deleted from beanstalk queue.
def handle_post(job):
    dbfile = config["sqlite"]["postsdb"]
    db = sqlite_utils.Database(dbfile)
    return createPost(job, db)

# Returns true if the given poll id exists
def checkIfPollIdIsValid(pollId):
    pollsdb = localdynamodb.Table(DYNAMODB_TABLE_NAME)
    dbresponse = pollsdb.query(
        IndexName="QueryIndex",
        KeyConditionExpression=Key("SK").eq("POLL#{}".format(pollId)) & Key("PK").begins_with("AUTHOR#")
    )
    if dbresponse["Count"] > 0:
        return True
    else:
        return False

def process_jobs():
    print ("Starting beanstalk consumer")
    while (True):
        # Wrap the client getter in a try/catch so that in the case
        # of exceptions we can recreate the client and continue working.
        try:
            # sleep in case of being stuck in an error loop.
            time.sleep(1)
            with greenstalk.Client(('127.0.0.1', 11300)) as client:
                while True:
                    job_obj = client.reserve() # blocks indefinitely and waits for a job
                    
                    job = json.loads(job_obj.body)
                    job_type = job["beanstalk_consumer_type"]
                    del job["beanstalk_consumer_type"]

                    res = False
                    if job_type == "post":
                        res = handle_post(job)
                    elif job_type == "polls":
                        urlLink = job["url"]
                        pollId = urlLink.split("/")[2]
                        checkIfPollIdIsValid()
                    else:
                        print ("Unknown job type found: " + job_type)
                        client.delete(job_obj)
                    if res:
                        print ("Completed job type: " + job_type)
                        client.delete(job_obj)
            
        except Exception as e:
            print ("beanstalk consumer saw an exception:")
            print (e)
            print(traceback.format_exc())


if __name__ == '__main__':
    process_jobs()