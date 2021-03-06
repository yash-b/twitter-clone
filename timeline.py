# CPSC 449 - Project 2
# Twitter clone - backend
# Contributers: Sijan Rijal, Hanyue Zheng, Yash Bhambhani

import configparser
import greenstalk
import json
import logging.config
import hug
import smtplib
import sqlite_utils
import requests
import datetime
import re

from utils import checkIfPollIdIsValid

#Load configuration
config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers= False)

def isLinkForPollOrLike(urlString):
    if len(urlString) > 0:
        #check if it's the link to a poll service
        if "/results" in urlString:
            return "polls"
        else:
            return "likes"
    else:
        return ""

def getUrlFromPost(postText: str):
    urlLink = re.findall(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", postText)
    if len(urlLink) > 0:
        return urlLink[0]
    else:
        return ""

@hug.startup()
def onStart(api):
    requests.post("http://localhost:5300/addservice", data={"serviceName":"timeline", "urls":"http://localhost:5100,http://localhost:5101,http://localhost:5102", "healthcheckPath":"/timeline/public"})

@hug.directive()
def postsdb(section="sqlite", key="postsdb", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.authentication.basic
def checkUserAuthorization(username, password):
    r = requests.get("http://localhost:5400/verify/", data={"username":str(username),"password":str(password)})
    print(r.text)
    if "true" in r.text:
        return True
    else:
        return False

@hug.get("/timeline/home", requires=checkUserAuthorization)
def getHomeTimeline(username:hug.types.text, hug_postsdb):
    r = requests.get(f"http://localhost:5000/following/{username}")
    followingJSON = r.json()
    string = ""
    for following in followingJSON:
        string += "\"" + following["following"] + "\"" + " OR username="
    if len(string) > 0:
        queryString = "SELECT * FROM posts WHERE username=" + string.strip()[0:len(string)-13].strip() + " ORDER BY timestamp DESC"
        result = hug_postsdb.query(queryString)
        list = []
        for row in result:
            list.append(row)
        return list
    return []


@hug.get("/timeline/{username}", requires=checkUserAuthorization)
def getUserTimeline(username: hug.types.text, hug_postsdb):
    db = hug_postsdb
    result = db.query("SELECT * FROM posts WHERE username==\"{}\" ORDER BY timestamp DESC".format(str(username)))
    list = []
    for row in result:
        # print(row)
        list.append(row)
    return list

@hug.get("/timeline/public/")
def getPublicTimeline(hug_postsdb):
    result = hug_postsdb.query("SELECT * FROM posts ORDER BY timestamp DESC")
    list = []
    for row in result:
        list.append(row)
    # print(hug_postsdb["posts"].last_rowid)
    return list

def createPostDict(username, post_text, kwargs):
    date = datetime.datetime.now()
    timeStamp = str(date)[0:19]
    post = {
        "username": username,
        "post": post_text,
        "timestamp": timeStamp
    }
    try:
        post["repost"] = "/posts/{}".format(kwargs["repost"])
    except:
        ""
    return post

@hug.post("/create/post", requires=checkUserAuthorization)
def createPost(request, username: hug.types.text, useremail: hug.types.text, post_text: hug.types.text, hug_postsdb, response, **kwargs):
    db = hug_postsdb["posts"]
    post = createPostDict(username, post_text, kwargs)
    urlLink = getUrlFromPost(post_text)
    linkType = isLinkForPollOrLike(urlLink)
    try:
        db.insert(post)
        # Now do everything sync here without beanstalk.
        # Check if there is a poll, check if it exists, if not send email
        if linkType == "polls":
            pollId = urlLink.split("/")[4]
            if not checkIfPollIdIsValid(pollId):
                message = "Invalid poll id"
                senderEmail = "noreply-project4@gmail.com"
                msg = ("From: %s\r\nTo: %s\r\n\r\n"% (senderEmail, useremail)) + message
                server = smtplib.SMTP("localhost", 1026)
                server.set_debuglevel(1)
                server.sendmail(senderEmail, useremail, msg)
                server.quit()

    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error":str(e)}
    return {"status":"success"}

@hug.post("/create/post_async")
def createPostAsync(request, username: hug.types.text, useremail: hug.types.text, post_text: hug.types.text, response, **kwargs):
    post = createPostDict(username, post_text, kwargs)
    # type is used to pick which process function to use in beanstalk_consumer.py
    post["beanstalk_consumer_type"] = "post"
    urlLink = getUrlFromPost(post_text)
    linkType = isLinkForPollOrLike(urlLink)
    try:
        with greenstalk.Client(('127.0.0.1', 11300)) as client:
            client.put(json.dumps(post))
            if linkType == "polls":
                pollLinkDict = {"url": urlLink, "beanstalk_consumer_type":"polls", "useremail": useremail}
                client.put(json.dumps(pollLinkDict))
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error":str(e)}

    response.status = hug.falcon.HTTP_202
    return {"status":"success"}

@hug.get("/posts/{id}")
def getPost(response, id: hug.types.number, hug_postsdb):
    posts = []
    try:
        post = hug_postsdb["posts"].get(id)
        posts.append(post)
    except sqlite_utils.db.NotFoundError:
        response.status = hug.falcon.HTTP_404
    return {"post": posts}