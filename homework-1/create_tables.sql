CREATE TABLE customers
(
	customer_id char(10) PRIMARY KEY,
	company_name varchar(50) NOT NULL,
	contact_name varchar(50) NOT NULL
);

SELECT * FROM customers;

CREATE TABLE employees
(
	employee_id int PRIMARY KEY,
	first_name varchar(10) NOT NULL,
	last_name varchar(50) NOT NULL,
	title varchar(50) NOT NULL,
	birth_date varchar(20) NOT NULL,
	notes text
);

SELECT * FROM employees;

CREATE TABLE orders
(
	order_id int PRIMARY KEY,
	customer_id varchar(10) REFERENCES customers (customer_id) NOT NULL,
	employee_id int REFERENCES employees (employee_id),
	order_date varchar(20) NOT NULL,
	ship_city varchar(20) NOT NULL
);

SELECT * FROM orders;
