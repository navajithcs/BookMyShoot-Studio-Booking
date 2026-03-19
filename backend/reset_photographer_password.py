from app import app, db
from models import User, Photographer

def reset_photographer(email, new_password):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"User {email} not found.")
            return False
        
        if user.user_type != 'photographer':
            print(f"User {email} is not a photographer (Type: {user.user_type}).")
            return False
        
        user.set_password(new_password)
        user.is_active = True
        
        # Ensure photographer profile exists
        profile = Photographer.query.filter_by(user_id=user.id).first()
        if not profile:
            print(f"Creating missing photographer profile for {email}...")
            profile = Photographer(user_id=user.id, specialty='General')
            db.session.add(profile)
            
        db.session.commit()
        print(f"Successfully reset password and ensured active status for {email}.")
        print(f"New password is: {new_password}")
        return True

if __name__ == "__main__":
    reset_photographer('photo@example.com', 'Password123')
