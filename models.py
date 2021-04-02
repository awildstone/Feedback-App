from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User Model for DB. """

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete, delete-orphan")

    @classmethod
    def register(self, fname, lname, email, username, password):
        """ Register a new User. Return a new User with a hashed password. """

        hash_pwd = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hash_pwd.decode("utf8")

        return self(first_name=fname, last_name=lname, email=email, username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(self, username, password):
        """ Authenticate a User. If the user exists & the password matches the user password hash, return
        the user, else return False. """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Feedback(db.Model):
    """ Feedback Model for DB. """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey("users.username"), nullable=False)