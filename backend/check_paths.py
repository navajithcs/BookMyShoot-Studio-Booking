import os
import sys
from app import app
from config import DATABASE_URI

print(f"CWD: {os.getcwd()}")
print(f"Script: {sys.argv[0]}")
print(f"DATABASE_URI: {DATABASE_URI}")
print(f"Abs Path of DB (if relative): {os.path.abspath('bookmyshoot.db')}")

# Check if file exists
if os.path.exists('bookmyshoot.db'):
    print("bookmyshoot.db FOUND in CWD")
else:
    print("bookmyshoot.db NOT FOUND in CWD")

# Check inside backend just in case
if os.path.exists('backend/bookmyshoot.db'):
    print("backend/bookmyshoot.db FOUND")
