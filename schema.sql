
CREATE TABLE messages (
    id INTEGER PRIMARY KEY, 
    content TEXT
);

CREATE TABLE plants (
    id INTEGER PRIMARY KEY, 
    name TEXT,
    price INTEGER
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);