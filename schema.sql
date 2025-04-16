-- Create Database
CREATE DATABASE IF NOT EXISTS store_manager;
USE store_manager;
-- Create Stores Table
CREATE TABLE IF NOT EXISTS stores (
    storename VARCHAR(50) NOT NULL PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS staff (
    name VARCHAR(50) NOT NULL,
    storename VARCHAR(50) NOT NULL,
    hourlyrate DECIMAL(10, 2),
    bonusrate DECIMAL(10, 2),
    password VARCHAR(255) NOT NULL,
    role ENUM('Owner', 'Manager', 'Employee') NOT NULL,
    PRIMARY KEY(name, storename),
    FOREIGN KEY(storename) REFERENCES stores(storename)
);
CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    storename VARCHAR(50),
    expensetype VARCHAR(50),
    expensevalue DECIMAL(10, 2),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(storename) REFERENCES stores(storename)
);

-- Create Revenue Table
CREATE TABLE IF NOT EXISTS revenue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    storename VARCHAR(50),
    reg DECIMAL(10, 2),
    credit DECIMAL(10, 2),
    cashinenvelope DECIMAL(10, 2),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(storename) REFERENCES stores(storename)
);

-- Create Merchandise Table
CREATE TABLE IF NOT EXISTS merchandise (
    id INT AUTO_INCREMENT PRIMARY KEY,
    storename VARCHAR(50),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    merchtype VARCHAR(255),
    merchvalue DECIMAL(10, 2),
    FOREIGN KEY(storename) REFERENCES stores(storename)
);

-- Create Invoices Table
CREATE TABLE IF NOT EXISTS invoices (
    invoicenum VARCHAR(255) PRIMARY KEY,
    storename VARCHAR(50),
    datereceived DATE,
    company VARCHAR(100),
    amount DECIMAL(10, 2),
    duedate DATE,
    paid BOOLEAN,
    datepaid DATE,
    paidwith ENUM('CREDIT', 'CASH'),
    FOREIGN KEY(storename) REFERENCES stores(storename)
);

-- Create Withdrawals Table
CREATE TABLE IF NOT EXISTS withdrawals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    storename VARCHAR(50),
    empname VARCHAR(50),
    amount DECIMAL(10, 2),
    notes VARCHAR(100),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(empname, storename) REFERENCES staff(name, storename)
);

-- Create Payroll Table
CREATE TABLE IF NOT EXISTS payroll (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empname VARCHAR(50),
    storename VARCHAR(50),
    regularpay DECIMAL(10, 2),
    bonus DECIMAL(10, 2),
    paydate DATE,
    FOREIGN KEY(empname, storename) REFERENCES staff(name, storename)
);

-- Create Timesheet Table
CREATE TABLE IF NOT EXISTS timesheet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    storename VARCHAR(50),
    empname VARCHAR(50),
    clock_in DATETIME,
    clock_out DATETIME,
    regin DECIMAL(10, 2),
    regout DECIMAL(10, 2),
    FOREIGN KEY(empname, storename) REFERENCES staff(name, storename)
);

-- Trigger for Insert: Ensures that no field is empty and the correct data types are used
CREATE TRIGGER validate_expense_insert BEFORE INSERT ON expenses
FOR EACH ROW
BEGIN

    -- Validate expense type: Must not be NULL or empty and must contain non-numeric characters
    IF NEW.expensetype IS NULL OR TRIM(NEW.expensetype) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Expense type cannot be empty.';
    END IF;

    IF NEW.expensetype REGEXP '^[0-9]+$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Expense type must contain letters.';
    END IF;

    -- Validate expense value: Must be a positive decimal
    IF NEW.expensevalue IS NULL OR NEW.expensevalue <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Expense value must be a positive number.';
    END IF;

END;


-- Trigger for Update: Ensures that no field is empty and the correct data types are used
CREATE TRIGGER validate_expense_update BEFORE UPDATE ON expenses
FOR EACH ROW
BEGIN

    -- Validate expense type: Must not be NULL or empty and must contain non-numeric characters
    IF NEW.expensetype IS NULL OR TRIM(NEW.expensetype) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Expense type cannot be empty.';
    END IF;

    IF NEW.expensetype REGEXP '^[0-9]+$' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Expense type must contain letters.';
    END IF;

    -- Validate expense value: Must be a positive decimal
    IF NEW.expensevalue IS NULL OR NEW.expensevalue <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Expense value must be a positive number.';
    END IF;

END;

CREATE PROCEDURE insert_expense (
    IN p_storename VARCHAR(50),
    IN p_expensetype VARCHAR(50),
    IN p_expensevalue DECIMAL(10,2),
    IN p_date DATE
)
BEGIN
    -- Call the trigger automatically (this is done by MySQL once insert occurs)
    INSERT INTO expenses (storename, expensetype, expensevalue, date)
    VALUES (p_storename, p_expensetype, p_expensevalue, p_date);
END;

CREATE PROCEDURE update_expense (
    IN p_id INT,
    IN p_date DATE,
    IN p_expensetype VARCHAR(50),
    IN p_expensevalue DECIMAL(10,2)
)
BEGIN
    -- Call the trigger automatically (this is done by MySQL once update occurs)
    UPDATE expenses
    SET expensetype = p_expensetype,
        expensevalue = p_expensevalue,
        date = p_date
    WHERE id = p_id;
END;
