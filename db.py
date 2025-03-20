# db.py
import mysql.connector

def authenticate_user(store, user, password):
    try:
        # Connect to the MySQL database (update with your credentials)
        conn = mysql.connector.connect(
            host="localhost",  # Replace with your DB host
            user="root",  # Replace with your DB username
            password="Cooldaisy662",  # Replace with your DB password
            database="store_db"  # Replace with your database name
        )
        cursor = conn.cursor()

        # Query to authenticate user
        query = "SELECT role FROM users WHERE store_name = %s AND username = %s AND password = %s"
        cursor.execute(query, (store, user, password))

        # Fetch one result
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the role (e.g., 'Owner', 'Manager', 'Employee')
        else:
            return None

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

    finally:
        if conn:
            conn.close()