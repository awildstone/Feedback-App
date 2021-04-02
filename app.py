from flask import Flask, render_template, redirect, session, flash, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "&03apJi4SkpjusrU^5NmOObh$"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

def session_user(username):
    """ Validates if the current user is in session.
    Return true if current user is in session, otherwise
    flash a warning to the user. """

    if session['username'] == username:
        return True
    else:
        flash("Access Denied.", "danger")

@app.errorhandler(404)
def page_not_found(e):
    """ Custom 404 route. """
    return render_template("404.html", e=e), 404

@app.errorhandler(403)
def page_not_found(e):
    """ Custom 404 route. """
    return render_template("denied.html", e=e), 403

@app.route("/")
def redirect_register():
    """ Redirect to /register. """

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    """ Show a form to register/create a user.
    Process the registration of a new user. """

    form = UserForm()

    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        new_user = User.register(first_name, last_name, email, username, password)

        db.session.add(new_user)

        # Error handling to check if a username already exists
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append(f"{username} is taken. Please choose a different username")

            return render_template("register.html", form=form)

        # Add username to the session
        session["username"] = new_user.username
        flash(f"Welcome, {new_user.first_name} {new_user.last_name}! Your account is created.", "success")

        return redirect(f"/users/{new_user.username}")

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    """ Show a form to login. Process the user login request. """

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user:
            session["username"] = user.username
            flash(f"Welcome back, {user.first_name} {user.last_name}!", "info")
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]

    return render_template("login.html", form=form)

@app.route("/users/<username>")
def secret(username):
    """ Display User landing page. """

    if session_user(username):
        current_user = User.query.get_or_404(username)
        # get the current user's feedback
        feedback = Feedback.query.filter_by(username=username).all()

        return render_template("landing.html", user=current_user, feedback=feedback)
    
    abort(403)

@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """ Delete a user from the database. """

    if session_user(username):
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")
        flash(f"{username} deleted", "warning")

        return redirect("/")

    abort(403)


@app.route("/logout")
def logout():
    """ Log out the current user and clear any session data. """

    session.pop("username")
    flash("Logged out.", "info")

    return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """ Show form for current user to add Feedback. Handle adding new Feedback. """

    if session_user(username):
        form = FeedbackForm()

        if form.validate_on_submit():
            new_feedback = Feedback(
                title = form.title.data,
                content = form.content.data,
                username = username
            )
            db.session.add(new_feedback)
            db.session.commit()
            flash("New feedback accepted!","success")

            return redirect(f"/users/{username}")
    else:
        abort(403)

    return render_template("add_feedback.html", form=form)

@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """ Show form for current user to update their Feedback. Handle updating Feedback."""

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.user.username

    if session_user(username):
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.commit()
            flash(f"Updated {feedback.title} for {username}.", "success")

            return redirect(f"/users/{username}")
    else:
        abort(403)
    
    return render_template("update_feedback.html", form=form)

@app.route("/feedback/<feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """ Delete current user's feedback from the DB. """

    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.user.username

    if session_user(username):
        db.session.delete(feedback)
        db.session.commit()
        flash(f"Deleted {feedback.title} for {username}.", "warning")

        return redirect(f"/users/{username}")

    else:
        abort(403)