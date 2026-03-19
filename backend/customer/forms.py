from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, FileField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from flask_wtf.file import FileAllowed

class CustomerProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    profile_image = FileField('Profile Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class BookingRequestForm(FlaskForm):
    service_type = StringField('Event Type', validators=[DataRequired()])
    event_date = DateField('Event Date', validators=[DataRequired()])
    event_time = StringField('Event Time', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    package_id = SelectField('Select Package', coerce=int, validators=[Optional()])
    notes = TextAreaField('Message/Notes', validators=[Optional()])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
