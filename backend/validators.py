"""
BookMyShoot — Server-Side Validation Module
Centralized input validation for all API endpoints
"""
import re
from datetime import datetime, date
from functools import wraps
from flask import request, jsonify

# ─── Regex Patterns ───
EMAIL_RE = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')
NAME_RE = re.compile(r"^[A-Za-z\s\-'.]+$")
PHONE_RE = re.compile(r'^\d{10}$')
TIME_RE = re.compile(r'^([01]?\d|2[0-3]):([0-5]\d)$')
TIME_RANGE_RE = re.compile(r'^([01]?\d|2[0-3]):([0-5]\d)\s*-\s*([01]?\d|2[0-3]):([0-5]\d)$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
PASSWORD_MIN = 8
PASSWORD_MAX = 128

# ─── Limits ───
MAX_NAME = 50
MAX_EMAIL = 100
MAX_PHONE = 15
MAX_BIO = 1000
MAX_NOTES = 500
MAX_MESSAGE = 2000
MAX_SUBJECT = 200
MAX_LOCATION = 200
VALID_USER_TYPES = {'customer', 'photographer'}
VALID_BOOKING_STATUSES = {'pending', 'accepted', 'declined', 'completed', 'token_paid', 'cancelled'}
VALID_SERVICE_TYPES = {'wedding', 'engagement', 'birthday', 'babyshower', 'naming', 'studio', 'portrait', 'events', 'other'}


def _strip(val):
    """Strip and clean a string value"""
    if val is None:
        return ''
    if isinstance(val, str):
        return val.strip()
    return str(val).strip()


def _sanitize_html(val):
    """Remove HTML tags to prevent XSS"""
    if not isinstance(val, str):
        return val
    return re.sub(r'<[^>]+>', '', val).strip()


def validate_name(value, field_label='Name', required=True):
    """Validate a name field"""
    v = _strip(value)
    if not v:
        return f'{field_label} is required' if required else None
    if len(v) < 2:
        return f'{field_label} must be at least 2 characters'
    if len(v) > MAX_NAME:
        return f'{field_label} must be under {MAX_NAME} characters'
    if not NAME_RE.match(v):
        return f'{field_label} can only contain letters, spaces, hyphens, and apostrophes'
    return None


def validate_email(value, required=True):
    """Validate email format"""
    v = _strip(value)
    if not v:
        return 'Email is required' if required else None
    if len(v) > MAX_EMAIL:
        return f'Email must be under {MAX_EMAIL} characters'
    if not EMAIL_RE.match(v):
        return 'Invalid email format'
    return None


def validate_phone(value, required=True):
    """Validate phone number (10 digits)"""
    v = _strip(value)
    if not v:
        return 'Phone number is required' if required else None
    digits = re.sub(r'\D', '', v)
    if len(digits) != 10:
        return 'Phone number must be exactly 10 digits'
    return None


def validate_password(value, field_label='Password'):
    """Validate password strength"""
    v = value or ''
    if not v:
        return f'{field_label} is required'
    if len(v) < PASSWORD_MIN:
        return f'{field_label} must be at least {PASSWORD_MIN} characters'
    if len(v) > PASSWORD_MAX:
        return f'{field_label} is too long'
    if not re.search(r'[a-z]', v):
        return f'{field_label} must include a lowercase letter'
    if not re.search(r'[A-Z]', v):
        return f'{field_label} must include an uppercase letter'
    if not re.search(r'\d', v):
        return f'{field_label} must include a number'
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', v):
        return f'{field_label} must include a special character (!@#$%...)'
    return None


def validate_date(value, field_label='Date', allow_past=False):
    """Validate date format and optionally reject past dates"""
    v = _strip(value)
    if not v:
        return f'{field_label} is required'
    if not DATE_RE.match(v):
        return f'{field_label} must be in YYYY-MM-DD format'
    try:
        d = datetime.strptime(v, '%Y-%m-%d').date()
    except ValueError:
        return f'{field_label} is not a valid date'
    if not allow_past and d < date.today():
        return f'{field_label} cannot be in the past'
    return None


def validate_time(value, field_label='Time', event_date=None):
    """Validate time format (HH:MM or HH:MM - HH:MM) and optionally reject past times"""
    v = _strip(value)
    if not v:
        return f'{field_label} is required'
    # Accept single time or time range
    range_match = TIME_RANGE_RE.match(v)
    single_match = TIME_RE.match(v)
    if not range_match and not single_match:
        return f'{field_label} must be in HH:MM or HH:MM - HH:MM format'
    # For range format, validate end > start
    if range_match:
        sh, sm, eh, em = int(range_match.group(1)), int(range_match.group(2)), int(range_match.group(3)), int(range_match.group(4))
        if eh * 60 + em <= sh * 60 + sm:
            return f'{field_label}: end time must be after start time'
        start_h, start_m = sh, sm
    else:
        start_h, start_m = int(single_match.group(1)), int(single_match.group(2))
    # Past-time check for today
    if event_date:
        try:
            d = datetime.strptime(event_date, '%Y-%m-%d').date() if isinstance(event_date, str) else event_date
            if d == date.today():
                now = datetime.now()
                if start_h < now.hour or (start_h == now.hour and start_m <= now.minute):
                    return f'{field_label} must be in the future for today\'s date'
        except (ValueError, TypeError):
            pass
    return None


def validate_numeric(value, field_label='Value', min_val=None, max_val=None, required=True):
    """Validate a numeric value"""
    if value is None or value == '':
        return f'{field_label} is required' if required else None
    try:
        n = float(value)
    except (ValueError, TypeError):
        return f'{field_label} must be a number'
    if min_val is not None and n < min_val:
        return f'{field_label} must be at least {min_val}'
    if max_val is not None and n > max_val:
        return f'{field_label} must be at most {max_val}'
    return None


def validate_text_length(value, field_label='Text', min_len=0, max_len=500, required=False):
    """Validate text field length"""
    v = _strip(value)
    if not v:
        return f'{field_label} is required' if required else None
    if min_len and len(v) < min_len:
        return f'{field_label} must be at least {min_len} characters'
    if len(v) > max_len:
        return f'{field_label} must be under {max_len} characters'
    return None


def validate_enum(value, allowed, field_label='Field'):
    """Validate value is in allowed set"""
    v = _strip(value).lower() if value else ''
    if not v:
        return f'{field_label} is required'
    if v not in allowed:
        return f'{field_label} must be one of: {", ".join(sorted(allowed))}'
    return None


# ─── Composite Validators ─── ───────────────────────────────

def validate_registration(data):
    """Validate registration form data. Returns list of errors."""
    errors = []
    e = validate_name(data.get('first_name'), 'First name')
    if e: errors.append(e)
    e = validate_name(data.get('last_name'), 'Last name')
    if e: errors.append(e)
    e = validate_email(data.get('email'))
    if e: errors.append(e)
    e = validate_phone(data.get('phone'))
    if e: errors.append(e)
    e = validate_password(data.get('password'))
    if e: errors.append(e)
    ut = _strip(data.get('user_type', '')).lower()
    if ut not in VALID_USER_TYPES:
        errors.append(f'User type must be one of: {", ".join(VALID_USER_TYPES)}')
    return errors


def validate_login(data):
    """Validate login form data"""
    errors = []
    e = validate_email(data.get('email'))
    if e: errors.append(e)
    if not data.get('password'):
        errors.append('Password is required')
    return errors


def validate_booking(data):
    """Validate booking creation data"""
    errors = []
    if not data.get('customer_id'):
        errors.append('Customer ID is required')
    st = _strip(data.get('service_type', ''))
    if not st:
        errors.append('Service type is required')
    e = validate_date(data.get('event_date'), 'Event date', allow_past=False)
    if e: errors.append(e)
    e = validate_time(data.get('event_time'), 'Event time', event_date=data.get('event_date'))
    if e and data.get('event_time'):  # Only error if time is provided
        errors.append(e)
    e = validate_numeric(data.get('total_price'), 'Total price', min_val=0.01)
    if e: errors.append(e)
    e = validate_text_length(data.get('notes'), 'Notes', max_len=MAX_NOTES)
    if e: errors.append(e)
    e = validate_text_length(data.get('location'), 'Location', max_len=MAX_LOCATION)
    if e: errors.append(e)
    return errors


def validate_contact(data):
    """Validate contact form data"""
    errors = []
    e = validate_name(data.get('first_name'), 'First name')
    if e: errors.append(e)
    e = validate_name(data.get('last_name'), 'Last name', required=False)
    if e: errors.append(e)
    e = validate_email(data.get('email'))
    if e: errors.append(e)
    e = validate_phone(data.get('phone'), required=False)
    if e: errors.append(e)
    e = validate_text_length(data.get('subject'), 'Subject', max_len=MAX_SUBJECT)
    if e: errors.append(e)
    e = validate_text_length(data.get('message'), 'Message', min_len=10, max_len=MAX_MESSAGE, required=True)
    if e: errors.append(e)
    return errors


def validate_profile_update(data):
    """Validate profile update data"""
    errors = []
    if data.get('first_name') is not None:
        e = validate_name(data.get('first_name'), 'First name')
        if e: errors.append(e)
    if data.get('last_name') is not None:
        e = validate_name(data.get('last_name'), 'Last name')
        if e: errors.append(e)
    if data.get('email') is not None:
        e = validate_email(data.get('email'))
        if e: errors.append(e)
    if data.get('phone') is not None:
        e = validate_phone(data.get('phone'), required=False)
        if e: errors.append(e)
    return errors


def validate_photographer_update(data):
    """Validate photographer profile update"""
    errors = []
    if 'hourly_rate' in data:
        e = validate_numeric(data.get('hourly_rate'), 'Hourly rate', min_val=0)
        if e: errors.append(e)
    if 'bio' in data:
        e = validate_text_length(data.get('bio'), 'Bio', max_len=MAX_BIO)
        if e: errors.append(e)
    if 'location' in data:
        e = validate_text_length(data.get('location'), 'Location', max_len=MAX_LOCATION)
        if e: errors.append(e)
    if 'specialty' in data:
        e = validate_text_length(data.get('specialty'), 'Specialty', max_len=100, required=True)
        if e: errors.append(e)
    return errors


def validate_change_password(data):
    """Validate password change request"""
    errors = []
    if not data.get('current_password'):
        errors.append('Current password is required')
    e = validate_password(data.get('new_password'), 'New password')
    if e: errors.append(e)
    return errors


def validate_feedback(data):
    """Validate feedback submission"""
    errors = []
    if not data.get('booking_id'):
        errors.append('Booking ID is required')
    if not data.get('customer_id'):
        errors.append('Customer ID is required')
    e = validate_numeric(data.get('rating'), 'Rating', min_val=1, max_val=5)
    if e: errors.append(e)
    e = validate_text_length(data.get('comment'), 'Comment', max_len=MAX_MESSAGE)
    if e: errors.append(e)
    return errors


def validate_admin_create_user(data):
    """Validate admin user creation"""
    errors = []
    e = validate_name(data.get('first_name'), 'First name')
    if e: errors.append(e)
    e = validate_name(data.get('last_name'), 'Last name')
    if e: errors.append(e)
    e = validate_email(data.get('email'))
    if e: errors.append(e)
    e = validate_password(data.get('password'))
    if e: errors.append(e)
    ut = _strip(data.get('user_type', '')).lower()
    if ut not in VALID_USER_TYPES:
        errors.append(f'User type must be one of: {", ".join(VALID_USER_TYPES)}')
    return errors


def validate_booking_status(status):
    """Validate booking status value"""
    if not status:
        return 'Status is required'
    if status.lower() not in VALID_BOOKING_STATUSES:
        return f'Status must be one of: {", ".join(sorted(VALID_BOOKING_STATUSES))}'
    return None


def sanitize_data(data):
    """Sanitize all string values in a dict"""
    if not isinstance(data, dict):
        return data
    cleaned = {}
    for k, v in data.items():
        if isinstance(v, str):
            cleaned[k] = _sanitize_html(v.strip())
        else:
            cleaned[k] = v
    return cleaned


def check_booking_conflicts(photographer_id, event_date, event_time=None, exclude_booking_id=None):
    """
    Check if a photographer has a conflicting booking on the same date/time.
    Returns error string if conflict found, None if clear.
    """
    from models import Booking
    query = Booking.query.filter(
        Booking.photographer_id == photographer_id,
        Booking.event_date == event_date,
        Booking.status.in_(['accepted', 'token_paid', 'completed', 'pending'])
    )
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)

    conflicting = query.all()

    if event_time and conflicting:
        # Check time-level conflicts
        for b in conflicting:
            if b.event_time == event_time:
                return f'Photographer already has a booking at {event_time} on {event_date}'
    elif conflicting:
        return f'Photographer already has {len(conflicting)} booking(s) on {event_date}'

    return None


def get_booked_slots(photographer_id, event_date):
    """Get all booked time slots for a photographer on a given date"""
    from models import Booking
    bookings = Booking.query.filter(
        Booking.photographer_id == photographer_id,
        Booking.event_date == event_date,
        Booking.status.in_(['accepted', 'token_paid', 'completed', 'pending'])
    ).all()
    return [b.event_time for b in bookings if b.event_time]
