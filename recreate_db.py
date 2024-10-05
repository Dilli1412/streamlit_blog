import os
import sqlite3
from database import init_db, add_admin

def recreate_db():
    # Remove existing database file
    if os.path.exists('blogsite.db'):
        os.remove('blogsite.db')
        print("Existing database removed.")

    # Initialize new database
    init_db()
    print("New database created.")

    # Add admin user
    add_admin()

if __name__ == "__main__":
    recreate_db()