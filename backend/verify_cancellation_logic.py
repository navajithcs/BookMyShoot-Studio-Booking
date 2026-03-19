
from app import app, db
from models import Booking, RefundRequest, Payment
import json

def test_api_logic():
    with app.app_context():
        # Case 1: Matching photographer (Jazim - #3, Booking #41)
        booking_id = 41
        photographer_id = 3
        
        print(f"--- Testing Match: Booking #{booking_id}, Photographer #{photographer_id} ---")
        booking = Booking.query.get(booking_id)
        if booking:
            print(f"Booking Status: {booking.status}, PhotogID: {booking.photographer_id}")
            
            # Simulate the updated check_cancellation_eligibility logic
            if booking.photographer_id != photographer_id:
                result = {'can_cancel': False, 'reason': 'Unauthorized'}
            elif booking.status not in ('accepted', 'token_paid'):
                result = {'can_cancel': False, 'reason': f'Status {booking.status}'}
            else:
                result = {'can_cancel': True, 'reason': ''}
            print(f"Result: {json.dumps(result)}")

        # Case 2: Mismatching photographer (Unauthorized)
        wrong_photog_id = 999
        print(f"\n--- Testing Mismatch: Booking #{booking_id}, Photographer #{wrong_photog_id} ---")
        if booking.photographer_id != wrong_photog_id:
            result = {
                'can_cancel': False,
                'reason': 'Unauthorized — this booking is not assigned to you.',
                'error': 'Unauthorized'
            }
        print(f"Result: {json.dumps(result)}")

        # Case 3: Invalid status (Completed booking #5)
        booking_id_c = 5
        booking_c = Booking.query.get(booking_id_c)
        if booking_c:
             print(f"\n--- Testing Invalid Status: Booking #{booking_id_c}, Photographer #{booking_c.photographer_id} ---")
             if booking_c.status not in ('accepted', 'token_paid'):
                 result = {
                     'can_cancel': False,
                     'reason': f'Booking status is "{booking_c.status}". Only accepted or token-paid sessions can be cancelled.'
                 }
             print(f"Result: {json.dumps(result)}")

if __name__ == "__main__":
    test_api_logic()
