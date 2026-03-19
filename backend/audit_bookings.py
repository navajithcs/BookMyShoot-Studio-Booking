
from app import app, db
from models import Booking, Photographer, User

with app.app_context():
    bookings = Booking.query.all()
    print(f"Total Bookings: {len(bookings)}")
    for b in bookings:
        photog = Photographer.query.get(b.photographer_id)
        photog_name = f"{photog.user.first_name} {photog.user.last_name}" if photog and photog.user else "Unknown"
        print(f"ID={b.id}, Status={b.status}, PhotogID={b.photographer_id} ({photog_name})")
