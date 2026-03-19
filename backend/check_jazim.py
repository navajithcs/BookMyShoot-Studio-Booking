
from app import app, db
from models import User, Photographer

with app.app_context():
    jazim = User.query.filter(User.first_name == 'Jazim').first()
    if jazim:
        print(f"User Jazim: ID={jazim.id}")
        photog = Photographer.query.filter_by(user_id=jazim.id).first()
        if photog:
            print(f"Photographer Jazim: ID={photog.id}")
        else:
            print("Jazim is not a photographer in the Photographer table.")
    else:
        print("User Jazim not found.")
