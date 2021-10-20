import configparser
import logging.config

import hug
import sqlite_utils, sqlite3

#Load configuration
config = configparser.ConfigParser()
config.read("./etc/api.ini")
logging.config.fileConfig(config["logging"]["config"], disable_existing_loggers= False)

def query(db, sql, args=(), one=False):
    cur = db.execute(sql, args)
    rv = [dict((cur.description[idx][0], value)
          for idx, value in enumerate(row))
          for row in cur.fetchall()]
    cur.close()

    return (rv[0] if rv else None) if one else rv

@hug.directive()
def usersdb(section="sqlite", key="usersdb", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.directive()
def postsdb(section="sqlite", key="postsdb", **kwargs):
    dbfile = config[section][key]
    return sqlite_utils.Database(dbfile)

@hug.post("/signup/", status = hug.falcon.HTTP_201)
def createUser(
    response,
    username: hug.types.text,
    bio: hug.types.text,
    email: hug.types.text,
    password: hug.types.text,
    hug_usersdb
):
    users = hug_usersdb["users"]
    user = {
        "username": username,
        "bio": bio,
        "email": email,
        "password": password,
    }
    print('whatever!')
    print(users)
    print('after users!')
    try:
        users.insert(user)
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error":str(e)}
    return user

# Route testing
@hug.get("/getAllUsers/")
def getUsers(response, hug_usersdb):
    temp = []
    for row in hug_usersdb.execute('SELECT * FROM users;'):
        temp.append(row)
    print('BEFORE THIS^')
    return temp

# Authenticate user
@hug.get("/login/")
def login(username:hug.types.text, password:hug.types.text, hug_usersdb):
    sql = 'SELECT username, password FROM users WHERE (username = ? AND password = ?)'
    user = query(hug_usersdb, sql, [username, password], one=True)
    if not user:
        return {'Error':'Authentication error, cannot log in user!'}
    return {'Status':'Login successful'}

# Delete user - not always successful
@hug.post("/deleteuser/")
def login(username:hug.types.text, password:hug.types.text, hug_usersdb):
    sql = 'DELETE FROM users WHERE (username = ? AND password = ?)'
    print(username, password)
    user = query(hug_usersdb, sql, [username, password], one=True)
    if not user:
        return {'Error':'Authentication error, cannot delete user!'}
    return {'Status':'Deletion successful'}

# timeline - public
@hug.get("/timeline/public/")
def getUsers(hug_postsdb):
    sql = 'SELECT * FROM posts'
    public_timeline = query(hug_postsdb, sql, [], one=True)
    if not public_timeline:
        return {'Error':'Cannot find any posts!'}
    return {'Posts':public_timeline}

# post - create
@hug.post("/create/post")
def getUsers(username: hug.types.text, post_text: hug.types.text, timestamp: hug.type.text, hug_postsdb):
    sql = 'INSERT INTO posts (username, post, timestamp) VALUES (?, ?, ?)'
    post = query(hug_postsdb, sql, [username, post_text, timestamp], one=True)
    if not post:
        return {"Error":"Cannot create post"}
    return{"New post":post}



#hug.API(__name__).http.serve(port=8001)
