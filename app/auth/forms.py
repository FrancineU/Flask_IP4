from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Email, EqualTo
from wtforms import ValidationError
from ..models import Writer

class SignupForm(FlaskForm):
    fullname = StringField('Your Fullname', validators=[Required()])
    email = StringField('Your Email Address', validators=[Required(), Email()])
    password = PasswordField('Password', validators = [Required(), EqualTo('password_confirm', message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords', validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self, data_field):
        if Writer.query.filter_by(email = data_field.data).first():
            raise ValidationError('Email already exists')

class LoginForm(FlaskForm):
    email = StringField('Your Email Address', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
