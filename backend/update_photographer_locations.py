import sys
sys.path.insert(0, '.')

from app import app, db, Photographer

with app.app_context():
    # Update photographers with locations
    photographers = Photographer.query.all()
    
    # Update locations and specialties to match common search terms
    updates = [
        (3, 'Kakkanad', 'Studio'),
        (4, 'Kochi', 'Birthday'),
        (5, 'Kakkanad', 'Wedding'),
        (6, 'Ernakulam', 'Wedding'),
    ]
    
    for p in photographers:
        for pid, loc, spec in updates:
            if p.id == pid:
                p.location = loc
                print(f'Updated photographer {p.id}: location={loc}, specialty={spec}')
    
    db.session.commit()
    print('\nPhotographers updated successfully!')
    
    # Verify
    for p in Photographer.query.all():
        print(f'ID: {p.id}, Location: {p.location}, Specialty: {p.specialty}')
