from models import db, User
from config import DATABASE_URI
from app import app

# Change these values as needed
EMAIL = 'navajith78@gmail.com'
FIRST = 'navajith'
LAST = 'cs'
PASSWORD = 'Password123'
PHONE = '1234567890'
USERTYPE = 'customer'

with app.app_context():
    if User.query.filter_by(email=EMAIL).first():
        print('User already exists:', EMAIL)
    else:
        user = User(first_name=FIRST, last_name=LAST, email=EMAIL, phone=PHONE, user_type=USERTYPE)
        user.set_password(PASSWORD)
        db.session.add(user)
        db.session.commit()
        print('User created:', EMAIL)
