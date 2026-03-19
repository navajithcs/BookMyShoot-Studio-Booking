
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app import app, db
from models import User, Photographer

def diagnose():
    print("Starting Photographer Diagnosis...")
    with app.app_context():
        photographers = Photographer.query.all()
        print(f"Total Photographers: {len(photographers)}")
        
        broken_photographers = []
        for p in photographers:
            if not p.user:
                print(f"!!! Error: Photographer ID {p.id} has no associated User (user_id={p.user_id})")
                broken_photographers.append(p)
            else:
                try:
                    p.to_dict()
                except Exception as e:
                    print(f"!!! Error: Photographer ID {p.id} failed to_dict: {e}")
                    broken_photographers.append(p)
        
        if not broken_photographers:
            print("No broken photographers found in the database.")
        else:
            print(f"Found {len(broken_photographers)} broken photographer records.")

if __name__ == "__main__":
    diagnose()
