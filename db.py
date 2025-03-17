# db.py
import sqlite3

DB_PATH = 'store_manager.db'  # Change path as needed

def get_connection():
    return sqlite3.connect(DB_PATH)

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