from flask import render_template, Blueprint, redirect, flash, request
from theatre.forms import UserForm
from theatre.routes.api.shared import get_plays, get_play
from theatre import models
from theatre.routes.api import admin as adminapi
from theatre.routes.route_functions import serialize_user_form

User = models.User
Reservation = models.Reservation


theatre = Blueprint("theatre", __name__)


@theatre.route("/")
def index():
    return render_template("theatre/pages/index.html")


@theatre.route("/about/")
def about():
    """
    Displays information about the site.
    """
    return render_template("theatre/pages/about.html")


@theatre.route("/plays/<int:page_num>")
def plays(page_num):
    """
    Displays the available plays to the user.
    """
    if page_num < 1:
        return render_template("theatre/pages/joke.html")
    plays = get_plays({"page": page_num})
    return render_template("theatre/pages/plays.html", plays=plays)


@theatre.route("/plays/")
def plays_page_one():
    """
    Displays the first page of the available plays to the user.
    """

    plays = get_plays({"page": 1})
    return render_template("theatre/pages/plays.html", plays=plays)


@theatre.route("/play/<int:play_number>")
def play(play_number):
    """
    Displays a single play to the user.
    """

    play = get_play(play_number)
    # This reservations query should be moved into the api in the future.
    # For now, I'm just testing.
    reservations = Reservation.query.filter_by(play=play)
    reservations = [res.seat.id for res in reservations]
    return render_template("theatre/pages/play.html", play=play,
                           reservations=reservations)


@theatre.route("/setup/", methods=["GET"])
def setup():
    """
    Handles all the post-install configuration.

    Currently, this just includes creating the administrative user.
    """

    user = User.query.filter_by(is_admin=True).first()
    form = UserForm()
    form.is_admin.data = True

    if user:
        flash("Admin user has already been made", "informational")
        return redirect("/")

    return render_template("theatre/pages/setup.html", form=form)


@theatre.route("/setup/", methods=["POST"])
def complete_setup():
    """
    Completes the setup of the administrative user by actually creating the
    user POST-ed to the URL.
    """
    # First check and see if an admin user already exists. If not, then there
    # is no reason to run this at all. Besides, if an admin user already
    # exists, then someone may be trying to do something nefarious and create
    # admin users without logging in.
    user = User.query.filter_by(is_admin=True).first()
    if user:
        flash("Admin user has already been made", "informational")
        return redirect("/")

    form = UserForm(request.form)
    form.is_admin.data = True

    user = serialize_user_form(form, 0)

    user = adminapi.create_user(user)

    if isinstance(user, dict):
        flash(user, "error")
        return render_template("theatre/pages/setup.html", form=form)

    flash("Admin created", "success")
    return redirect("/")
