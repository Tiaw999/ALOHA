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

        # Table: users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('Owner', 'Manager', 'Employee') NOT NULL
            )
        """)

        # Table: expenses
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INT AUTO_INCREMENT PRIMARY KEY,
                expense_type VARCHAR(50),
                amount DECIMAL(10, 2),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table: revenue
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS revenue (
                id INT AUTO_INCREMENT PRIMARY KEY,
                source VARCHAR(50),
                amount DECIMAL(10, 2),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table: merchandise
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS merchandise (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100),
                quantity INT,
                price DECIMAL(10, 2)
            )
        """)

        # Table: invoices
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_name VARCHAR(100),
                total_amount DECIMAL(10, 2),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table: withdrawals
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS withdrawals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                amount DECIMAL(10, 2),
                reason VARCHAR(100),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table: payroll
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payroll (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_name VARCHAR(100),
                amount DECIMAL(10, 2),
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table: timesheets
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS timesheets (
                id INT AUTO_INCREMENT PRIMARY KEY,
                employee_id INT,
                clock_in DATETIME,
                clock_out DATETIME,
                FOREIGN KEY (employee_id) REFERENCES users(id)
            )
        """)

        # Sample Users
        cursor.execute("""
            INSERT IGNORE INTO users (username, password, role)
            VALUES
                ('owner1', 'password123', 'Owner'),
                ('manager1', 'password123', 'Manager'),
                ('employee1', 'password123', 'Employee')
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