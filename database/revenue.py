import mysql.connector
from mysql.connector import Error

# MySQL credentials (you may want to use environment variables for production)
HOST = 'localhost'
USER = 'root'
PASSWORD = 'Cooldaisy662'
DATABASE = 'store_manager'

# Connect to the MySQL database
def connect_to_db():
    try:
        conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE)
        if conn.is_connected():
            print('Successfully connected to the database')
            return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to add revenue
def add_revenue(storename, reg, credit, cashinenvelope):
    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO revenue (storename, reg, credit, cashinenvelope)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (storename, reg, credit, cashinenvelope))
            conn.commit()
            print("Revenue added successfully.")
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error adding revenue: {e}")

# Function to view revenue for a store
def view_revenue(storename):
    try:
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT * FROM revenue WHERE storename = %s
            """
            cursor.execute(query, (storename,))
            records = cursor.fetchall()
            print(f"Revenue for {storename}:")
            for row in records:
                print(f"Invoicenum: {row[0]}, Store: {row[1]}, Reg: {row[2]}, Credit: {row[3]}, Cash Envelope: {row[4]}, Date: {row[5]}")
            cursor.close()
            conn.close()
    except Error as e:
        print(f"Error viewing revenue: {e}")

if __name__ == "__main__":
    # Example of adding revenue
    add_revenue('aloha', 500.00, 200.00, 150.00)

    # Example of viewing revenue
    view_revenue('aloha')