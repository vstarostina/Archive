CREATE TABLE IF NOT EXISTS users
(
    id integer PRIMARY KEY AUTOINCREMENT,
    login text NOT NULL,
    password text NOT NULL,
    category integer NOT NULL
);

CREATE TABLE IF NOT EXISTS dan_prof(
    id integer PRIMARY KEY AUTOINCREMENT,
    id_client integer NOT NULL,
    fio text NOT NULL,
    tel integer NOT NULL,
    email text NOT NULL,
    pasport text NOT NULL
);

CREATE TABLE IF NOT EXISTS credit(
    id integer PRIMARY KEY AUTOINCREMENT,
    text text NOT NULL,
    sum integer NOT NULL
);

