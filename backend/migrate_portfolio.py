"""Add category column to portfolio_items table"""
from app import app, db
from sqlalchemy import inspect, text

with app.app_context():
    inspector = inspect(db.engine)
    cols = [c['name'] for c in inspector.get_columns('portfolio_items')]
    if 'category' not in cols:
        db.session.execute(text('ALTER TABLE portfolio_items ADD COLUMN category VARCHAR(50) DEFAULT "General"'))
        db.session.commit()
        print('Added category column to portfolio_items')
    else:
        print('category column already exists')
