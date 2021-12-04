# CPSC 449 - Project 2
# Twitter clone - backend
# Contributers: Sijan Rijal, Hanyue Zheng, Yash Bhambhani

import configparser
import logging.config
import hug
import sqlite_utils
import requests
import datetime

#Load configuration
config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers= False)

@hug.startup()
def onStart(api):
    requests.post("http://localhost:5300/addservice", data={"servicename":"polls", "urls":"http://localhost:5100, http://localhost:5101, http://localhost:5102", "healthcheckPath":"/timeline/public"})

@hug.directive()
def postsdb(section="sqlite", key="postsdb", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.authentication.basic
def checkUserAuthorization(username, password):
    r = requests.get("http://localhost:5000/verify/", data={"username":str(username),"password":str(password)})
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

@hug.post("/create/post", requires=checkUserAuthorization)
def createPost(request, username: hug.types.text, post_text: hug.types.text, hug_postsdb, response, **kwargs):
    db = hug_postsdb["posts"]
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
    try:
        db.insert(post)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error":str(e)}
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