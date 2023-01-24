CREATE TABLE IF NOT EXISTS mainmenu
(
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS employee
(
    id integer PRIMARY KEY AUTOINCREMENT,
    last_name text NOT NULL,
    first_name text NOT NULL,
    o_patronymic text NOT NULL,
    d_position text NOT NULL,
    birthday data
);

CREATE TABLE IF NOT EXISTS addrequest
(
    id integer PRIMARY KEY AUTOINCREMENT,
    pp integer NOT NULL,
    data_nach data NOT NULL,
    data_kon data NOT NULL,
    data_tek data NOT NULL,
    employee_id INTEGER NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS users
(
    id integer PRIMARY KEY AUTOINCREMENT,
    login text NOT NULL,
    password text NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS documents
(
    id integer PRIMARY KEY AUTOINCREMENT,
    inventory_number integer NOT NULL,
    name_doc text NOT NULL,
    type_doc text NOT NULL,
    pp text NOT NULL,
    years integer NOT NULL,
    shelf_life integer NOT NULL,
    counts integer NOT NULL,
    data_add data NOT NULL
);

CREATE TABLE IF NOT EXISTS orders
(
    id integer PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    documents_id INTEGER NOT NULL,
    type_orders text NOT NULL,
    data data NOT NULL,
    nomber integer NOT NULL,
    page integer NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(id),
    FOREIGN KEY (documents_id) REFERENCES documents(id)
);

CREATE TABLE IF NOT EXISTS personal_accounts
(
    id integer PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    years integer NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employee(id)
);

CREATE TABLE IF NOT EXISTS calc_by_month
(
    id integer PRIMARY KEY AUTOINCREMENT,
    personal_accounts_id INTEGER NOT NULL,
    month_calc text NOT NULL,
    summ integer NOT NULL,
    FOREIGN KEY (personal_accounts_id) REFERENCES personal_accounts(id)
);

CREATE TABLE IF NOT EXISTS allemployee
(
    id integer PRIMARY KEY AUTOINCREMENT,
    last_name text NOT NULL,
    first_name text NOT NULL,
    o_patronymic text NOT NULL,
    pp integer NOT NULL
);

CREATE TABLE IF NOT EXISTS  deletes 
(
	id	integer PRIMARY KEY AUTOINCREMENT,
	del_number integer NOT NULL,
    name_doc text NOT NULL,
    type_doc text NOT NULL,
    pp text NOT NULL,
    years integer NOT NULL,
    shelf_life integer NOT NULL,
    counts integer NOT NULL,
    data_add data NOT NULL,
    data_del integer NOT NULL
);

CREATE TABLE IF NOT EXISTS inventories 
(
	id	integer PRIMARY KEY AUTOINCREMENT,
	inventorie	integer NOT NULL
);

CREATE TABLE IF NOT EXISTS act
(
	id	integer PRIMARY KEY AUTOINCREMENT,
	act	text NOT NULL
);