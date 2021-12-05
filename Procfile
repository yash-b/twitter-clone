users: gunicorn users:__hug_wsgi__ --bind=localhost:$PORT
timeline: gunicorn timeline:__hug_wsgi__ --bind=localhost:$PORT
polls: gunicorn polls:__hug_wsgi__ --bind=localhost:$PORT
serviceregistry: gunicorn serviceregistry:__hug_wsgi__ --bind=localhost:$PORT
# Use this command to run foreman: foreman start -m users=1,timeline=3,polls=1,serviceregistry=1 -p 5000