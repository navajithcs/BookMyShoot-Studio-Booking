import sys
sys.path.insert(0, '.')

from app import app, db, Photographer

with app.app_context():
    photographers = Photographer.query.all()
    print('Total photographers:', len(photographers))
    for p in photographers:
        print(f'ID: {p.id}, Available: {p.is_available}, Location: {p.location}, Specialty: {p.specialty}')
    
    # Also check available photographers
    available = Photographer.query.filter_by(is_available=True).all()
    print(f'\nAvailable photographers: {len(available)}')
    for p in available:
        print(f'ID: {p.id}, Location: {p.location}, Specialty: {p.specialty}')
