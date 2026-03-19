from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import User, Photographer, Booking, Package, PortfolioItem, Notification, ActivityLog, EventCategory
from . import photographer_bp
from .forms import PhotographerProfileForm, PackageForm, ChangePasswordForm
from functools import wraps
import os
import uuid
from datetime import datetime
from invoice_generator import generate_booking_invoice_pdf
from email_service import send_booking_accepted_email, send_booking_cancelled_email
from models import RefundRequest

def photographer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'photographer':
            flash('Photographer access required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def log_activity(action, details=None):
    try:
        log = ActivityLog(user_id=current_user.id, action=action, details=details)
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging activity: {e}")

@photographer_bp.route('/dashboard')
@photographer_required
def dashboard():
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    if not photographer:
        flash('Photographer profile not found.', 'error')
        return redirect(url_for('login'))
    
    # Stats
    total_requests = Booking.query.filter_by(photographer_id=photographer.id, status='pending').count()
    active_sessions = Booking.query.filter_by(photographer_id=photographer.id, status='accepted').count()
    completed_events = Booking.query.filter_by(photographer_id=photographer.id, status='completed').count()
    
    # Calculate total earnings from completed bookings
    completed_bookings = Booking.query.filter_by(photographer_id=photographer.id, status='completed').all()
    total_earnings = sum(b.total_price for b in completed_bookings)
    
    # Recent Logs
    from models import ActivityLog
    recent_logs = ActivityLog.query.filter_by(user_id=current_user.id).order_by(ActivityLog.timestamp.desc()).limit(5).all()
    
    return render_template('photographer/dashboard.html', 
                           total_requests=total_requests,
                           active_sessions=active_sessions,
                           completed_events=completed_events,
                           total_earnings=total_earnings,
                           recent_logs=recent_logs)

@photographer_bp.route('/requests')
@photographer_required
def incoming_requests():
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    requests = Booking.query.filter_by(photographer_id=photographer.id, status='pending').order_by(Booking.created_at.desc()).all()
    return render_template('photographer/requests.html', bookings=requests)

@photographer_bp.route('/request/accept/<int:id>', methods=['POST'])
@photographer_required
def accept_request(id):
    booking = Booking.query.get_or_404(id)
    booking.status = 'accepted'
    
    # Notification for customer
    notification = Notification(
        user_id=booking.customer_id,
        booking_id=booking.id,
        title='Booking Accepted! 📸',
        message=f'Your {booking.service_type} session has been accepted by the photographer. Please pay the token amount to confirm your booking.',
        notification_type='job_accepted'
    )
    db.session.add(notification)
    db.session.commit()
    
    # Send email with PDF invoice to customer
    try:
        customer = User.query.get(booking.customer_id)
        photographer = Photographer.query.get(booking.photographer_id)
        
        if customer and photographer:
            # Generate PDF invoice
            pdf_bytes = generate_booking_invoice_pdf(booking, customer, photographer)
            
            # Send email with PDF attached
            email_sent = send_booking_accepted_email(booking, customer, photographer, pdf_bytes)
            
            if email_sent:
                print(f"[EMAIL] Booking acceptance email sent for Booking #{id}")
            else:
                print(f"[EMAIL] Failed to send email for Booking #{id}")
    except Exception as e:
        # Don't block the acceptance flow if email fails
        print(f"[EMAIL ERROR] Error sending booking email: {e}")
    
    log_activity('accept_request', f"Accepted booking ID: {id}")
    flash('Booking accepted successfully!', 'success')
    return redirect(url_for('photographer.incoming_requests'))

@photographer_bp.route('/request/decline/<int:id>', methods=['POST'])
@photographer_required
def decline_request(id):
    booking = Booking.query.get_or_404(id)
    booking.status = 'declined'
    
    # Notification
    notification = Notification(
        user_id=booking.customer_id,
        booking_id=booking.id,
        title='Booking Declined',
        message=f'Unfortunately, the photographer has declined your {booking.service_type} session.',
        notification_type='job_declined'
    )
    db.session.add(notification)
    db.session.commit()
    
    log_activity('decline_request', f"Declined booking ID: {id}")
    flash('Booking declined.', 'info')
    return redirect(url_for('photographer.incoming_requests'))

@photographer_bp.route('/packages')
@photographer_required
def manage_packages():
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    packages = Package.query.filter_by(photographer_id=photographer.id).all()
    form = PackageForm()
    # Populate categories for the form
    categories = EventCategory.query.all()
    return render_template('photographer/packages.html', packages=packages, form=form, categories=categories)

@photographer_bp.route('/package/add', methods=['POST'])
@photographer_required
def add_package():
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    form = PackageForm()
    if form.validate_on_submit():
        new_package = Package(
            photographer_id=photographer.id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category_id=form.category_id.data
        )
        
        if form.sample_image.data:
            file = form.sample_image.data
            filename = f"pkg_{uuid.uuid4().hex}_{file.filename}"
            file.save(os.path.join(current_app.config['PROFILE_FOLDER'], filename))
            new_package.image_url = f"profiles/{filename}"
            
        db.session.add(new_package)
        db.session.commit()
        flash('Package added successfully!', 'success')
    return redirect(url_for('photographer.manage_packages'))

@photographer_bp.route('/sessions')
@photographer_required
def accepted_sessions():
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    sessions = Booking.query.filter(
        Booking.photographer_id == photographer.id, 
        Booking.status.in_(['accepted', 'token_paid'])
    ).order_by(Booking.event_date.asc()).all()
    return render_template('photographer/sessions.html', sessions=sessions)
@photographer_bp.route('/earnings')
@photographer_required
def earnings():
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    # Earning stats
    completed_bookings = Booking.query.filter_by(photographer_id=photographer.id, status='completed').all()
    total_token = sum(b.token_amount for b in completed_bookings)
    total_balance = sum(b.remaining_amount for b in completed_bookings)
    
    return render_template('photographer/earnings.html', 
                           total_token=total_token, 
                           total_balance=total_balance, 
                           bookings=completed_bookings)

@photographer_bp.route('/profile', methods=['GET', 'POST'])
@photographer_required
def profile():
    profile_form = PhotographerProfileForm(obj=current_user)
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    
    if photographer:
        if request.method == 'GET':
            profile_form.experience.data = photographer.experience
            profile_form.location.data = photographer.location
            profile_form.bio.data = photographer.bio
            profile_form.specialty.data = photographer.specialty
            profile_form.hourly_rate.data = photographer.hourly_rate

    password_form = ChangePasswordForm()
    
    if profile_form.validate_on_submit() and 'submit_profile' in request.form:
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.email = profile_form.email.data
        current_user.phone = profile_form.phone.data
        
        if photographer:
            photographer.experience = profile_form.experience.data
            photographer.location = profile_form.location.data
            photographer.bio = profile_form.bio.data
            photographer.specialty = profile_form.specialty.data
            photographer.hourly_rate = profile_form.hourly_rate.data
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('photographer.profile'))
        
    return render_template('photographer/profile.html', profile_form=profile_form, password_form=password_form)

@photographer_bp.route('/session/complete/<int:id>', methods=['POST'])
@photographer_required
def complete_session(id):
    booking = Booking.query.get_or_404(id)
    booking.status = 'completed'
    booking.payment_status = 'paid'
    db.session.commit()
    log_activity('complete_session', f"Completed booking ID: {id}")
    flash('Session marked as completed!', 'success')
    return redirect(url_for('photographer.accepted_sessions'))

@photographer_bp.route('/session/update-balance/<int:id>', methods=['POST'])
@photographer_required
def update_balance(id):
    booking = Booking.query.get_or_404(id)
    try:
        new_balance = float(request.form.get('balance', 0))
        booking.remaining_amount = new_balance
        db.session.commit()
        flash('Balance updated successfully!', 'success')
    except ValueError:
        flash('Invalid balance amount.', 'error')
    return redirect(url_for('photographer.accepted_sessions'))

@photographer_bp.route('/portfolio/upload', methods=['POST'])
@photographer_required
def upload_portfolio():
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    if 'photos' in request.files:
        files = request.files.getlist('photos')
        for file in files:
            if file:
                filename = f"pt_{uuid.uuid4().hex}_{file.filename}"
                file.save(os.path.join(current_app.config['PROFILE_FOLDER'], filename))
                item = PortfolioItem(photographer_id=photographer.id, image_url=f"profiles/{filename}")
                db.session.add(item)
        db.session.commit()
        flash('Portfolio updated!', 'success')
    return redirect(url_for('photographer.profile'))


@photographer_bp.route('/session/cancel/<int:id>', methods=['POST'])
@photographer_required
def cancel_session(id):
    booking = Booking.query.get_or_404(id)
    photographer = Photographer.query.filter_by(user_id=current_user.id).first()
    
    if booking.photographer_id != photographer.id:
        flash('Unauthorized.', 'error')
        return redirect(url_for('photographer.accepted_sessions'))

    if booking.status == 'cancelled':
        flash('Booking already cancelled.', 'info')
        return redirect(url_for('photographer.accepted_sessions'))

    # Update booking status
    booking.status = 'cancelled'
    booking.cancelled_by = 'photographer'
    
    # Check if payment was made (token or full)
    if booking.payment_status in ('token_paid', 'paid'):
        # Create refund request automatically
        refund_req = RefundRequest(
            booking_id=booking.id,
            customer_id=booking.customer_id,
            refund_amount=booking.token_amount if booking.payment_status == 'token_paid' else booking.total_price,
            reason=f"Photographer cancelled the booking. (Cancelled by: {current_user.first_name})",
            status='pending',
            cancelled_by='photographer'
        )
        db.session.add(refund_req)

    # Notification for customer
    notification = Notification(
        user_id=booking.customer_id,
        booking_id=booking.id,
        title='Booking Cancelled ⚠️',
        message=f'Unfortunately, the photographer has cancelled your {booking.service_type} session on {booking.event_date}. A refund will be processed if applicable.',
        notification_type='job_cancelled'
    )
    db.session.add(notification)
    db.session.commit()

    # Send email to customer
    try:
        customer = User.query.get(booking.customer_id)
        if customer:
            send_booking_cancelled_email(booking, customer, photographer, reason="Photographer had a schedule conflict or emergency.")
    except Exception as e:
        print(f"[EMAIL ERROR] Error sending cancellation email: {e}")

    log_activity('cancel_request', f"Cancelled booking ID: {id} as photographer")
    flash('Booking cancelled successfully.', 'success')
    return redirect(url_for('photographer.accepted_sessions'))
