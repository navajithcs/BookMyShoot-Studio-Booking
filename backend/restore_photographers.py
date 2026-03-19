#!/usr/bin/env python3
"""Restore deleted photographers"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, Photographer, PortfolioItem

def restore_photographers():
    with app.app_context():
        # Check existing users and photographers
        existing_users = User.query.all()
        existing_photographers = Photographer.query.all()
        
        print(f"Current users: {[(u.id, u.email, u.first_name, u.user_type) for u in existing_users]}")
        print(f"Current photographers: {[(p.id, p.user_id) for p in existing_photographers]}")
        
        # Restore photographers that were deleted
        photographers_data = [
            {
                "user_id": 2,
                "first_name": "John",
                "last_name": "Doe",
                "email": "photo@example.com",
                "phone": "9876543210",
                "specialty": "Wedding & Events",
                "hourly_rate": 200.0,
                "bio": "Professional photographer with 5 years of experience.",
                "portfolio": [
                    {"url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&h=600&fit=crop", "caption": "Wedding Ceremony"},
                    {"url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=800&h=600&fit=crop", "caption": "Couple Portrait"},
                    {"url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&h=600&fit=crop", "caption": "Engagement"},
                ]
            },
            {
                "user_id": 6,
                "first_name": "Alice",
                "last_name": "Smith",
                "email": "alice.photo@example.com",
                "phone": "9876543211",
                "specialty": "Wedding Photography",
                "hourly_rate": 250.0,
                "bio": "Experienced wedding photographer with 7 years in the industry.",
                "portfolio": [
                    {"url": "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800&h=600&fit=crop", "caption": "Wedding Party"},
                    {"url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&h=600&fit=crop", "caption": "First Dance"},
                    {"url": "https://images.unsplash.com/photo-1507504036103?w=800&h=600&fit=crop", "caption": "Ceremony"},
                ]
            },
            {
                "user_id": 7,
                "first_name": "Bob",
                "last_name": "Johnson",
                "email": "bob.photo@example.com",
                "phone": "9876543212",
                "specialty": "Portrait & Events",
                "hourly_rate": 180.0,
                "bio": "Specializing in portraits and corporate events.",
                "portfolio": [
                    {"url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&h=600&fit=crop", "caption": "Professional Portrait"},
                    {"url": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800&h=600&fit=crop", "caption": "Corporate Event"},
                    {"url": "https://images.unsplash.com/photo-1522556189639-b150ed9c4330?w=800&h=600&fit=crop", "caption": "Headshot"},
                ]
            },
            {
                "user_id": 8,
                "first_name": "Carol",
                "last_name": "Williams",
                "email": "carol.photo@example.com",
                "phone": "9876543213",
                "specialty": "Birthday & Baby Showers",
                "hourly_rate": 150.0,
                "bio": "Fun and creative photographer for birthdays and baby showers.",
                "portfolio": [
                    {"url": "https://images.unsplash.com/photo-1530103862676-de3c9ef59af2?w=800&h=600&fit=crop", "caption": "Birthday Celebration"},
                    {"url": "https://images.unsplash.com/photo-1519817914152-22d216bb9170?w=800&h=600&fit=crop", "caption": "Baby Shower"},
                    {"url": "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800&h=600&fit=crop", "caption": "Party Fun"},
                ]
            }
        ]
        
        for pdata in photographers_data:
            # Check if user exists
            user = User.query.get(pdata["user_id"])
            if not user:
                # Create user
                user = User(
                    id=pdata["user_id"],
                    first_name=pdata["first_name"],
                    last_name=pdata["last_name"],
                    email=pdata["email"],
                    phone=pdata["phone"],
                    user_type="photographer"
                )
                user.set_password("photo123")
                db.session.add(user)
                print(f"Created user: {pdata['first_name']} {pdata['last_name']}")
            
            # Check if photographer exists
            photographer = Photographer.query.filter_by(user_id=pdata["user_id"]).first()
            if not photographer:
                # Create photographer
                photographer = Photographer(
                    user_id=pdata["user_id"],
                    specialty=pdata["specialty"],
                    hourly_rate=pdata["hourly_rate"],
                    bio=pdata["bio"],
                    is_available=True
                )
                db.session.add(photographer)
                db.session.flush()  # Get the photographer ID
                print(f"Created photographer profile for {pdata['first_name']}")
            else:
                print(f"Photographer already exists for {pdata['first_name']}")
            
            # Check if portfolio exists for this photographer
            existing_portfolio = PortfolioItem.query.filter_by(photographer_id=photographer.id).all()
            if not existing_portfolio:
                # Add portfolio items
                for img in pdata["portfolio"]:
                    item = PortfolioItem(
                        photographer_id=photographer.id,
                        image_url=img["url"],
                        caption=img["caption"]
                    )
                    db.session.add(item)
                print(f"Added {len(pdata['portfolio'])} portfolio items for {pdata['first_name']}")
        
        db.session.commit()
        print("\nDone! Photographers restored.")

if __name__ == "__main__":
    restore_photographers()
