
from app import app, db
from models import Booking, RefundRequest, Payment

with app.app_context():
    booking_id = 41
    booking = Booking.query.get(booking_id)
    if not booking:
        print(f"Booking #{booking_id} not found.")
    else:
        print(f"Booking #{booking_id}:")
        print(f"  Status: {booking.status}")
        print(f"  Photographer ID: {booking.photographer_id}")
        print(f"  Customer ID: {booking.customer_id}")
        print(f"  Payment Status: {booking.payment_status}")
        print(f"  Token Amount: {booking.token_amount}")
        print(f"  Event Date: {booking.event_date}")
        
        refunds = RefundRequest.query.filter_by(booking_id=booking_id).all()
        print(f"  Refund Requests: {len(refunds)}")
        for r in refunds:
            print(f"    - ID: {r.id}, Status: {r.status}, Cancelled By: {r.cancelled_by}")
            
        payments = Payment.query.filter_by(booking_id=booking_id).all()
        print(f"  Payments: {len(payments)}")
        for p in payments:
            print(f"    - ID: {p.id}, Type: {p.payment_type}, Status: {p.status}, Amount: {p.amount}")
