from app import app, db, User

def reset_admin_password():
    with app.app_context():
        admin = User.query.filter_by(email='admin@bookmyshoot.com').first()
        if not admin:
            print("Admin user not found! Use create_admin.py first.")
            return

        print(f"Found admin user: {admin.email}")
        admin.set_password('Admin123')
        db.session.commit()
        print("Password reset successfully to: Admin123")

if __name__ == "__main__":
    reset_admin_password()
