timeline: gunicorn timeline:__hug_wsgi__ --bind=localhost:$PORT
polls: gunicorn polls:__hug_wsgi__ --bind=localhost:$PORT
serviceregistry: gunicorn serviceregistry:__hug_wsgi__ --bind=localhost:$PORT
users: gunicorn users:__hug_wsgi__ --bind=localhost:$PORT
dynamo_local: java -Djava.library.path=bin/dynamodb_local_latest/DynamoDBLocal_lib -jar bin/dynamodb_local_latest/DynamoDBLocal.jar -sharedDb -dbPath var/
beanstalkd: beanstalkd
beanstalk_consumer: python3 beanstalk_consumer.py
# Use this command to run foreman: foreman start -m beanstalkd=1,beanstalk_consumer=1,dynamo_local=1,timeline=3,polls=1,serviceregistry=1,users=1 -p 5100