from app import app, db, User

with app.app_context():
    users = User.query.all()
    print("\n" + "="*70)
    print("ALL REGISTERED USERS")
    print("="*70)
    for u in users:
        print(f"ID: {u.id}")
        print(f"  Email:    {u.email}")
        print(f"  Type:     {u.user_type}")
        print(f"  Name:     {u.first_name} {u.last_name}")
        print(f"  Phone:    {u.phone}")
        print(f"  Active:   {u.is_active}")
        print("-"*40)
    print(f"\nTotal users: {len(users)}")
