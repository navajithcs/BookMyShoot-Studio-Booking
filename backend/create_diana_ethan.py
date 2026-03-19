from models import db, User, Photographer
from app import app

photographers_data = [
    {
        'email': 'diana.flash@bookmyshoot.com',
        'password': 'Diana@Flash2026',
        'first_name': 'Diana',
        'last_name': 'Flash',
        'phone': '9876543220',
        'specialty': 'Wedding & Engagement',
        'hourly_rate': 220.0,
        'bio': 'Passionate wedding and engagement photographer with an eye for golden hour moments.',
        'location': 'Chennai'
    },
    {
        'email': 'ethan.focus@bookmyshoot.com',
        'password': 'Ethan@Focus2026',
        'first_name': 'Ethan',
        'last_name': 'Focus',
        'phone': '9876543221',
        'specialty': 'Portrait & Studio',
        'hourly_rate': 190.0,
        'bio': 'Creative portrait and studio photographer delivering sharp, stunning results.',
        'location': 'Mumbai'
    }
]

with app.app_context():
    created_count = 0

    for data in photographers_data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            print(f"User {data['email']} already exists. Skipping...")
            continue

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

        photographer = Photographer(
            user_id=user.id,
            specialty=data['specialty'],
            hourly_rate=data['hourly_rate'],
            bio=data['bio'],
            location=data['location'],
            is_available=True
        )
        db.session.add(photographer)
        db.session.commit()
        print(f"Photographer profile created for {data['email']}")
        created_count += 1

    print(f"\n=== Successfully created {created_count} photographer(s) ===")
    print("\nLogin credentials:")
    for data in photographers_data:
        print(f"  Name:     {data['first_name']} {data['last_name']}")
        print(f"  Email:    {data['email']}")
        print(f"  Password: {data['password']}")
        print()
