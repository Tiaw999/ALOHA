# db.py
import mysql.connector

# Central DB config — users only edit these two!
db_user = 'root'
db_password = 'Cooldaisy662'

db_config = {
    'host': 'localhost',
    'user': db_user,
    'password': db_password,
    'database': 'store_manager'
}

def get_connection():
    """Return a new DB connection with a selected database."""
    return mysql.connector.connect(**db_config)

def get_connection_without_db():
    """Return a connection without specifying a database."""
    return mysql.connector.connect(
        host='localhost',
        user=db_user,
        password=db_password
    )

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
        """
        SELECT role 
        FROM staff 
        WHERE storename = %s 
        AND BINARY name = %s 
        AND BINARY password = %s
        """,
        (storename, name, password)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None
