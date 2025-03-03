CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50)
);

SELECT id, CONCAT(first_name, ' ', last_name) AS full_name FROM employees LIMIT 10 OFFSET 5;



SELECT CONCAT(first_name, ' ', last_name) AS full_name FROM employees;


SELECT id, first_name, last_name FROM employees WHERE hire_date > NOW();



SELECT id, first_name, last_name FROM employees WHERE hire_date = CURDATE();

