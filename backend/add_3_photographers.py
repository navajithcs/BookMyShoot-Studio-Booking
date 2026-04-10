from models import db, User, Photographer
from app import app
import os

# Force the database to use the correct path (instance folder in project root)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/bookmyshoot.db'

# List of 3 new photographers to create
photographers_data = [
    {
        'email': 'alice.photo@example.com',
        'password': 'PhotoPass123',
        'first_name': 'Alice',
        'last_name': 'Smith',
        'phone': '9876543211',
        'specialty': 'Wedding Photography',
        'hourly_rate': 250.0,
        'bio': 'Experienced wedding photographer with 7 years in the industry.'
    },
    {
        'email': 'bob.photo@example.com',
        'password': 'PhotoPass456',
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'phone': '9876543212',
        'specialty': 'Portrait & Events',
        'hourly_rate': 180.0,
        'bio': 'Specializing in portraits and corporate events.'
    },
    {
        'email': 'carol.photo@example.com',
        'password': 'PhotoPass789',
        'first_name': 'Carol',
        'last_name': 'Williams',
        'phone': '9876543213',
        'specialty': 'Birthday & Baby Showers',
        'hourly_rate': 150.0,
        'bio': 'Fun and creative photographer for birthdays and baby showers.'
    }
]

with app.app_context():
    created_count = 0
    
    for data in photographers_data:
        # Check if user already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            print(f"User {data['email']} already exists. Skipping...")
            continue
        
        # Create User
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone'],
            user_type='photographer'
        )
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        print(f"User created: {data['email']}")
        
        # Create Photographer Profile
        photographer = Photographer(
            user_id=user.id,
            specialty=data['specialty'],
            hourly_rate=data['hourly_rate'],
            bio=data['bio']
        )
        db.session.add(photographer)
        db.session.commit()
        print(f"Photographer profile created for {data['email']}")
        created_count += 1
    
    print(f"\n=== Successfully created {created_count} photographer(s) ===")
    print("\nLogin credentials:")
    for data in photographers_data:
        print(f"  Email: {data['email']}")
        print(f"  Password: {data['password']}")
        print()
