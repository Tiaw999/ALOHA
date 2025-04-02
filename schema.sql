-- Create Database
CREATE DATABASE IF NOT EXISTS store_manager;
USE store_manager;

-- Create Stores Table
CREATE TABLE IF NOT EXISTS stores (
    storename VARCHAR(50) NOT NULL PRIMARY KEY,
    password VARCHAR(255)
);

-- Create Staff Table
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

-- Create Expenses Table
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
