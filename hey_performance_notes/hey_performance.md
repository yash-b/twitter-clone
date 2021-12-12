In order to test the performance of a sync endpoint vs an async endpoint which queues work onto beanstalk we created a version of create/post where instead of reading/writing directly to the sqllite db, dynamo, and sending emails we queue the post as a json string onto beanstalk for async processing.

The performance results are stored in this folder under 'hey_sync' and 'hey_async'.

The difference in performance is that the async endpoint can respond to requests 30x faster.

The commands used to test this (Contains an invalid poll to trigger the SMTP codepath):

For sync:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"useremail":"dest_email@gmail.com","username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007? http://localhost:1936/results/12"}' http://localhost:1936/create/post

For async:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"useremail":"dest_email@gmail.com","username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007? http://localhost:1936/results/12"}' http://localhost:1936/create/post_async

Note: the basic authorization feature of 'hey' does not seem to be working, but simply passing a raw basic authentation header with the base64 of the auth info does work.

