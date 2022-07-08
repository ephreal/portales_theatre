from theatre import models, db
from theatre.routes.api import shared
from werkzeug.security import generate_password_hash
from flask_login import current_user
from datetime import datetime


# This file implements the client API. Any places the client api is required,
# this file can be imported and used.

Date = models.Date
User = models.User
Play = models.Play
Reservation = models.Reservation
Seat = models.Seat
Time = models.Time


# Bringing the shared functions to the top level for ease of access
# View shared.py for information on what these do.
def get_play(play_id):
    return shared.get_play(play_id)


def get_seat(seat_id):
    return shared.get_seat(seat_id)


def get_plays(modifiers):
    return shared.get_plays(modifiers)


def get_date(date_id):
    return shared.get_date(date_id)


def get_time(time_id):
    return shared.get_time(time_id)


# Implementing the other parts of the API specific to the client

def register(user_data):
    """
    Registers a user in the database.

    | Parameters:
    |     user_data: JSON {
    |                      email, password, confirmation, first_name, last_name
    |                     }

    | Returns:
    |     User or False
    """

    # First check to see if the user already exists in the database.
    # The user's email address MUST be unique.
    user = User.query.filter_by(email=user_data['email'])
    if user:
        # Cannot create a new user. Email address is not unique
        return False

    password = user_data['password']
    confirmation = user_data['confirmation']

    if not password == confirmation:
        # The user password does not match the confirmation
        return False

    password = generate_password_hash(password, method='pbkdf2:sha256',
                                      salt_length=16)

    user = User(first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=password,
                is_admin=False
                )

    db.session.add(user)
    db.session.commit()

    return user


def get_reservations(play_id, date_id, time_id):
    """
    Gets the reservations for a play at a specific date and time.

    Notably, this does not accept all items as single JSON input.

    | Parameters:
    |     play_id: int
    |     date_id: int
    |     time_id: int

    | Returns:
    |     dict OR [Reservation]
    """

    # Make sure the play, date, and time exist.
    play = Play.query.filter_by(id=play_id).first()
    date = Date.query.filter_by(id=date_id).first()
    time = Time.query.filter_by(id=time_id).first()

    if not play:
        return {"error": "Play not found.", "status": 404}

    if not date:
        return {"error": "Date not found.", "status": 404}

    if not time:
        return {"error": "Time not found.", "status": 404}

    reservations = Reservation.query.filter_by(
        play=play, date=date, time=time
    ).all()

    return reservations


def check_reservation(seat_id, date_id, time_id):
    """
    Checks to see if a reservation exists.

    | Parameters:
    |     seat_id: int
    |     date_id: int
    |     time_id: int

    | Returns:
    |     Error or Reservation
    """

    # make sure the seat, date, and time truly exist
    seat = Seat.query.filter_by(id=seat_id).first()
    date = Date.query.filter_by(id=date_id).first()
    time = Time.query.filter_by(id=time_id).first()

    if not seat:
        return {"error": "Seat not found.", "status": 404}

    if not date:
        return {"error": "Date not found.", "status": 404}

    if not time:
        return {"error": "Time not found.", "status": 404}

    # Then check to see if this reservation already exists.
    reservation = Reservation.query.filter_by(
        seat=seat,
        date=date,
        time=time,
        play=seat.play,
    ).first()

    if not reservation:
        return {"error": "Reservation not found", "status": 404}

    return reservation


def get_reservations_by_date(date):
    """
    Gets the reservations for the current user on the specified date.

    Parameters:
        date: String (YYYY-MM-DD)

    Returns:
        dict or [Reservations]
    """

    # Check to see if the currently active user is logged in.
    if not current_user.is_authenticated:
        return {"error": "You must be logged in", "status": 401}

    # The user is logged in. We can search the user's reservations for any
    # date matching the date passed in.
    date = datetime.strptime(date, "%Y-%m-%d").date()
    reservations = []

    for reservation in current_user.reservations:
        if reservation.reserved == date:
            reservations.append(reservation)
    return reservations


def create_reservation(reservation_json):
    """
    Reserves a seat.

    | Parameters:
    |     reservation_json: JSON {seat_id, date_id, time_id}

    | Returns
    |     Error or Reservation
    """

    # The user must be logged in to make a reservation
    if not current_user.authenticated:
        return {"error": "You must be logged in to make a reservation.",
                "status": 401}

    seat_id = shared.json_checker(reservation_json, "seat_id", None)
    date_id = shared.json_checker(reservation_json, "date_id", None)
    time_id = shared.json_checker(reservation_json, "time_id", None)
    reserved = datetime.utcnow().date()

    if not seat_id:
        return {"error": "'seat_id' is required.", "status": 400}

    if not date_id:
        return {"error": "'sate_id' is required.", "status": 400}

    if not time_id:
        return {"error": "'time_id' is required.", "status": 400}

    # Next make sure the seat, date, and time truly exist
    seat = Seat.query.filter_by(id=seat_id).first()
    date = Date.query.filter_by(id=date_id).first()
    time = Time.query.filter_by(id=time_id).first()

    if not seat:
        return {"error": "Seat not found.", "status": 404}

    if not date:
        return {"error": "Date not found.", "status": 404}

    if not time:
        return {"error": "Time not found.", "status": 404}

    # Then check to see if this reservation already exists.
    reservation = Reservation.query.filter_by(
        seat=seat,
        date=date,
        time=time,
        play=seat.play
    ).first()

    if reservation:
        return {"error": "This seat has already been reserved.", "status": 400}

    # Finally, we can make our reservation
    reservation = Reservation(seat=seat,
                              date=date,
                              time=time,
                              user=current_user,
                              play=seat.play,
                              price=seat.price,
                              reserved=reserved)

    db.session.add(reservation)
    db.session.commit()
    return reservation


def delete_reservation(reservation_json):
    """
    Removes a reservation that matches the date, time, and seat for the
    current user. If the current user has not made that reservation, the
    reservation will not be removed.

    | Parameters:
    |     reservation_json: JSON {seat_id, date_id, time_id}

    | Returns:
    |     dict (either success or error)
    """

    # The user must be logged in to make a reservation
    if not current_user.authenticated:
        return {"error": "You must be logged in to make a reservation.",
                "status": 401}

    seat_id = shared.json_checker(reservation_json, "seat_id", None)
    date_id = shared.json_checker(reservation_json, "date_id", None)
    time_id = shared.json_checker(reservation_json, "time_id", None)

    if not seat_id:
        return {"error": "'seat_id' is required.", "status": 400}

    if not date_id:
        return {"error": "'sate_id' is required.", "status": 400}

    if not time_id:
        return {"error": "'time_id' is required.", "status": 400}

    # Next make sure the seat, date, and time truly exist
    seat = Seat.query.filter_by(id=seat_id).first()
    date = Date.query.filter_by(id=date_id).first()
    time = Time.query.filter_by(id=time_id).first()

    if not seat:
        return {"error": "Seat not found.", "status": 404}

    if not date:
        return {"error": "Date not found.", "status": 404}

    if not time:
        return {"error": "Time not found.", "status": 404}

    # Then check to see if this reservation already exists.
    reservation = Reservation.query.filter_by(
        seat=seat,
        date=date,
        time=time,
        play=seat.play,
        user=current_user
    ).first()

    if not reservation:
        return {"error": "Reservation not found.", "status": 404}

    db.session.delete(reservation)
    db.session.commit()
    return {"success": "Reservation removed.", "status": 200}
