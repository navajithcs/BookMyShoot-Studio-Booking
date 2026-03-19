from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import User, Photographer, Booking, Package, PortfolioItem, Notification, ActivityLog, EventCategory
from . import customer_bp
from .forms import CustomerProfileForm, BookingRequestForm, ChangePasswordForm
from functools import wraps
from datetime import datetime

def customer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'customer':
            flash('Customer access required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@customer_bp.route('/dashboard')
@customer_required
def dashboard():
    # Stats for the dashboard
    active_bookings = Booking.query.filter_by(customer_id=current_user.id).filter(Booking.status.in_(['accepted', 'token_paid'])).count()
    pending_requests = Booking.query.filter_by(customer_id=current_user.id, status='pending').count()
    completed_sessions = Booking.query.filter_by(customer_id=current_user.id, status='completed').count()
    
    categories = EventCategory.query.all()
    
    return render_template('customer/dashboard.html', 
                           active_count=active_bookings,
                           pending_count=pending_requests,
                           completed_count=completed_sessions,
                           categories=categories)

@customer_bp.route('/search')
@customer_required
def search():
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    category_id = request.args.get('category', '')
    
    photographers_query = Photographer.query.join(User)
    
    if query:
        photographers_query = photographers_query.filter(User.first_name.contains(query) | User.last_name.contains(query))
    if location:
        photographers_query = photographers_query.filter(Photographer.location.contains(location))
    if category_id:
        # Assuming photographers have a primary specialty or we filter by category
        photographers_query = photographers_query.filter(Photographer.specialty.contains(category_id))

    photographers = photographers_query.all()
    categories = EventCategory.query.all()
    
    return render_template('customer/search.html', 
                           photographers=photographers, 
                           categories=categories)

@customer_bp.route('/photographer/<int:id>')
@customer_required
def view_photographer(id):
    photographer = Photographer.query.get_or_404(id)
    packages = Package.query.filter_by(photographer_id=id).all()
    portfolio = PortfolioItem.query.filter_by(photographer_id=id).all()
    form = BookingRequestForm()
    form.package_id.choices = [(0, 'Custom/Not Listed')] + [(p.id, f"{p.name} (₹{p.price})") for p in packages]
    
    return render_template('customer/photographer_profile.html', 
                           photo=photographer, 
                           packages=packages, 
                           portfolio=portfolio,
                           form=form)

@customer_bp.route('/book/<int:photo_id>', methods=['POST'])
@customer_required
def request_session(photo_id):
    photographer = Photographer.query.get_or_404(photo_id)
    packages = Package.query.filter_by(photographer_id=photo_id).all()
    
    form = BookingRequestForm()
    form.package_id.choices = [(0, 'Custom/Not Listed')] + [(p.id, f"{p.name} (₹{p.price})") for p in packages]
    
    if form.validate_on_submit():
        total_price = 0
        selected_package = None
        
        if form.package_id.data and form.package_id.data > 0:
            selected_package = Package.query.get(form.package_id.data)
            if selected_package:
                total_price = selected_package.price
        
        # Calculate 20% token
        token_amount = total_price * 0.20
        remaining_amount = total_price - token_amount
        
        new_booking = Booking(
            customer_id=current_user.id,
            photographer_id=photo_id,
            service_type=form.service_type.data,
            event_date=form.event_date.data,
            event_time=form.event_time.data,
            location=form.location.data,
            notes=form.notes.data,
            status='pending',
            total_price=total_price,
            token_amount=token_amount,
            remaining_amount=remaining_amount,
            payment_status='pending'
        )
        db.session.add(new_booking)
        db.session.commit()
        
        # Notify photographer
        notification = Notification(
            user_id=photographer.user_id,
            booking_id=new_booking.id,
            title='New Booking Request! 📸',
            message=f'{current_user.first_name} has requested a {form.service_type.data} session.',
            notification_type='new_booking'
        )
        db.session.add(notification)
        db.session.commit()
        
        flash('Session requested successfully! Check "My Orders" for status updates.', 'success')
        return redirect(url_for('customer.my_orders'))
    
    flash('Error in booking form. Please check your inputs.', 'error')
    return redirect(url_for('customer.view_photographer', id=photo_id))

@customer_bp.route('/orders')
@customer_required
def my_orders():
    bookings = Booking.query.filter_by(customer_id=current_user.id).order_by(Booking.created_at.desc()).all()
    return render_template('customer/my_orders.html', bookings=bookings)

@customer_bp.route('/notifications')
@customer_required
def notifications():
    notes = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('customer/notifications.html', notifications=notes)

@customer_bp.route('/profile', methods=['GET', 'POST'])
@customer_required
def profile():
    form = CustomerProfileForm(obj=current_user)
    password_form = ChangePasswordForm()
    
    if form.validate_on_submit() and 'submit_profile' in request.form:
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('customer.profile'))
        
    return render_template('customer/profile.html', form=form, password_form=password_form)
