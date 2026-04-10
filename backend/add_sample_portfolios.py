#!/usr/bin/env python3
"""Add sample portfolio images for all photographers"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Photographer, PortfolioItem

# Sample portfolio images (using Unsplash URLs - public domain)
SAMPLE_IMAGES = [
    {
        "url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&h=600&fit=crop",
        "caption": "Wedding Ceremony"
    },
    {
        "url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=800&h=600&fit=crop",
        "caption": "Romantic Portrait"
    },
    {
        "url": "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800&h=600&fit=crop",
        "caption": "Event Coverage"
    },
    {
        "url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&h=600&fit=crop",
        "caption": "Engagement Shoot"
    },
    {
        "url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&h=600&fit=crop",
        "caption": "Studio Portrait"
    },
    {
        "url": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800&h=600&fit=crop",
        "caption": "Fashion Shoot"
    }
]

# Different images for each photographer to make them unique
PHOTOGRAPHER_IMAGES = {
    1: [  # John Doe - Wedding & Events
        {"url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&h=600&fit=crop", "caption": "Wedding Ceremony"},
        {"url": "https://images.unsplash.com/photo-1519741497674-611481863552?w=800&h=600&fit=crop", "caption": "Couple Portrait"},
        {"url": "https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?w=800&h=600&fit=crop", "caption": "Engagement"},
    ],
    2: [  # Alice Smith - Wedding Photography
        {"url": "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=800&h=600&fit=crop", "caption": "Wedding Party"},
        {"url": "https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=800&h=600&fit=crop", "caption": "First Dance"},
        {"url": "https://images.unsplash.com/photo-1507504036103?w=800&h=600&fit=crop", "caption": "Ceremony"},
    ],
    3: [  # Bob Johnson - Portrait & Events
        {"url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&h=600&fit=crop", "caption": "Professional Portrait"},
        {"url": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800&h=600&fit=crop", "caption": "Corporate Event"},
        {"url": "https://images.unsplash.com/photo-1522556189639-b150ed9c4330?w=800&h=600&fit=crop", "caption": "Headshot"},
    ],
    4: [  # Carol Williams - Birthday & Baby Showers
        {"url": "https://images.unsplash.com/photo-1530103862676-de3c9ef59af2?w=800&h=600&fit=crop", "caption": "Birthday Celebration"},
        {"url": "https://images.unsplash.com/photo-1519817914152-22d216bb9170?w=800&h=600&fit=crop", "caption": "Baby Shower"},
        {"url": "https://images.unsplash.com/photo-1464349095431-e9a21285b5f3?w=800&h=600&fit=crop", "caption": "Party Fun"},
    ]
}

def add_portfolios():
    with app.app_context():
        # Get all photographers
        photographers = Photographer.query.all()
        
        print(f"Found {len(photographers)} photographers")
        
        for photographer in photographers:
            print(f"\nProcessing photographer {photographer.id}: {photographer.user.first_name if photographer.user else 'Unknown'}")
            
            # Check if photographer already has portfolio
            if photographer.portfolio:
                print(f"  - Already has {len(photographer.portfolio)} portfolio items, skipping...")
                continue
            
            # Get images for this photographer
            images = PHOTOGRAPHER_IMAGES.get(photographer.id, SAMPLE_IMAGES)
            
            for img_data in images:
                # We'll use external URLs directly instead of downloading
                # The frontend will display these URLs
                item = PortfolioItem(
                    photographer_id=photographer.id,
                    image_url=img_data["url"],  # Using external URL directly
                    caption=img_data["caption"]
                )
                db.session.add(item)
                print(f"  + Added: {img_data['caption']}")
        
        db.session.commit()
        print("\n✅ Sample portfolios added successfully!")

if __name__ == "__main__":
    add_portfolios()
