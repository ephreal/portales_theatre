from flask import render_template, redirect, Blueprint, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from theatre import models, login_manager, db
from theatre.forms import UserForm, LoginForm
from theatre.routes import route_functions
from theatre.routes.api import admin as admin_api


User = models.User


auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user for use with the login manager.

    This is handled automatically by login_manager, so you should never need
    to call this manually.
    """
    return User.query.filter_by(id=user_id).first()


@login_manager.request_loader
def request_loader(id):
    return True


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login/')


# These routes are used to centralize any user authentication

@auth.route("/login/", methods=["GET"])
def display_login():
    """
    URL: /login/

    Method: GET

    Displays the login page to the user.
    """
    form = LoginForm()
    return render_template("theatre/pages/login.html", form=form)


@auth.route("/login/", methods=["POST"])
def login():
    """
    URL: /login/

    Method: POST

    Processes the submitted Login Form.

    If the form is valid, it will then check the email/password combo.
    If the email/password combo is valid, it will then log the user in.

    If the form is invalid, or if the email/password combo are incorrect,
    the user will be returned to the login screen.
    """

    form = LoginForm(request.form)

    if not form.validate():
        # Something is wrong with the form. Flash the errors and return to
        # the login screen.
        route_functions.flash_form_errors(form, "error")
        return render_template("theatre/pages/login.html", form=form)

    # The form is valid. Load the user that has the email provided.
    user = User.query.filter_by(email=form.email.data).first()

    # Make sure that a user actually exists first
    if not user:
        flash("User does not exist", "error")
        return render_template("theatre/pages/login.html", form=form)

    # If the user exists, check the password.
    if not user.check_password(form.password.data):
        # The password does not match. Return to the login screen.
        flash("Invalid username or password")
        return render_template("theatre/pages/login.html", form=form)

    # log the user in.
    user.authenticated = True
    login_user(user, remember=True)

    # Save the authentication information back to the DB.
    db.session.add(user)
    db.session.commit()
    flash("Logged in", "success")

    # Redirect the user to the main page.
    return redirect("/")


@auth.route("/signup/", methods=["GET"])
def display_signup():
    """
    URL: /signup/

    Method: GET

    Returns the signup page to the user.
    """
    form = UserForm()
    return render_template("theatre/pages/signup.html", form=form)


@auth.route("/signup/", methods=["POST"])
def signup():
    """
    URL: /signup/

    Method: POST

    Processes the signup form.

    If the form is valid, it will then attempt to create a new user.

    If the user data is invalid, or the email address already exists in the
    user database, the user will be returned to the signup page and asked to
    correct the errors.

    If the user data is valid and the email address does not alraedy exist,
    the user will be created in the database and the user will be redirected
    to the login page.

    Request Post Form fields
    Username: String
    Password: String
    Confirmation: String
    Email: String
    """

    form = UserForm(request.form)

    if not form.validate():
        route_functions.flash_errors(form)
        return render_template("theatre/pages/signup.html", form=form)

    # We will not allow signed up users to be an admin, even if they somehow
    # manage to set the is_admin bit.
    form.is_admin.data = False

    user = route_functions.serialize_user_form(form, 0)

    user = admin_api.create_user(user)

    if isinstance(user, dict):
        flash(user, "error")
        return render_template("theatre/pages/signup.html", form=form)

    flash("Signup successful, please login.", "success")
    return redirect("/login/")


@login_required
@auth.route("/logout/")
def logout():
    """
    URL: /logout/

    Method: GET

    Logs the current user out.
    """
    current_user.authenticated = False

    db.session.add(current_user)
    db.session.commit()

    logout_user()
    flash("Logged out", "informational")
    return redirect("/")
