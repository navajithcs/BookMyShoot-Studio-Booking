"""Add cancellation-related columns to bookings and refund_requests tables"""
from app import app, db
from sqlalchemy import inspect, text

with app.app_context():
    inspector = inspect(db.engine)

    # Add cancelled_by to bookings
    booking_cols = [c['name'] for c in inspector.get_columns('bookings')]
    if 'cancelled_by' not in booking_cols:
        db.session.execute(text('ALTER TABLE bookings ADD COLUMN cancelled_by VARCHAR(20)'))
        print('Added cancelled_by column to bookings')
    else:
        print('cancelled_by column already exists in bookings')

    # Add columns to refund_requests
    refund_cols = [c['name'] for c in inspector.get_columns('refund_requests')]

    if 'cancelled_by' not in refund_cols:
        db.session.execute(text('ALTER TABLE refund_requests ADD COLUMN cancelled_by VARCHAR(20)'))
        print('Added cancelled_by column to refund_requests')
    else:
        print('cancelled_by column already exists in refund_requests')

    if 'razorpay_payment_id' not in refund_cols:
        db.session.execute(text('ALTER TABLE refund_requests ADD COLUMN razorpay_payment_id VARCHAR(100)'))
        print('Added razorpay_payment_id column to refund_requests')
    else:
        print('razorpay_payment_id column already exists in refund_requests')

    if 'razorpay_refund_id' not in refund_cols:
        db.session.execute(text('ALTER TABLE refund_requests ADD COLUMN razorpay_refund_id VARCHAR(100)'))
        print('Added razorpay_refund_id column to refund_requests')
    else:
        print('razorpay_refund_id column already exists in refund_requests')

    db.session.commit()
    print('Migration complete!')
