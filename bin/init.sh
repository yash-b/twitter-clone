rm ./var/users.db
rm ./var/posts.db
sqlite3 ./var/users.db < users.sql
sqlite3 ./var/posts.db < posts.sql
