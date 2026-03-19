from app import app, db, User, Photographer

with app.app_context():
    print("--- USERS ---")
    users = User.query.all()
    for u in users:
        print(f"ID: {u.id}, Email: {u.email}, Type: {u.user_type}")

    print("\n--- PHOTOGRAPHERS ---")
    photographers = Photographer.query.all()
    for p in photographers:
        print(f"ID: {p.id}, UserID: {p.user_id}, Specialty: {p.specialty}")
