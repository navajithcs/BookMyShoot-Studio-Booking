from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Optional
from flask_wtf.file import FileAllowed

class PhotographerProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    experience = StringField('Experience', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    bio = TextAreaField('Bio', validators=[Optional()])
    specialty = StringField('Specialty', validators=[Optional()])
    hourly_rate = FloatField('Hourly Rate', validators=[Optional()])

class PackageForm(FlaskForm):
    name = StringField('Package Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired()])
    category_id = StringField('Category ID', validators=[Optional()])
    sample_image = FileField('Sample Image', validators=[Optional(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
