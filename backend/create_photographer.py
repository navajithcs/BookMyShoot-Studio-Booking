from models import db, User, Photographer
from app import app

# Photographer Credentials
EMAIL = 'photo@example.com'
PASSWORD = 'Password123'
FIRST = 'John'
LAST = 'Doe'
PHONE = '9876543210'

# Photographer Profile Details
SPECIALTY = 'Wedding & Events'
HOURLY_RATE = 200.0
BIO = 'Professional photographer with 5 years of experience.'

with app.app_context():
    # check if user exists
    existing_user = User.query.filter_by(email=EMAIL).first()
    if existing_user:
        print(f"User {EMAIL} already exists.")
        if existing_user.user_type != 'photographer':
            print("User exists but is not a photographer.")
    else:
        # Create User
        user = User(
            first_name=FIRST,
            last_name=LAST,
            email=EMAIL,
            phone=PHONE,
            user_type='photographer'
        )
        user.set_password(PASSWORD)
        db.session.add(user)
        db.session.commit()
        print(f"User created: {EMAIL}")

        # Create Photographer Profile
        photographer = Photographer(
            user_id=user.id,
            specialty=SPECIALTY,
            hourly_rate=HOURLY_RATE,
            bio=BIO
        )
        db.session.add(photographer)
        db.session.commit()
        print(f"Photographer profile created for {EMAIL}")
