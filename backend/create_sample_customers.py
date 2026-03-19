#!/usr/bin/env python3
"""Create sample customers"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def create_customers():
    with app.app_context():
        # Check if customers exist
        existing = User.query.filter_by(user_type='customer').first()
        if existing:
            print("Customers already exist!")
            return
        
        customers_data = [
            {"first_name": "Raj", "last_name": "Patel", "email": "raj.patel@example.com", "phone": "9876543201"},
            {"first_name": "Priya", "last_name": "Sharma", "email": "priya.sharma@example.com", "phone": "9876543202"},
            {"first_name": "Amit", "last_name": "Kumar", "email": "amit.kumar@example.com", "phone": "9876543203"},
            {"first_name": "Sneha", "last_name": "Gupta", "email": "sneha.gupta@example.com", "phone": "9876543204"},
            {"first_name": "Vikram", "last_name": "Singh", "email": "vikram.singh@example.com", "phone": "9876543205"},
        ]
        
        for cdata in customers_data:
            user = User(
                first_name=cdata["first_name"],
                last_name=cdata["last_name"],
                email=cdata["email"],
                phone=cdata["phone"],
                user_type="customer"
            )
            user.set_password("customer123")
            db.session.add(user)
            print(f"Created customer: {cdata['first_name']} {cdata['last_name']}")
        
        db.session.commit()
        print("\nDone! Sample customers created.")

if __name__ == "__main__":
    create_customers()
