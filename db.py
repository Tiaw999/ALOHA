# db.py
import mysql.connector
from mysql.connector import Error

# Update these values with your MySQL credentials
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Cooldaisy662',
    'database': 'store_manager'  # The DB name you'll create
}

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ---------- USER AUTHENTICATION ----------

def authenticate_user(role, username, password):
    """
    Authenticate a user based on role.
    role: 'owner', 'manager', or 'employee'
    """
    table_map = {
        'owner': 'Owners',
        'manager': 'Managers',
        'employee': 'Employees'
    }

    table = table_map.get(role.lower())
    if not table:
        raise ValueError("Invalid role specified")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT * FROM {table}
            WHERE username = ? AND password = ?
        """, (username, password))
        result = cursor.fetchone()

    return result  # None if not found, otherwise user record tuple

# ---------- DATA FETCHING (Placeholder Examples) ----------

def get_store_expenses(store_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Expenses WHERE store_name = ?
        """, (store_name,))
        return cursor.fetchall()

def get_store_revenue(store_name):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Revenue WHERE store_name = ?
        """, (store_name,))
        return cursor.fetchall()

# ---------- DATA INSERTION (Placeholder Examples) ----------

def add_expense(store_name, expense_type, amount):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Expenses (store_name, expense_type, amount)
            VALUES (?, ?, ?)
        """, (store_name, expense_type, amount))
        conn.commit()

# Add similar methods for payroll, timesheet, etc. as needed.