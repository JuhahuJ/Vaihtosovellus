CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE areas (id SERIAL PRIMARY KEY, area TEXT UNIQUE, request_amount INTEGER);
CREATE TABLE requests (id SERIAL PRIMARY KEY, request TEXT, area_id INTEGER REFERENCES areas);
CREATE TABLE request (id SERIAL PRIMARY KEY, request_title TEXT, need TEXT, offer TEXT, contact TEXT, postedby TEXT, area_id INTEGER REFERENCES areas);
