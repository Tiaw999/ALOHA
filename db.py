# db.py
import mysql.connector

# Set up the database connection (global connection)
conn = mysql.connector.connect(
    host='localhost',  # Your host
    user='root',  # Your username
    password='Cooldaisy662',  # Your password
    database='store_manager'  # Your database
)

# Create a cursor to interact with the database
cursor = conn.cursor()


def get_stores():
    # Query to fetch stores from the stores table
    cursor.execute("SELECT storename FROM stores")  # Adjust the query to your table
    stores = cursor.fetchall()  # Fetch all store names
    return [store[0] for store in stores]  # Return list of store names


def authenticate_user(storename, name, password):
    # Example query to authenticate user (adjust query as needed)
    cursor.execute("SELECT role FROM staff WHERE storename = %s AND name = %s AND password = %s",
                   (storename, name, password))
    result = cursor.fetchone()  # Get the first result (assuming one row)

    if result:
        return result[0]  # Return the role of the user
    return None


# Add any other functions that interact with the database here

# Don't forget to close the cursor and connection when you're done (in your main script or at the end of db operations)
def close_connection():
    cursor.close()
    conn.close()