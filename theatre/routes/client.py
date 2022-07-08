from flask import render_template, Blueprint, request, flash, redirect, url_for
from theatre.app import models, db
from flask_login import login_required, current_user
from theatre.forms import PasswordForm, ModifyUserForm
from theatre.routes.route_functions import flash_form_errors


User = models.User


client = Blueprint("client", __name__)


@client.route("/user/password/")
@login_required
def password():
    """
    URL: /user/password

    Method: GET

    Displays the user password form that allows the current user to change
    their password.
    """

    form = PasswordForm()
    return render_template("client/password.html", form=form)


@client.route("/user/password/", methods=["POST"])
@login_required
def change_password():
    """
    URL: /user/password

    Method: POST

    Changes the currently logged in user's password (assuming it matches the
    confirmation field)
    """

    form = PasswordForm(request.form)

    # Check to make sure the form is valid
    if not form.validate():
        flash_form_errors(form, "error")
        return render_template("client/password.html", form=form)

    # Make sure the password matches the confirmation
    if not form.password.data == form.confirmation.data:
        flash("Password does not match confirmation", "error")
        return render_template("client/password.html", form=form)

    # Update the user's password
    current_user.password = form.password.data
    db.session.add(current_user)
    db.session.commit()

    flash("Password Changed", "success")
    return redirect(url_for('client.user_info'))


@client.route("/user/", methods=["GET"])
@login_required
def user_info():
    """
    URL: /user/

    Method: GET

    Displays the information about the currently logged in user. The user may
    change the info from this screen.
    """

    form = ModifyUserForm(obj=current_user)
    return render_template("client/user_info.html", form=form)


@client.route("/checkout/")
@login_required
def checkout():
    """
    URL: /checkout/

    Method: GET

    Displays the reservations currently in the cart to the user and allows the
    user to remove items from the cart or proceed with the purchase.
    """

    return render_template("client/checkout.html")


@client.route("/user/", methods=["POST"])
@login_required
def update_user():
    """
    URL: /user/

    Method: POST

    Updates the user information with the posted data.
    """

    form = ModifyUserForm(request.form)

    # Make sure the form validates. If not, return an error.
    if not form.validate():
        flash_form_errors(form, "error")
        return render_template("client/user_info.html", form=form)

    # Otherwise, update the current user's information
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    current_user.address = form.address.data
    current_user.apartment = form.apartment.data
    current_user.city = form.city.data
    current_user.state = form.state.data
    current_user.zip_code = form.zip_code.data

    db.session.add(current_user)
    db.session.commit()

    flash("User information has been updated!", "success")
    return render_template("client/user_info.html", form=form)


@client.route("/checkout_success/")
@login_required
def checkout_success():
    """
    URL: /checkout_succes/

    Method: GET

    Returns a template that uses javascript to display the reservations that
    the user has just successfully made.

    If no reservations exist in the local storage, this page will not show any
    information.
    """

    return render_template("client/checkout_success.html")
