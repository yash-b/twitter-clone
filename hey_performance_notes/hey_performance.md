In order to test the performance of a sync endpoint vs an async endpoint which queues work onto beanstalk we created a version of create/post where instead of reading/writing directly to the sqllite db, dynamo, and sending emails we queue the post as a json string onto beanstalk for async processing.

The performance results are stored in this folder.

# First comparing sync vs async without a poll url in the post text:

The difference in performance is that the async endpoint can respond to requests 4.8x faster than the sync endpoint.

The commands used to test this:

For sync:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007?"}' http://localhost:1936/create/post

For async:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007?"}' http://localhost:1936/create/post_async

The results for this test are stored in hey_sync_posts and hey_async_posts.

# Next, comparing sync vs async with an invalid post url in the post text:

The difference in performance is that the async endpoint can respond to requests 30x faster than the sync endpoint.

The commands used to test this (Contains an invalid poll url to trigger the SMTP codepath):

For sync:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"useremail":"dest_email@gmail.com","username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007? http://localhost:1936/results/12"}' http://localhost:1936/create/post

For async:
hey -m POST -H "Authorization: Basic cnllOnJ5ZQ==" -H "Content-Type: application/json" -d  '{"useremail":"dest_email@gmail.com","username":"rye","post_text":"Ronaldo back at Man Utd? what is this, 2007? http://localhost:1936/results/12"}' http://localhost:1936/create/post_async

The results for this test are stored in hey_sync_polls and hey_async_polls.

