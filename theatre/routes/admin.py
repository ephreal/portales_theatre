from flask import render_template, Blueprint, redirect, flash, request, url_for
from theatre.app import models
from flask_login import login_required, current_user
from theatre.routes.api import admin as api
from theatre.forms import UserForm, PlayForm, ModifyUserForm, PasswordForm
from theatre.routes.route_functions import flash_form_errors
from theatre.routes.route_functions import serialize_user_form
from theatre.routes.route_functions import serialize_play_form


admin = Blueprint("admin", __name__, url_prefix="/admin/")


User = models.User
Play = models.Play


@admin.before_request
def check_admin():
    """
    Checks to see if the current user is an administrator.

    If the user is not an administrator, it redirects them to the site's index
    page.
    """
    if not current_user.is_admin:
        return redirect("/")


@admin.route("test/")
def test():
    """
    A simple test route.
    """
    return render_template("admin/test.html")


@login_required
@admin.route("/")
def index():
    """
    URL: /admin/

    Method: GET

    Returns the index page for the administrative area.
    """
    return render_template("admin/pages/index.html")


@login_required
@admin.route("users/")
def users():
    """
    URL: /admin/users/

    method: GET

    Returns a page showing the current users for the system. Non-admin users
    are shown clearly and separately from administrative users.
    """
    users = {"page": 1, "useronly": True, "per_page": 25}
    admins = {"page": 1, "adminonly": True, "per_page": 25}

    # Query the DB for these users.
    users = api.get_users(users)
    admins = api.get_users(admins)

    return render_template("admin/pages/users.html", users=users,
                           admins=admins)


@login_required
@admin.route("user/<int:userid>")
def user(userid):
    """
    URL: /admin/user/<userid>

    Method: GET

    Displays the user identified by the userid passed in the URL. The user can
    be modified from this page.
    """

    user = User.query.filter_by(id=userid).first()
    if not user:
        flash("User does not exist", "error")
        return redirect("/users/")

    form = ModifyUserForm(obj=user)

    return render_template("admin/pages/user.html", form=form, userid=userid)


@login_required
@admin.route("user/<int:userid>", methods=["POST"])
def edit_user(userid):
    """
    URL: /admin/user/<userid>

    Method: Get

    Verifies the submitted data. If verified, converts the submitted data to
    JSON and submits the updated user information to the admin API.

    Returns the user to the main user screen if successful.
    """

    form = UserForm(request.form)

    # Verify the form
    if not form.validate():
        # There are some errors on the form.
        flash_form_errors(form, "error")
        return render_template("admin/pages/user.html", form=form,
                               userid=userid)

    # The form is valid. Convert the form data to JSON and submit it to the
    # API for updating.
    json_form = serialize_user_form(form, userid)
    user = api.edit_user(json_form)

    # Check for errors
    if isinstance(user, dict):
        flash(user, "error")
        return redirect("/admin/users/")

    flash("User Modified", "success")
    return redirect(url_for("admin.users"))


@login_required
@admin.route("user/")
def new_user():
    """
    URL: /admin/user/

    Method: GET

    Displays a new user form so a new user can be created.
    """

    form = UserForm()

    return render_template("admin/pages/newuser.html", form=form)


@login_required
@admin.route("user/", methods=["POST"])
def create_user():
    """
    URL: /admin/user/

    Method: POST

    Creates a new user from the form data passed in.
    """

    form = UserForm(request.form)

    if not form.validate():
        flash_form_errors(form)
        return render_template("admin/pages/newuser.html", form=form)

    json_form = serialize_user_form(form, 0)

    user = api.create_user(json_form)

    if isinstance(user, dict):
        # an error occurred. Flash the error on the screen and return to the
        # new user page.
        flash(user, "error")
        return render_template("admin/pages/newuser.html", form=form)

    flash("User created", "success")
    return redirect(url_for("admin.user", userid=user.id))


@login_required
@admin.route("user/delete/<int:userid>")
def delete_user(userid):
    """
    URL: /admin/user/delete/userid

    Method: GET

    Deletes the user associated with the id specified.

    Parameters:

        userid: int
    """

    result = api.delete_user({"id": userid})

    if isinstance(result, dict):
        flash(result, "error")
    else:
        flash("User Deleted", "success")
    return redirect(url_for("admin.users"))


@login_required
@admin.route("plays/")
def plays():
    """
    URL: /admin/plays/

    Method: GET

    Displays the plays for the admin user to select for further modification.
    """

    plays = api.get_plays({"page": 1, "per_page": 25})
    page = 1

    return render_template("admin/pages/plays.html", plays=plays, page=page)


@login_required
@admin.route("play/")
def new_play():
    """
    URL: /admin/play/

    Method: GET

    Displays the "Create new play" form to the user.
    """
    play_form = PlayForm()
    return render_template("admin/pages/newplay.html", form=play_form)


@login_required
@admin.route("play/", methods=["POST"])
def create_play():
    """
    URL: /admin/play/

    Method: POST

    Creates the Play from the form provided.
    """
    form = PlayForm(request.form)

    if not form.validate():
        flash_form_errors(form, "error")
        return render_template("admin/pages/newplay.html", form=form)

    play = serialize_play_form(form, 0)
    play = api.create_play(play)

    if isinstance(play, dict):
        flash(play, "error")
        return render_template("admin/pages/newplay.html", form=form)

    flash("Play Created", "success")
    return redirect(url_for("admin.play", play_id=play.id))


@login_required
@admin.route("play/<int:play_id>")
def play(play_id):
    """
    URL: /admin/play/<play_id>

    Method: GET

    Displays the play identified by play_id

    Parameters:

        play_id: int
    """

    play = Play.query.filter_by(id=play_id).first()
    reservations = [reservation.seat.id for reservation in play.reservations]

    if not play:
        flash("Play does not exist", "error")
        return redirect(url_for("admin.plays"))

    form = PlayForm(obj=play)

    return render_template("admin/pages/play.html", form=form, play=play,
                           play_id=play_id, reservations=reservations)


@login_required
@admin.route("play/<int:play_id>", methods=["POST"])
def edit_play(play_id):
    """
    URL: /admin/play/<play_id>

    Method: POST

    Edits the play to be consistent with the play form data.

    Parameters:
        play_id: int
    """

    play = Play.query.filter_by(id=play_id).first()

    if not play:
        flash("Play does not exist", "error")
        return redirect(url_for('admin.plays'))

    form = PlayForm(request.form)

    play = serialize_play_form(form, play_id)
    play = api.update_play(play)

    if isinstance(play, dict):
        flash(play, "error")
        return render_template("admin/pages/play.html", form=form,
                               play_id=play_id)

    flash("Play has been updated", "success")
    return redirect(url_for('admin.play', play_id=play.id))


@login_required
@admin.route("user/<int:userid>/password/")
def password(userid):
    """
    URL: /admin/user/<userid>/password/

    Method: GET

    Displays the edit password form for the user with user.id == userid

    Parameters:

        userid: int
    """

    form = PasswordForm()
    return render_template("admin/pages/password.html", form=form,
                           userid=userid)


@login_required
@admin.route("user/<int:userid>/password/", methods=["POST"])
def edit_password(userid):
    """
    URL: /admin/user/<userid>/password

    Method: POST

    Updates the password for the user with user.id == userid
    """

    form = PasswordForm(request.form)

    # Make sure the form is valid
    if not form.validate():
        flash_form_errors(form, "error")
        return render_template("admin/pages/password.html", form=form,
                               userid=userid)

    password = form.password.data
    confirmation = form.confirmation.data

    if not password == confirmation:
        return render_template("admin/pages/password.html", form=form,
                               userid=userid)

    user = {"userid": userid, "password": password,
            "confirmation": confirmation}

    user = api.edit_password(user)

    # The response will be a dict if an error has occurred.
    if isinstance(user, dict):
        flash(user, "error")
        return render_template("admin/pages/password.html", form=form,
                               userid=userid)

    flash("Password updated", "success")
    return redirect(url_for('admin.edit_user', userid=userid))


@admin.route("reporting/", methods=["GET"])
@login_required
def reporting():
    """
    URL: /admin/reporting

    Method: GET

    Returns the page that allows the user to run reports.

    Parameters:
        None

    Returns:
        Template
    """

    return render_template("admin/pages/reporting.html")
