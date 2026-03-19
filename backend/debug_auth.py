from app import app, db, User
from werkzeug.security import check_password_hash, generate_password_hash

def debug_auth(email, password):
    with app.app_context():
        print(f"--- Debugging Auth for {email} ---")
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print("User NOT FOUND")
            return

        print(f"User Found: ID={user.id}, Email={user.email}")
        print(f"Stored Hash: {user.password_hash}")
        
        # Test 1: Check using model method
        result_model = user.check_password(password)
        print(f"Model check_password('{password}'): {result_model}")
        
        # Test 2: Check using werkzeug directly
        result_direct = check_password_hash(user.password_hash, password)
        print(f"Direct check_password_hash: {result_direct}")
        
        # Test 3: Generate new hash and check
        new_hash = generate_password_hash(password)
        print(f"New Hash generation: {new_hash}")
        print(f"Check against new hash: {check_password_hash(new_hash, password)}")

if __name__ == "__main__":
    debug_auth("admin@bookmyshoot.com", "Admin123")
    print("\n")
    debug_auth("new_admin@bookmyshoot.com", "NewAdmin123")
