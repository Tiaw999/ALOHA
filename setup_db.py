# setup_db.py
import re
from mysql.connector import Error
from db import get_connection, get_connection_without_db

def execute_sql_file(filename, use_db=True):
    try:
        conn = get_connection() if use_db else get_connection_without_db()
        cursor = conn.cursor()

        with open(filename, 'r') as file:
            sql_script = file.read()

            # Define a pattern to match triggers and procedures
            trigger_pattern = r'CREATE TRIGGER.*?END;'  # Non-greedy match for triggers
            procedure_pattern = r'CREATE PROCEDURE.*?END;'  # Non-greedy match for procedures

            # Find all triggers and procedures in the script
            triggers = re.findall(trigger_pattern, sql_script, re.DOTALL)
            procedures = re.findall(procedure_pattern, sql_script, re.DOTALL)

            # Remove the triggers and procedures from the original SQL script
            sql_script = re.sub(trigger_pattern, '', sql_script)
            sql_script = re.sub(procedure_pattern, '', sql_script)

            # Split the rest of the script into individual statements
            sql_statements = sql_script.split(';')

            # Combine the found triggers and procedures back into the script
            sql_statements.extend(triggers)
            sql_statements.extend(procedures)

            # Execute each statement
            for statement in sql_statements:
                statement = statement.strip()

                # Skip empty statements
                if not statement:
                    continue

                try:
                    print(f"Executing: {statement}")  # Debugging statement execution
                    cursor.execute(statement)  # Execute each SQL command
                except Exception:
                    pass
        conn.commit()
        print(f"✅ Executed SQL file: {filename}")
        cursor.close()
        conn.close()

    except Error as e:
        print(f"❌ Error executing {filename}: {e}")

if __name__ == "__main__":
    execute_sql_file("schema.sql", use_db=False)
    execute_sql_file("sample_data.sql", use_db=True)
