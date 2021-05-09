CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
CREATE TABLE areas (id SERIAL PRIMARY KEY, area TEXT UNIQUE, request_amount INTEGER);
CREATE TABLE requests (id SERIAL PRIMARY KEY, request TEXT, area_id INTEGER REFERENCES areas);
CREATE TABLE request (id SERIAL PRIMARY KEY, request_title TEXT, need TEXT, offer TEXT, contact TEXT, postedby TEXT, area_id INTEGER REFERENCES areas);
CREATE TABLE adminpass (id SERIAL PRIMARY KEY, password TEXT, changedby TEXT);

INSERT INTO adminpass (password) VALUES ('pbkdf2:sha256:150000$AjqydGJz$e9d040687651ef8b7891bc3e5ac11671a21ab68f9c8d5e39f0c2cf80d951234a');
INSERT INTO users (username, password, admin) VALUES ('admin', 'pbkdf2:sha256:150000$AevnYeuQ$0a573520d78ed00d0db37ac453745a7847e1aed50191ad31509ee28961e54317', True);
