sqlite3 ./var/users.db < users.sql
sqlite3 ./var/posts.db < posts.sql
foreman start -m users=1,timeline=3 -p 5000
