# db.py
import mysql.connector

# Central DB config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Cooldaisy662',
    'database': 'store_manager'
}

def get_connection():
    """Return a new DB connection."""
    return mysql.connector.connect(**db_config)

def get_stores():
    """Fetch store names from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT storename FROM stores")
    stores = cursor.fetchall()
    cursor.close()
    conn.close()
    return [store[0] for store in stores]

def authenticate_user(storename, name, password):
    """Authenticate user and return their role if valid."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role FROM staff WHERE storename = %s AND name = %s AND password = %s",
        (storename, name, password)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None