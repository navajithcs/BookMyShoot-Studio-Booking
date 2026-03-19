"""Migration script to add location column to photographers table"""
import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'bookmyshoot.db')
    
    # Check if column already exists
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table schema
    cursor.execute("PRAGMA table_info(photographers)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'location' not in columns:
        print("Adding 'location' column to photographers table...")
        cursor.execute("ALTER TABLE photographers ADD COLUMN location VARCHAR(255)")
        conn.commit()
        print("Column added successfully!")
    else:
        print("Column 'location' already exists.")
    
    conn.close()

if __name__ == '__main__':
    migrate()
