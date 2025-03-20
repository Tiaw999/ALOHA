# setup_db.py
import mysql.connector
from mysql.connector import Error

# MySQL credentials
HOST = 'localhost'
USER = 'root'
PASSWORD = 'Cooldaisy662'

def create_database():
    try:
        conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS store_manager")
        print("Database 'store_manager' created or already exists.")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error creating database: {e}")

def create_tables_and_sample_data():
    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database='store_manager'
        )
        cursor = conn.cursor()

        # Table: STORES
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stores (
                        storename VARCHAR(50) NOT NULL PRIMARY KEY,
                        password VARCHAR(255)
                    )
                """)

        # Table: STAFF
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staff (
                name VARCHAR(50) NOT NULL,
                storename VARCHAR(50) NOT NULL,
                hourlyrate DECIMAL(10, 2),
                bonusrate DECIMAL(10, 2),
                password VARCHAR(255) NOT NULL,
                role ENUM('Owner', 'Manager', 'Employee') NOT NULL,
                PRIMARY KEY(name, storename),
                FOREIGN KEY(storename) references stores(storename)
            )
        """)

        # Table: expenses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                storename VARCHAR(50),
                expensetype VARCHAR(50),
                expensevalue DECIMAL(10, 2),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(storename) references stores(storename)
            )
        """)

        # Table: revenue
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue (
                id INT AUTO_INCREMENT PRIMARY KEY,
                storename VARCHAR(50),
                reg DECIMAL(10, 2),
                credit DECIMAL(10, 2),
                cashinenvelope DECIMAL(10, 2),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(storename) references stores(storename)
            )
        """)

        # Table: merchandise
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS merchandise (
                id INT AUTO_INCREMENT PRIMARY KEY,
                storename VARCHAR(50),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                merchtype VARCHAR(255),
                merchvalue DECIMAL(10, 2),
                FOREIGN KEY(storename) references stores(storename)
            )
        """)

        # Table: invoices
        cursor.execute("""
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
                FOREIGN KEY(storename) references stores(storename)
            )
        """)

        # Table: withdrawals
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS withdrawals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                storename VARCHAR(50),
                empname VARCHAR(50),
                amount DECIMAL(10, 2),
                notes VARCHAR(100),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(empname, storename) references staff(name, storename)
            )
        """)

        # Table: payroll
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payroll (
                id INT AUTO_INCREMENT PRIMARY KEY,
                empname VARCHAR(50),
                storename VARCHAR(50),
                regularpay DECIMAL(10, 2),
                bonus DECIMAL(10, 2),
                paydate DATE,
                FOREIGN KEY(empname, storename) references staff(name, storename)
            )
        """)

        # Table: timesheet
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timesheet (
                id INT AUTO_INCREMENT PRIMARY KEY,
                storename VARCHAR(50),
                empname VARCHAR(50),
                clock_in DATETIME,
                clock_out DATETIME,
                regin DECIMAL(10, 2),
                regout DECIMAL(10, 2),
                FOREIGN KEY (empname, storename) REFERENCES staff(name, storename)
            )
        """)

        # Sample stores
        cursor.execute("""
            INSERT INTO stores (storename, password)
            VALUES ('aloha', 'storepass1'), ('aloha2', 'storepass2'), ('aloha3', 'storepass3')
        """)

        # Sample staff
        cursor.execute("""
            INSERT IGNORE INTO staff (name, storename, hourlyrate, bonusrate, password, role)
            VALUES
                ('owner1', 'aloha', '25', '0.03', 'password123', 'Owner'),
                ('manager1', 'aloha2', '20', '.02', 'password123', 'Manager'),
                ('employee1', 'aloha3', '15', '.01', 'password123', 'Employee')
        """)

        conn.commit()
        print("Tables created and sample data inserted.")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error creating tables: {e}")

if __name__ == "__main__":
    create_database()
    create_tables_and_sample_data()