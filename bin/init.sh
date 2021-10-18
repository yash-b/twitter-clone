sqlite-utils create-table ./var/users.db users username text bio text email text password text --pk=username
sqlite-utils create-table ./var/posts.db posts username text post text timestamp text repost text --fk username users username
