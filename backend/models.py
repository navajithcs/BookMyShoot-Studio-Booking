from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.String(20), nullable=False, default='customer')
    password_hash = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='customer', lazy=True, foreign_keys='Booking.customer_id',
                               cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    activities = db.relationship('ActivityLog', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'user_type': self.user_type,
            'profile_image': self.profile_image,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class Photographer(db.Model):
    __tablename__ = 'photographers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialty = db.Column(db.String(100), nullable=True)  # wedding, portrait, event, etc.
    hourly_rate = db.Column(db.Float, default=0)
    experience = db.Column(db.String(50), nullable=True)  # e.g., '5+ years'
    bio = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)  # City/location for search
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to user
    user = db.relationship('User', backref='photographer_profile')
    bookings = db.relationship('Booking', backref='photographer', lazy=True, cascade='all, delete-orphan')
    packages = db.relationship('Package', backref='photographer', lazy=True, cascade='all, delete-orphan')
    portfolio = db.relationship('PortfolioItem', backref='photographer', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'specialty': self.specialty,
            'hourly_rate': self.hourly_rate,
            'experience': self.experience,
            'bio': self.bio,
            'location': self.location,
            'is_available': self.is_available,
            'portfolio': [p.to_dict() for p in self.portfolio] if self.portfolio else [],
            'packages': [p.to_dict() for p in self.packages] if self.packages else [],
            'user': self.user.to_dict() if self.user else None
        }


class Package(db.Model):
    __tablename__ = 'packages'
    
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographers.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('event_categories.id'), nullable=True)
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    category = db.relationship('EventCategory', backref='packages')
    
    def to_dict(self):
        return {
            'id': self.id,
            'photographer_id': self.photographer_id,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else 'General',
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'
    
    id = db.Column(db.Integer, primary_key=True)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographers.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True, default='General')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    CATEGORIES = ['Wedding', 'Portrait', 'Event', 'Nature', 'Fashion', 'Product', 'Architecture', 'Street', 'Food', 'Other']
    
    def to_dict(self):
        return {
            'id': self.id,
            'photographer_id': self.photographer_id,
            'image_url': self.image_url,
            'caption': self.caption,
            'category': self.category or 'General',
            'created_at': self.created_at.isoformat()
        }


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographers.id'), nullable=True)
    
    # Service details
    service_type = db.Column(db.String(50), nullable=False)  # wedding, engagement, birthday, etc.
    package_name = db.Column(db.String(100), nullable=True)  # Basic, Standard, Premium etc.
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    location_type = db.Column(db.String(50), nullable=True)  # indoor, outdoor, studio, destination
    address_line = db.Column(db.String(500), nullable=True)
    pincode = db.Column(db.String(10), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True, default='India')
    contact_number = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Pricing
    total_price = db.Column(db.Float, nullable=False)
    token_amount = db.Column(db.Float, default=0)
    remaining_amount = db.Column(db.Float, default=0)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, accepted, declined, completed, cancelled
    payment_status = db.Column(db.String(20), default='pending')  # pending, token_paid, paid, refunded
    cancelled_by = db.Column(db.String(20), nullable=True)  # 'photographer', 'customer', or None
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        booking_status_label = self.status.title() if self.status else 'Unknown'
        if self.status == 'cancelled' and self.cancelled_by == 'photographer':
            booking_status_label = 'Cancelled by Photographer'

        refund_status_label = 'Refund Pending'
        if self.payment_status == 'refunded':
            refund_status_label = 'Refund Completed'
        elif self.payment_status in ('token_paid', 'paid'):
            refund_status_label = 'Not Refunded'

        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'photographer_id': self.photographer_id,
            'service_type': self.service_type,
            'package_name': self.package_name,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'event_time': self.event_time,
            'location': self.location,
            'location_type': self.location_type,
            'address_line': self.address_line,
            'pincode': self.pincode,
            'state': self.state,
            'country': self.country,
            'contact_number': self.contact_number,
            'notes': self.notes,
            'total_price': self.total_price,
            'token_amount': self.token_amount,
            'remaining_amount': self.remaining_amount,
            'status': self.status,
            'booking_status_label': booking_status_label,
            'payment_status': self.payment_status,
            'refund_status_label': refund_status_label,
            'cancelled_by': self.cancelled_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'customer': self.customer.to_dict() if self.customer else None,
            'photographer': self.photographer.to_dict() if self.photographer else None,
            'refund_request': self.refund_requests[0].to_dict() if self.refund_requests else None,
            'refund_transaction': self.refund_transactions[0].to_dict() if self.refund_transactions else None
        }
    
    def __repr__(self):
        return f'<Booking {self.id} - {self.service_type}>'


class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographers.id'), nullable=True)
    
    # Payment details
    amount = db.Column(db.Float, nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)  # token, remaining, full
    payment_method = db.Column(db.String(50), nullable=True)  # card, upi, netbanking, etc.
    transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed, refunded
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    booking = db.relationship('Booking', backref='payments')
    customer = db.relationship('User', backref='payments', foreign_keys=[customer_id])
    refunds = db.relationship('RefundTransaction', backref='payment', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'customer_id': self.customer_id,
            'photographer_id': self.photographer_id,
            'amount': self.amount,
            'payment_type': self.payment_type,
            'payment_method': self.payment_method,
            'transaction_id': self.transaction_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Payment {self.id} - ₹{self.amount}>'


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # backref 'user' defined on User model
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_email': self.user.email if self.user else 'System/Deleted',
            'action': self.action,
            'details': self.details,
            'timestamp': self.timestamp.isoformat()
        }


class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=True)
    
    # Notification details
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # job_accepted, job_declined, payment_received, etc.
    is_read = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships (backref on User model)
    booking = db.relationship('Booking', backref='notifications')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'booking_id': self.booking_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    def __repr__(self):
        return f'<Notification {self.id} - {self.notification_type}>'

class EventCategory(db.Model):
    __tablename__ = 'event_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<EventCategory {self.name}>'


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name or '',
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<ContactMessage {self.id} from {self.email}>'


class ServicePackage(db.Model):
    """Website-level service packages displayed on service pages (managed by admin)"""
    __tablename__ = 'service_packages'

    id = db.Column(db.Integer, primary_key=True)
    service_type = db.Column(db.String(50), nullable=False)  # wedding, engagement, birthday, babyshower, naming, studio
    name = db.Column(db.String(100), nullable=False)  # Basic, Premium, Complete, etc.
    price = db.Column(db.Float, nullable=False)
    features = db.Column(db.Text, nullable=True)  # JSON array of feature strings
    is_featured = db.Column(db.Boolean, default=False)  # Highlighted/gradient card
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'service_type': self.service_type,
            'name': self.name,
            'price': self.price,
            'features': json.loads(self.features) if self.features else [],
            'is_featured': self.is_featured,
            'sort_order': self.sort_order,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<ServicePackage {self.service_type} - {self.name} ₹{self.price}>'


class Feedback(db.Model):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photographer_id = db.Column(db.Integer, db.ForeignKey('photographers.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship('Booking', backref='feedbacks')
    customer = db.relationship('User', backref='feedbacks', foreign_keys=[customer_id])
    photographer = db.relationship('Photographer', backref='feedbacks')

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'customer_id': self.customer_id,
            'photographer_id': self.photographer_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<Feedback {self.id} - {self.rating} stars>'


class RefundTransaction(db.Model):
    __tablename__ = 'refunds'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False, index=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    refund_status = db.Column(db.String(20), default='refunded')  # pending, refunded, failed
    refund_date = db.Column(db.DateTime, default=datetime.utcnow)
    gateway = db.Column(db.String(30), default='razorpay')
    gateway_payment_id = db.Column(db.String(100), nullable=True)
    gateway_refund_id = db.Column(db.String(100), unique=True, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    booking = db.relationship('Booking', backref='refund_transactions')

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'payment_id': self.payment_id,
            'amount': self.amount,
            'refund_status': self.refund_status,
            'refund_date': self.refund_date.isoformat() if self.refund_date else None,
            'gateway': self.gateway,
            'gateway_payment_id': self.gateway_payment_id,
            'gateway_refund_id': self.gateway_refund_id,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    def __repr__(self):
        return f'<RefundTransaction {self.id} - ₹{self.amount}>'


class RefundRequest(db.Model):
    __tablename__ = 'refund_requests'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    refund_amount = db.Column(db.Float, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)
    # UPI and Receipt details
    upi_id = db.Column(db.String(100), nullable=True)
    upi_name = db.Column(db.String(100), nullable=True)
    receipt_number = db.Column(db.String(50), nullable=True)
    refund_method = db.Column(db.String(50), default='upi')  # upi, bank_transfer, razorpay
    # Photographer cancellation fields
    cancelled_by = db.Column(db.String(20), nullable=True)  # 'photographer' or 'customer'
    razorpay_payment_id = db.Column(db.String(100), nullable=True)
    razorpay_refund_id = db.Column(db.String(100), nullable=True)

    booking = db.relationship('Booking', backref='refund_requests')
    customer = db.relationship('User', backref='refund_requests', foreign_keys=[customer_id])

    def to_dict(self):
        return {
            'id': self.id,
            'booking_id': self.booking_id,
            'customer_id': self.customer_id,
            'refund_amount': self.refund_amount,
            'reason': self.reason,
            'status': self.status,
            'admin_notes': self.admin_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'upi_id': self.upi_id,
            'upi_name': self.upi_name,
            'receipt_number': self.receipt_number,
            'refund_method': self.refund_method,
            'cancelled_by': self.cancelled_by,
            'razorpay_payment_id': self.razorpay_payment_id,
            'razorpay_refund_id': self.razorpay_refund_id,
            'customer': self.customer.to_dict() if self.customer else None,
            'booking': {
                'id': self.booking.id,
                'service_type': self.booking.service_type,
                'event_date': self.booking.event_date.isoformat() if self.booking and self.booking.event_date else None,
                'total_price': self.booking.total_price if self.booking else 0,
                'status': self.booking.status if self.booking else None
            } if self.booking else None
        }

    def __repr__(self):
        return f'<RefundRequest {self.id} - {self.status}>'


class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    status = db.Column(db.String(20), default='open')  # open, in_progress, resolved, closed
    admin_reply = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = db.relationship('User', backref='support_tickets', foreign_keys=[customer_id])

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'subject': self.subject,
            'message': self.message,
            'priority': self.priority,
            'status': self.status,
            'admin_reply': self.admin_reply,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'customer': self.customer.to_dict() if self.customer else None
        }

    def __repr__(self):
        return f'<SupportTicket {self.id} - {self.status}>'
