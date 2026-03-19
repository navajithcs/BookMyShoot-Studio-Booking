from flask import render_template, redirect, url_for, flash, request, current_app, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import User, Photographer, Booking, EventCategory, ActivityLog, PortfolioItem, Notification
from . import admin_bp
from .forms import AdminProfileForm, ChangePasswordForm, EventCategoryForm, PackageEditForm
from functools import wraps
import os
import uuid
from datetime import datetime

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.user_type != 'admin':
            flash('Admin access required.', 'error')
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

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Analytics data
    total_users = User.query.count()
    total_photographers = User.query.filter_by(user_type='photographer').count()
    total_bookings = Booking.query.count()
    
    # Revenue calculation
    completed_bookings = Booking.query.filter_by(status='completed').all()
    total_revenue = sum(b.total_price for b in completed_bookings)
    
    return render_template('admin/admin_dashboard.html', 
                           total_users=total_users,
                           total_photographers=total_photographers,
                           total_bookings=total_bookings,
                           total_revenue=total_revenue)

@admin_bp.route('/profile', methods=['GET', 'POST'])
@admin_required
def profile():
    profile_form = AdminProfileForm(obj=current_user)
    password_form = ChangePasswordForm()
    
    if profile_form.validate_on_submit() and 'submit_profile' in request.form:
        current_user.first_name = profile_form.first_name.data
        current_user.last_name = profile_form.last_name.data
        current_user.email = profile_form.email.data
        
        if profile_form.profile_image.data:
            file = profile_form.profile_image.data
            filename = f"{current_user.id}_{uuid.uuid4().hex}_{file.filename}"
            file.save(os.path.join(current_app.config['PROFILE_FOLDER'], filename))
            current_user.profile_image = f"profiles/{filename}"
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))
        
    return render_template('admin/profile.html', profile_form=profile_form, password_form=password_form)

@admin_bp.route('/change-password', methods=['POST'])
@admin_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Password changed successfully!', 'success')
        else:
            flash('Incorrect old password.', 'error')
    return redirect(url_for('admin.profile'))

@admin_bp.route('/categories', methods=['GET'])
@admin_required
def categories():
    categories = EventCategory.query.order_by(EventCategory.name).all()
    form = EventCategoryForm()
    return render_template('admin/categories.html', categories=categories, form=form)

@admin_bp.route('/category/add', methods=['POST'])
@admin_required
def add_category():
    form = EventCategoryForm()
    if form.validate_on_submit():
        new_cat = EventCategory(name=form.name.data, description=form.description.data)
        db.session.add(new_cat)
        db.session.commit()
        log_activity('add_category', f"Added category: {new_cat.name}")
        flash(f'Category "{new_cat.name}" added successfully!', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/category/edit/<int:id>', methods=['POST'])
@admin_required
def edit_category(id):
    cat = EventCategory.query.get_or_404(id)
    form = EventCategoryForm()
    if form.validate_on_submit():
        cat.name = form.name.data
        cat.description = form.description.data
        db.session.commit()
        log_activity('edit_category', f"Edited category ID: {id}")
        flash('Category updated successfully!', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/category/delete/<int:id>', methods=['POST'])
@admin_required
def delete_category(id):
    cat = EventCategory.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    log_activity('delete_category', f"Deleted category: {cat.name}")
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/bookings')
@admin_required
def bookings():
    status = request.args.get('status')
    query = Booking.query
    if status:
        query = query.filter_by(status=status)
    bookings = query.order_by(Booking.created_at.desc()).all()
    return render_template('admin/bookings.html', bookings=bookings, current_status=status)

@admin_bp.route('/booking/<int:id>/complete', methods=['POST'])
@admin_required
def complete_booking(id):
    booking = Booking.query.get_or_404(id)
    booking.status = 'completed'
    booking.payment_status = 'paid'
    db.session.commit()
    flash('Booking marked as completed!', 'success')
    return redirect(url_for('admin.bookings'))

@admin_bp.route('/users')
@admin_required
def users():
    query = request.args.get('q', '')
    user_type = request.args.get('role', '')
    
    users_query = User.query
    if query:
        users_query = users_query.filter(User.email.contains(query) | User.first_name.contains(query))
    if user_type:
        users_query = users_query.filter_by(user_type=user_type)
        
    users_list = users_query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users_list)

@admin_bp.route('/packages')
@admin_required
def packages():
    # Package management placeholder logic
    # In a full implementation, this would list photographer packages
    # and allow simple edits or search by photographer name.
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    
    # Photographers often have packages (implicitly or explicitly)
    # For now, let's list all photographers and their key metrics
    # as a "Package/Service Management" view.
    photographers_query = Photographer.query
    if search_query:
        photographers_query = photographers_query.join(User).filter(User.first_name.contains(search_query))
        
    pagination = photographers_query.paginate(page=page, per_page=10)
    return render_template('admin/packages.html', pagination=pagination)
