DROP TABLE IF EXISTS posts;

CREATE TABLE users (
    id SERIAL NOT NULL,
    full_name VARCHAR NOT NULL,
    login VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);