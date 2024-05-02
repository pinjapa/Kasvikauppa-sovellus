DROP TABLE IF EXISTS Feedbacks CASCADE;
DROP TABLE IF EXISTS Plants CASCADE;
DROP TABLE IF EXISTS Accounts CASCADE;
DROP TABLE IF EXISTS Categories CASCADE;
DROP TABLE IF EXISTS Descriptions CASCADE;

CREATE TABLE Feedbacks (
    id SERIAL PRIMARY KEY,
    username TEXT,
    content TEXT NOT NULL,
    stars INTEGER
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
    price INTEGER,
    category_id INTEGER
);

CREATE TABLE Categories (
    id SERIAL PRIMARY KEY, 
    name TEXT
);

CREATE TABLE Descriptions (
    id SERIAL PRIMARY KEY, 
    content TEXT,
    plant_id INTEGER REFERENCES Plants,
    username_id INTEGER REFERENCES Accounts
);

INSERT INTO Categories (name) VALUES ('Nahkealehtiset kasvit');
INSERT INTO Categories (name) VALUES ('Kukat');
INSERT INTO Categories (name) VALUES ('Köynnöskasvit');
INSERT INTO Categories (name) VALUES ('Muut');
INSERT INTO Accounts (username, password, rights) VALUES ('Omistaja', 'scrypt:32768:8:1$l5XlEaf7BdF8dYmn$05dbb1e924066de52abd4355b469df8e74e1d618e5ae940d606ac84279a7d23075525cf28fb308d7a146b9b114d2783e50b4fa632324ba1cef58d0e8b5b2f4a6', 'admin');
