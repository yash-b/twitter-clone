import greenstalk
import configparser
import logging.config
from typing import NamedTuple
import hug
import redis
import json


# Load configuration
#
config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers=False)
r = redis.Redis(host='localhost', port=6379, db=0,decode_responses=True)


#Get Popular posts
@hug.get("/likes/popular") 
def popularLikes(response):
    topPost = r.zrange("postlikes",0,4, desc=True,withscores=True)
    posts =[]
    for post in topPost:
        posts.append({"postid": post[0].decode(), "likes": post[1] })
    # print(topPost, "=============")
    return {"data": posts}

#Like a post
@hug.post("/like",status=hug.falcon.HTTP_201) 
def likepost(response, username, postid):
    exists = r.sismember("user"+username, postid)
    if exists: #its True
        return {"message": "User has already liked the post"}
    else:
        r.sadd("user"+username, postid)
        rank=r.zrank("postlikes", postid)
        if(rank!=None):
            rank = int(rank) + 1
        else:
            rank = 1
        r.zadd("postlikes", {postid: rank} )

    return {"message": "Post liked successfully"}

#Liking a post async
@hug.post("/likeasync", status=hug.falcon.HTTP_202)
def likePostAsync(response, username, postid):
    try:
        with greenstalk.Client(("127.0.0.1", 11300)) as client:
            likesDict = {"username":str(username), "postid": str(postid), "beanstalk_consumer_type":"likes"}
            client.put(json.dumps(likesDict))
    except Exception as e:
            response.status = hug.falcon.HHTP_409
            return {"error":str(e)}
    response.status = hug.falcon.HTTP_202


#Get posts liked by a user
@hug.get("/likes/{username}") 
def popularLikes(response,username):
   
    posts = r.smembers("user"+username)
    postsnew = []
    for post in posts:
        # print(post,"=======")
        postsnew.append(post)
    return {"data": postsnew}