
from app import app, db
from models import Booking, RefundRequest, Payment
from flask import Flask, request
import json

def simulate_check(booking_id, photographer_id):
    with app.app_context():
        # This simulates the logic in check_cancellation_eligibility
        print(f"Checking Booking #{booking_id} for Photographer #{photographer_id}")
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return {"error": "Booking not found"}, 404

        if booking.photographer_id != photographer_id:
            return {"error": "Unauthorized", "booking_p_id": booking.photographer_id, "sent_p_id": photographer_id}, 403

        can_cancel = True
        reason = ''

        # Only accepted or token_paid bookings can be cancelled
        if booking.status not in ('accepted', 'token_paid'):
            can_cancel = False
            reason = f'Booking status is {booking.status}'

        # Prevent duplicate cancellation
        if can_cancel:
            existing_refund = RefundRequest.query.filter_by(booking_id=booking_id, cancelled_by='photographer').first()
            if existing_refund:
                can_cancel = False
                reason = 'This booking has already been cancelled by you.'

        # Calculate paid amount for display
        paid_amount = 0
        token_payment = Payment.query.filter_by(
            booking_id=booking_id,
            payment_type='token'
        ).order_by(Payment.created_at.desc()).first()

        if booking.payment_status in ('token_paid', 'paid'):
            paid_amount = booking.token_amount or (token_payment.amount if token_payment else 0)

        return {
            'can_cancel': can_cancel,
            'reason': reason,
            'paid_amount': paid_amount,
            'payment_status': booking.payment_status
        }, 200

if __name__ == "__main__":
    result, status_code = simulate_check(41, 3)
    print(f"Status Code: {status_code}")
    print(f"Response: {json.dumps(result, indent=2)}")
