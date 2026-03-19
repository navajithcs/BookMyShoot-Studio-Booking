import sys
sys.path.insert(0, '.')

from app import app, db, Photographer

with app.app_context():
    # Update photographers with more searchable specialties
    photographers = Photographer.query.all()
    
    for p in photographers:
        if p.id == 3:
            p.specialty = 'Studio,Portrait,Events'
        elif p.id == 4:
            p.specialty = 'Birthday,Baby Shower,Events'
        elif p.id == 5:
            p.specialty = 'Wedding,Engagement,Events'
        elif p.id == 6:
            p.specialty = 'Wedding,Photography,Events'
        print(f'Updated photographer {p.id}: specialty={p.specialty}')
    
    db.session.commit()
    print('\nSpecialties updated successfully!')
    
    # Verify
    for p in Photographer.query.all():
        print(f'ID: {p.id}, Location: {p.location}, Specialty: {p.specialty}')
