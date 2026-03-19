from models import db, User, Photographer
from app import app

photographers_data = [
    {
        "email": "diana@example.com",
        "password": "Password123",
        "first": "Diana",
        "last": "Flash",
        "phone": "4444444444",
        "specialty": "Event",
        "rate": 180.0,
        "bio": "Experienced event photographer specializing in corporate events, parties, and live concerts. Capturing the energy of every moment."
    },
    {
        "email": "ethan@example.com",
        "password": "Password123",
        "first": "Ethan",
        "last": "Focus",
        "phone": "5555555555",
        "specialty": "Nature",
        "rate": 120.0,
        "bio": "Nature and landscape photographer with a passion for outdoor shoots, travel photography, and wildlife encounters."
    }
]

with app.app_context():
    for data in photographers_data:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            print(f"User {data['email']} already exists.")
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

print("Finished creating 2 new photographers.")
