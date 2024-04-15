DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS plants CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;

CREATE TABLE Messages (
    id SERIAL PRIMARY KEY,
    username TEXT,
    content TEXT NOT NULL
);

CREATE TABLE Accounts (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    rights TEXT
);

CREATE TABLE Plants (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    price INTEGER
);

CREATE TABLE Categories (
    id SERIAL PRIMARY KEY, 
    name TEXT,
    plant_ids INTEGER
);



INSERT INTO plants (name, price) VALUES ("Pennimuori", 15);
INSERT INTO plants (name, price) VALUES ("Orkidea", 10);
INSERT INTO plants (name, price) VALUES ("Jukkapalmu", 15);
