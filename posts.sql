PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS posts(
    username TEXT,
    post TEXT,
    timestamp TEXT,
    repost TEXT,
    PRIMARY KEY (username, timestamp)
);

INSERT INTO posts (username, post, timestamp) VALUES(
    "reindeer",
    "I think I will buy the red car, or I will lease the blue one.",
    "09-23-1923"
);

INSERT INTO posts (username, post, timestamp) VALUES(
    "star-lord",
    "There was coal in his stocking and he was thrilled.",
    "05-08-1934"
);

INSERT INTO posts (username, post, timestamp) VALUES(
    "rye",
    "The busker hoped that the people passing by would throw money, but they threw tomatoes instead, so he exchanged his hat for a juicer.",
    "08-11-1945"
);

INSERT INTO posts (username, post, timestamp) VALUES(
    "thegreenmile",
    "There was coal in his stocking and he was thrilled.",
    "07-28-2000"
);

INSERT INTO posts (username, post, timestamp) VALUES(
    "reindeer",
    "We need to rent a room for our party.",
    "09-24-1923"
);

INSERT INTO posts (username, post, timestamp) VALUES(
    "thegreenmile",
    "She thought there'd be sufficient time if she hid her watch.",
    "09-23-1923"
);

INSERT INTO posts (username, post, timestamp) VALUES(
    "rye",
    "The bug was having an excellent day until he hit the windshield.",
    "01-23-1983"
);