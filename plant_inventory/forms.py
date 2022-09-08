from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email

class UserLoginForm(FlaskForm):
    first_name = StringField('First name', validators = [InputRequired()])
    last_name = StringField('Last name')
    email = StringField('Email', validators = [InputRequired(), Email()])
    password = PasswordField('Password', validators = [InputRequired()])
    submit_button = SubmitField()