import sqlite3
from database import init_db, add_admin

def refresh_database():
    # Connect to the database
    conn = sqlite3.connect('blogsite.db')
    cursor = conn.cursor()

    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Delete all rows from each table
    for table in tables:
        table_name = table[0]
        print(f"Deleting all rows from {table_name}")
        cursor.execute(f"DELETE FROM {table_name};")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("All tables have been cleared.")

    # Reinitialize the database
    init_db()
    print("Database reinitialized.")

    # Add the admin user back
    add_admin()
    print("Admin user added.")

if __name__ == "__main__":
    refresh_database()