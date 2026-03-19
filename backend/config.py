"""
Database configuration for BookMyShoot.

By default the application will use a local SQLite file (good for restarting
from scratch and local development). If you want to connect to MySQL/MariaDB
instead, replace the `DATABASE_URI` value below with your MySQL connection
string (example commented).

To reset and work locally, this project now defaults to SQLite and does not
automatically connect to any remote MySQL instance.
"""

# Use local SQLite by default (file: bookmyshoot.db)
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Ensure DB is always in the backend/ folder regardless of where script runs
DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'bookmyshoot.db')

# UPI Configuration for Refunds
UPI_ID = 'bookmyshoot@upi'
UPI_NAME = 'BookMyShoot'
UPI_BANK = 'Sample Bank'

# Example MySQL configuration (uncomment and edit to use MySQL/MariaDB):
# DATABASE_URI = 'mysql+pymysql://root:your_password@localhost/bookmyshoot'

# Notes:
# - To delete a remote MySQL/MariaDB database, see `backend/drop_database.py`
# - When switching back to MySQL, ensure `PyMySQL` is installed and the
#   connection string has correct credentials.

# PostgreSQL Configuration (alternative)
# DATABASE_URI = 'postgresql://username:password@localhost/bookmyshoot'
