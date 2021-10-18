PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    bio TEXT,
    email TEXT,
    password TEXT
);

CREATE TABLE IF NOT EXISTS posts(
    username TEXT,
    post TEXT,
    timestamp TEXT,
    repost TEXT,
    FOREIGN KEY (username) REFERENCES users (username)
);