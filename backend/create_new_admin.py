import sys
from app import app, db, User

def create_admin(email, password):
    with app.app_context():
        if User.query.filter_by(email=email).first():
            print(f"User {email} already exists.")
            return

        u = User(
            first_name='New', 
            last_name='Admin', 
            email=email, 
            user_type='admin', 
            phone='9999999999'
        )
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        print(f"Successfully created new admin user:")
        print(f"Email: {email}")
        print(f"Password: {password}")

if __name__ == "__main__":
    email = "new_admin@bookmyshoot.com"
    password = "NewPassword123"
    
    if len(sys.argv) > 2:
        email = sys.argv[1]
        password = sys.argv[2]
        
    create_admin(email, password)
