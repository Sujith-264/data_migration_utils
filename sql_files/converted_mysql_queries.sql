CREATE TABLE employees (
id INT IDENTITY PRIMARY KEY +
first_name VARCHAR(50) +
last_name VARCHAR(50)
)

SELECT TOP 10 id + first_name + ' ' + last_name AS full_name FROM employees


SELECT first_name + ' ' + last_name AS full_name FROM employees


SELECT id + first_name + last_name FROM employees WHERE hire_date > GETDATE()


SELECT id + first_name + last_name FROM employees WHERE hire_date = CURRENT_DATE

