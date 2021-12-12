import configparser
import greenstalk
import json
import logging.config
import sqlite_utils
import time
import traceback
import boto3
from boto3.dynamodb.conditions import Key, Attr
from utils import checkIfPollIdIsValid

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

def handle_post(job):
    dbfile = config["sqlite"]["postsdb"]
    db = sqlite_utils.Database(dbfile)
    return createPost(job, db)

def notifyUser(useremail: str):
    print("Notifying...")
    try:
        with greenstalk.Client(('127.0.0.1', 11400)) as client:
            messageDict = {"sender":"noreply-project4@gmail.com", "receiver":useremail, "message":"Invalid poll id"}
            client.put(json.dumps(messageDict))
    except Exception as e:
        print("Error notifying user")

def process_jobs():
    print ("Starting beanstalk consumer")
    while True:
        time.sleep(1)
        with greenstalk.Client(('127.0.0.1', 11300)) as client:
            while True:
                job_obj = client.reserve() # blocks indefinitely and waits for a job
                try:
                    job = json.loads(job_obj.body)
                    job_type = job["beanstalk_consumer_type"]
                    del job["beanstalk_consumer_type"]
                    if job_type == "post":
                        handle_post(job)
                    elif job_type == "polls":
                        urlLink = job["url"]
                        pollId = urlLink.split("/")[4]
                        pollValid = checkIfPollIdIsValid(pollId)
                        if not pollValid:
                            notifyUser(job["useremail"])
                    else:
                        print ("Unknown job type found: " + job_type)

                    print ("Done with job type: " + job_type)
                    # Let's just complete the job always, the alternative is to do a max # of retries
                    client.delete(job_obj)
                except Exception as e:
                    client.delete(job_obj)
                    print ("beanstalk consumer saw an exception:")
                    print (e)
                    print(traceback.format_exc())


if __name__ == '__main__':
    process_jobs()