from theatre import models
from werkzeug.security import check_password_hash
from flask_login import login_user

# This file implements any shared functionality between both the administrative
# and client API. This way, any we do not need to change items in two different
# locations. That's just begging for making mistakes.

Date = models.Date
Play = models.Play
Seat = models.Seat
Time = models.Time
User = models.User


def get_plays(modifiers):
    """
    By default, returns the first 25 plays. This can be changed by passing in
    various modifiers.

    | Parameters:
    |     modifiers: JSON {page, per_page}

    | Returns:
    |     None or list(Plays)
    """
    try:
        page = modifiers['page']
    except KeyError:
        # Return the first page
        page = 1

    try:
        per_page = modifiers['per_page']
    except KeyError:
        per_page = 25

    plays = Play.query.order_by(Play.id.desc()).paginate(page=page,
                                                         per_page=per_page)

    return plays.items


def get_play(play_id):
    """
    Gets a single play and returns the play to the caller. If no play exists,
    returns None.

    | Parameters:
    |     play_id: int

    | Returns:
    |     Play or "error"
    """
    play = Play.query.filter_by(id=play_id).first()
    if not play:
        return None
    return play


def get_seat(seat_id):
    """
    Gets a single seat and returns the seat to the caller. If no seat exists,
    returns None.

    | Parameters:
    |     seat_id: int

    | Returns:
    |     Play or None
    """
    seat = Seat.query.filter_by(id=seat_id).first()
    if not seat:
        return None

    return seat


def get_times(play_id):
    """
    Returns a list of times for a play identified by play_id.

    | Parameters:
    |     play_id: int

    | Returns:
    |     Error or [Times]
    """

    # Make sure the play exists
    play = Play.query.filter_by(id=play_id)

    if not play:
        return {404: "Play not found."}

    return play.times


def get_date(date_id):
    """
    Returns a date object for use.

    | Parameters:
    |     date_id

    | Returns:
    |     Error or Date
    """

    # Make sure the date exists
    date = Date.query.filter_by(id=date_id).first()

    if not date:
        return {"error": "Date not found", "status": 404}

    return date


def get_time(time_id):
    """
    Returns a time object for use.

    | Parameters:
    |     time_id

    | Returns:
    |     Error or Time
    """

    # Make sure the time exists
    time = Time.query.filter_by(id=time_id).first()

    if not time:
        return {"error": "Time not found", "status": 404}

    return time


def login(user_info):
    """
    Attempts to log the user in with the information provided.

    | Parameters:
    |     user_info: JSON {email, password}

    | Returns:
    |     None, False, or User
    """

    # Check to see if the user exists.
    try:
        email = user_info['email']
    except KeyError:
        return None

    user = User.query.filter_by(email=email).first()
    if not user:
        return None

    # Check to see if the password provided matches the user's password
    try:
        password = user_info['password']
    except KeyError:
        return None

    if not check_password_hash(user.password, password):
        return None

    # At this point, the user has authenticated. Log them in.
    login_user(user)
    return user


def json_checker(json, key, default):
    """
    Checks the json passed in to determine if a given key exists or not.

    If the key does not exist, the default value will be returned.

    In the case the default is None, None will be returned. It is up to the
    calling function to verify that required values passed back are not None.

    | Parameters:
    |     json: dict
    |     key: String
    |     default: Any data type

    | Returns
    |     default OR json[key]
    """

    try:
        return json[key]
    except KeyError:
        return default
