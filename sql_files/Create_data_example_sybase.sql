CREATE TABLE Employee (
    ID INT PRIMARY KEY,
    Name VARCHAR(50),
    Salary DECIMAL(10, 2)
)
INSERT INTO Employee (ID, Name, Salary) VALUES (1, 'Alice', 50000.00)
INSERT INTO Employee (ID, Name, Salary) VALUES (2, 'Bob', 60000.00)
INSERT INTO Employee (ID, Name, Salary) VALUES (3, 'Charlie', 55000.00)
SELECT * FROM Employee;