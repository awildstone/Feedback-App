from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class UserForm(FlaskForm):
    """ User form to accept a username, password, email, first_name, and last_name."""

    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30, message="Your first name must be less than 30 characters.")])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30, message="Your last name must be less than 30 characters.")])
    email = StringField("Email", validators=[InputRequired(), Email(message="You must enter a valid email."), Length(min=6, max=50, message="Your email address must be between 6 and 50 characters.")])
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20, message="Your username must be between 1 and 20 characters.")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55, message="Your password must be between 6 and 55 characters.")])

class LoginForm(FlaskForm):
    """ Login form that accepts a username and password. """

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20, message="Your username must be between 1 and 20 characters.")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55, message="Your password must be between 6 and 55 characters.")])

class FeedbackForm(FlaskForm):
    """ Form to add User Feedbck. """

    title = StringField("Title", validators=[InputRequired(), Length(max=100, message="Your title must be less than 100 characters.")])
    content = TextAreaField("Content", validators=[InputRequired()])