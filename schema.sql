DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS plants CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    username TEXT,
    content TEXT NOT NULL
);

CREATE TABLE plants (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    price INTEGER
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    rights TEXT
);

INSERT INTO plants (name, price) VALUES ('Pennimuori', 15);
INSERT INTO plants (name, price) VALUES ('Orkidea', 10);
INSERT INTO plants (name, price) VALUES ('Jukkapalmu', 15);
