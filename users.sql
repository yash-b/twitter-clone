CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    bio TEXT,
    email TEXT UNIQUE,
    password TEXT
);

INSERT INTO users (username, bio, email,password) VALUES("reindeer",
"I think I will buy the red car",
"reindeerblazarpiepie@gmail.com",
"reindeer"
);

INSERT INTO users (username, bio, email,password) VALUES("star-lord",
"She wondered what his eyes were saying",
"star-lord@gmail.com",
"star-lord"
);

INSERT INTO users (username, bio, email,password) VALUES("rye",
"The stench from the feedlot",
"rye@gmail.com",
"rye"
);

INSERT INTO users (username, bio, email,password) VALUES("thegreenmile",
"She wondered what his eyes were saying",
"thegreenmile@gmail.com",
"thegreenmile"
);

INSERT INTO users (username, bio, email,password) VALUES("lastrada",
"In hopes of finding out the truth",
"lastrada@gmail.com",
"lastrada"
);

INSERT INTO users (username, bio, email,password) VALUES("kyanite",
"Entered the one-room library",
"kyanite@gmail.com",
"kyanite"
);

