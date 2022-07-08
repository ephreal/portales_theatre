from flask import flash


def flash_form_errors(wtform, category):
    """
    Flashes errors in the form so they can be displayed to the user.

    Parameters:

        wtform: A flask-wtf form

        category: A string for the category of the error. Valid categories:
                  error, informational
    """
    for error in wtform.errors.items():
        flash(error, f"{category}")


def serialize_play(play, include_seats=True):
    """
    Turns a play into a json string

    Parameters:

        play: a Play object

    Returns:

        JSON
    """

    json_play = {
        "id": play.id,
        "dates": [serialize_date(date, include_play=False) for date in play.dates],
        "times": [serialize_time(time, include_play=False) for time in play.times],
        "name": play.name
    }

    if include_seats:
        json_play["seats"] = [serialize_seat(seat) for seat in play.seats]
    return json_play


def serialize_seat(seat):
    """
    Turns a seat into a json string.

    Parameters:

        seat: a Seat object

    Returns:

        JSON
    """

    json_seat = {
        "id": seat.id,
        "play": seat.play.id,
        "price": seat.price,
        "row": seat.row,
        "column": seat.column
    }

    return json_seat


def serialize_date(date, include_play=True):
    """
    Turns a Date object into a JSON string.

    Parameters:

        date: Date object

        include_play: Boolean.

    Returns:

        JSON
    """

    json_date = {
        "id": date.id,
        "date": str(date.date)
    }

    if include_play:
        json_date['play'] = serialize_play(date.play)

    return json_date


def serialize_time(time, include_play=True):
    """
    Turns a Time object into a JSON string.

    Parameters:

        time: Time object

        include_play: Boolean.

    Returns:

        JSON
    """

    json_time = {
        "id": time.id,
        "time": str(time.time)
    }

    if include_play:
        json_time['play'] = serialize_play(time.play)

    return json_time


def serialize_reservation(reservation):
    """
    Turns a reservation object into a JSON string.

    Parameters:

        reservation: Reservation object

    Returns:

        JSON
    """

    json_reservation = {
        "id": reservation.id,
        "seat": serialize_seat(reservation.seat),
        "play": serialize_play(reservation.play, include_seats=False),
        "date": serialize_date(reservation.date, include_play=False),
        "time": serialize_time(reservation.time, include_play=False),
        "reserved": reservation.reserved,
        "price": reservation.price
    }

    return json_reservation


def serialize_user_form(form, userid):
    """
    Turns a UserForm object into a JSON string

    Parameters:

        form: UserForm

        userid: int

    Returns

        JSON
    """

    json_form = {
        "id": userid,
        "first_name": form.first_name.data,
        "last_name": form.last_name.data,
        "address": form.address.data,
        "apartment": form.apartment.data,
        "zip_code": form.zip_code.data,
        "city": form.city.data,
        "state": form.state.data,
        "password": form.password.data,
        "confirmation": form.confirmation.data,
        "is_admin": form.is_admin.data,
        "email": form.email.data
    }

    return json_form


def serialize_play_form(play_form, play_id):
    """
    Turns a PlayForm object into a JSON string

    Parameters:

        form: PlayForm

        play_id: int

    Returns

        JSON
    """

    json_form = {
        "id": play_id,
        "name": play_form.name.data,
        "description": play_form.description.data,
        "default_price": play_form.default_price.data,
        "active": play_form.active.data,
        "dates": play_form.dates.data,
        "times": play_form.times.data
    }

    return json_form
