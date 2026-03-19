"""
Seed the service_packages table with the current hardcoded website packages.
Run once: python seed_service_packages.py
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from models import ServicePackage

PACKAGES = [
    # ── Wedding ──
    {"service_type": "wedding", "name": "Essential", "price": 25000, "is_featured": False, "sort_order": 1,
     "features": ["4 Hours Coverage", "1 Photographer", "200+ Edited Photos", "Online Gallery", "Delivery in 7 Days"]},
    {"service_type": "wedding", "name": "Premium", "price": 45000, "is_featured": True, "sort_order": 2,
     "features": ["8 Hours Coverage", "2 Photographers", "500+ Edited Photos", "Photo Album", "Drone Photography", "Delivery in 5 Days"]},
    {"service_type": "wedding", "name": "Luxury", "price": 75000, "is_featured": False, "sort_order": 3,
     "features": ["Full Day Coverage", "2 Photographers + Videographer", "1000+ Edited Photos", "Premium Photo Album", "Drone + Cinematography", "Same Day Preview"]},

    # ── Engagement ──
    {"service_type": "engagement", "name": "Basic", "price": 8000, "is_featured": False, "sort_order": 1,
     "features": ["2 Hours Session", "1 Location", "50 Edited Photos", "Online Gallery"]},
    {"service_type": "engagement", "name": "Premium", "price": 15000, "is_featured": True, "sort_order": 2,
     "features": ["4 Hours Session", "2 Locations", "100 Edited Photos", "Photo Print", "Makeup Artist"]},
    {"service_type": "engagement", "name": "Complete", "price": 25000, "is_featured": False, "sort_order": 3,
     "features": ["Full Day Session", "Unlimited Locations", "200 Edited Photos", "Premium Album", "Video Coverage"]},

    # ── Birthday ──
    {"service_type": "birthday", "name": "Small Party", "price": 5000, "is_featured": False, "sort_order": 1,
     "features": ["2 Hours Coverage", "1 Photographer", "100 Edited Photos", "Online Gallery"]},
    {"service_type": "birthday", "name": "Big Bash", "price": 12000, "is_featured": True, "sort_order": 2,
     "features": ["4 Hours Coverage", "1 Photographer", "250 Edited Photos", "Photo Prints", "Cake Cutting Video"]},
    {"service_type": "birthday", "name": "Grand Party", "price": 20000, "is_featured": False, "sort_order": 3,
     "features": ["Full Day Coverage", "2 Photographers", "500+ Edited Photos", "Premium Album", "Video Coverage"]},

    # ── Baby Shower ──
    {"service_type": "babyshower", "name": "Basic", "price": 6000, "is_featured": False, "sort_order": 1,
     "features": ["2 Hours Coverage", "1 Photographer", "75 Edited Photos", "Online Gallery"]},
    {"service_type": "babyshower", "name": "Complete", "price": 12000, "is_featured": True, "sort_order": 2,
     "features": ["4 Hours Coverage", "1 Photographer", "150 Edited Photos", "Photo Prints", "Video Highlights"]},
    {"service_type": "babyshower", "name": "Grand", "price": 18000, "is_featured": False, "sort_order": 3,
     "features": ["Full Day Coverage", "2 Photographers", "300 Edited Photos", "Premium Album", "Full Video Coverage"]},

    # ── Naming Ceremony ──
    {"service_type": "naming", "name": "Basic", "price": 5000, "is_featured": False, "sort_order": 1,
     "features": ["2 Hours Coverage", "50 Edited Photos", "Online Gallery"]},
    {"service_type": "naming", "name": "Premium", "price": 10000, "is_featured": True, "sort_order": 2,
     "features": ["4 Hours Coverage", "100 Edited Photos", "Photo Prints", "Video Highlights"]},
    {"service_type": "naming", "name": "Complete", "price": 15000, "is_featured": False, "sort_order": 3,
     "features": ["Full Day Coverage", "200 Edited Photos", "Premium Album", "Full Video"]},

    # ── Studio ──
    {"service_type": "studio", "name": "Quick", "price": 2000, "is_featured": False, "sort_order": 1,
     "features": ["30 Mins Session", "10 Edited Photos", "Online Gallery"]},
    {"service_type": "studio", "name": "Standard", "price": 5000, "is_featured": True, "sort_order": 2,
     "features": ["1 Hour Session", "25 Edited Photos", "Multiple Outfits", "2 Backgrounds"]},
    {"service_type": "studio", "name": "Premium", "price": 10000, "is_featured": False, "sort_order": 3,
     "features": ["2 Hour Session", "50 Edited Photos", "Unlimited Outfits", "All Backgrounds", "Makeup Artist"]},
]

def seed():
    with app.app_context():
        db.create_all()
        existing = ServicePackage.query.count()
        if existing > 0:
            print(f"⚠️  service_packages table already has {existing} rows. Skipping seed.")
            return
        for pkg_data in PACKAGES:
            pkg = ServicePackage(
                service_type=pkg_data["service_type"],
                name=pkg_data["name"],
                price=pkg_data["price"],
                features=json.dumps(pkg_data["features"]),
                is_featured=pkg_data["is_featured"],
                sort_order=pkg_data["sort_order"]
            )
            db.session.add(pkg)
        db.session.commit()
        print(f"✅ Seeded {len(PACKAGES)} service packages successfully!")

if __name__ == "__main__":
    seed()
