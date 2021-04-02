from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email


class UserForm(FlaskForm):
    """ User form to accept a username, password, email, first_name, and last_name."""

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), Email(message="You must enter a valid email.")])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """ Login form that accepts a username and password. """

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """ Form to add User Feedbck. """

    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content", validators=[InputRequired()])


# class EditFeedback(FlaskForm):
#     """ Form to edit User Feedbck. """

#     title = StringField("Title", validators=[InputRequired()])
#     content = StringField("Title", validators=[InputRequired()])