# setup_db.py
import mysql.connector
from mysql.connector import Error

# MySQL credentials
HOST = 'localhost'
USER = 'root'
PASSWORD = 'Cooldaisy662'
DATABASE = 'store_manager'


def create_database():
    """Creates the database if it does not exist."""
    try:
        conn = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        print(f"Database '{DATABASE}' created or already exists.")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error creating database: {e}")


def execute_sql_file(filename):
    """Executes SQL commands from a file."""
    try:
        conn = mysql.connector.connect(
            host=HOST, user=USER, password=PASSWORD, database=DATABASE
        )
        cursor = conn.cursor()

        with open(filename, 'r') as file:
            sql_script = file.read()

        for statement in sql_script.split(';'):
            if statement.strip():
                cursor.execute(statement)

        conn.commit()
        print(f"Executed SQL file: {filename}")
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Error executing {filename}: {e}")


if __name__ == "__main__":
    create_database()
    execute_sql_file("schema.sql")  # Creates tables
    execute_sql_file("sample_data.sql")  # Inserts sample data