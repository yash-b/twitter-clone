In order to test the performance of a sync endpoint vs an async endpoint which queues work onto beanstalk we created a version of create/post where instead of writing directly to the sqllite db we queue the post as a json string onto beanstalk (for async processing).

The performance results are stored in this folder under 'hey_sync' and 'hey_async'.

The difference in performance is that the async endpoint can respond to requests 45% faster.

The commands used to test this:

For sync:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007?"}' http://localhost:1936/create/post

For async:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007?"}' http://localhost:1936/create/post_async

Note: the basic authorization feature of 'hey' does not seem to be working, but simply passing a raw basic authentation header with the base64 of the auth info does work.


The implementation of the async post used to do this benchmark looked like this:

@hug.post("/create/post_async", requires=checkUserAuthorization)
def createPostAsync(request, username: hug.types.text, post_text: hug.types.text, response, **kwargs):
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
        with greenstalk.Client(('127.0.0.1', 11300)) as client:
            client.put(json.dumps(post))
    except Exception as e:
        response.status = hug.falcon.HTTP_409
        return {"error":str(e)}

    response.status = hug.falcon.HTTP_202
    return {"status":"success"}