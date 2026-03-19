from app import app, db, User

def create_admin():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@bookmyshoot.com').first()
        if admin:
            print("Admin user already exists.")
            return

        # Create admin user
        admin = User(
            first_name='Admin',
            last_name='User',
            email='admin@bookmyshoot.com',
            user_type='admin',
            phone='0000000000'
        )
        admin.set_password('Admin123')  # Default password
        
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
        print("Email: admin@bookmyshoot.com")
        print("Password: Admin123")

if __name__ == "__main__":
    create_admin()
