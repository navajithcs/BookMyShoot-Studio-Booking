from models import db, User, Photographer
from app import app

photographers_data = [
    {
        "email": "alice@example.com",
        "password": "Password123",
        "first": "Alice",
        "last": "Lens",
        "phone": "1111111111",
        "specialty": "Wedding",
        "rate": 150.0,
        "bio": "Expert wedding photographer capturing your special moments."
    },
    {
        "email": "bob@example.com",
        "password": "Password123",
        "first": "Bob",
        "last": "Shutter",
        "phone": "2222222222",
        "specialty": "Portrait",
        "rate": 100.0,
        "bio": "Portrait specialist with a knack for lighting."
    },
    {
        "email": "charlie@example.com",
        "password": "Password123",
        "first": "Charlie",
        "last": "Frame",
        "phone": "3333333333",
        "specialty": "Fashion",
        "rate": 250.0,
        "bio": "High-end fashion photography and editorial shoots."
    }
]

with app.app_context():
    for data in photographers_data:
        # check if user exists
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            print(f"User {data['email']} already exists.")
            # Check if they have a photographer profile
            if existing_user.user_type == 'photographer':
                existing_profile = Photographer.query.filter_by(user_id=existing_user.id).first()
                if not existing_profile:
                     print(f"Creating missing profile for {data['email']}")
                     photographer = Photographer(
                        user_id=existing_user.id,
                        specialty=data["specialty"],
                        hourly_rate=data["rate"],
                        bio=data["bio"]
                    )
                     db.session.add(photographer)
                     db.session.commit()
            else:
                print(f"User {data['email']} exists but is not a photographer. Skipping.")
            continue
        
        # Create User
        user = User(
            first_name=data["first"],
            last_name=data["last"],
            email=data["email"],
            phone=data["phone"],
            user_type='photographer'
        )
        user.set_password(data["password"])
        db.session.add(user)
        db.session.commit()
        print(f"User created: {data['email']}")

        # Create Photographer Profile
        photographer = Photographer(
            user_id=user.id,
            specialty=data["specialty"],
            hourly_rate=data["rate"],
            bio=data["bio"]
        )
        db.session.add(photographer)
        db.session.commit()
        print(f"Photographer profile created for {data['email']}")

print("Finished creating photographers.")
