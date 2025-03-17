# setup_db.py
import sqlite3

DB_PATH = 'store_manager.db'

def create_tables():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Owners Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Owners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # Managers Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Managers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # Employees Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        # Expenses Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                expense_type TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE
            )
        """)

        # Revenue Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Revenue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                revenue_type TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE
            )
        """)

        # Merchandise Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Merchandise (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)

        # Invoices Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                invoice_number TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE
            )
        """)

        # Withdrawals Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Withdrawals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE
            )
        """)

        # Payroll Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payroll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                store_name TEXT NOT NULL,
                employee_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                date TEXT DEFAULT CURRENT_DATE,
                FOREIGN KEY (employee_id) REFERENCES Employees(id)
            )
        """)

        # Timesheet Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Timesheet (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                clock_in TEXT NOT NULL,
                clock_out TEXT NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES Employees(id)
            )
        """)

        conn.commit()
        print("Tables created successfully.")

def insert_sample_data():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Sample Owner
        cursor.execute("INSERT OR IGNORE INTO Owners (username, password) VALUES (?, ?)", ('owner1', 'pass123'))

        # Sample Manager
        cursor.execute("INSERT OR IGNORE INTO Managers (store_name, username, password) VALUES (?, ?, ?)",
                       ('StoreA', 'manager1', 'pass123'))

        # Sample Employee
        cursor.execute("INSERT OR IGNORE INTO Employees (store_name, username, password) VALUES (?, ?, ?)",
                       ('StoreA', 'employee1', 'pass123'))

        # Sample Expenses
        cursor.execute("INSERT INTO Expenses (store_name, expense_type, amount) VALUES (?, ?, ?)",
                       ('StoreA', 'Utilities', 120.50))

        # Sample Revenue
        cursor.execute("INSERT INTO Revenue (store_name, revenue_type, amount) VALUES (?, ?, ?)",
                       ('StoreA', 'Sales', 500.00))

        conn.commit()
        print("Sample data inserted successfully.")

if __name__ == '__main__':
    create_tables()
    insert_sample_data()