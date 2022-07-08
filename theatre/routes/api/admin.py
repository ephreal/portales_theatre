from theatre import models, db
from theatre.routes.api.shared import get_play, get_seat, json_checker
from theatre.routes.api import shared
from flask_login import current_user

# This file implements the admin API. Any places the admin api is required,
# this file can be imported and used.

Date = models.Date
Play = models.Play
Reservation = models.Reservation
Seat = models.Seat
Time = models.Time
User = models.User


# Bringing some of the shared items to this level for ease of use
def get_plays(modifiers):
    return shared.get_plays(modifiers)


def create_date(date_json):
    """
    Creates a date in the database.

    | Parameters:
    |     date_json: {date, play_id}

    | Returns:
    |     Error or Date
    """

    date = json_checker(date_json, "date", None)
    play_id = json_checker(date_json, "play_id", None)

    if not date:
        return {400: "'date' key is required."}

    if not play_id:
        return {400: "'play' key is required"}

    date = Date(date=date, play_id=play_id)

    db.session.add(date)
    db.session.commit()

    return date


def create_seat(seat_data):
    """
    Creates a seat with the info passed in.

    Returns a dict or the Seat depending on whether or not the seat creation
    was successful.

    | Parameters:
    |     seat_data: JSON {play_id, price, row, column}

    | Returns:
    |     Seat, None
    """

    # Just in case slightly invalid data was sent in, check to see if these
    # values exist or not. We'll assign defaukts where it's sane to do so.
    play_id = json_checker(seat_data, "play_id", None)
    row = json_checker(seat_data, "row", None)
    column = json_checker(seat_data, "column", None)
    price = json_checker(seat_data, "price", 50)

    if not play_id:
        return {400: "'play_id' is required."}

    if not row or not column:
        # Not going to try guess what the row or column were supposed to be
        return {400: "'row' and 'column' are both required."}

    seat = Seat(price=price, play_id=play_id, row=row, column=column)
    db.session.add(seat)
    db.session.commit()

    return seat


def delete_seat(seat_id):
    """
    Deletes a seat and all associated seats.

    | Parameters:
    |     seat_id: int

    | Returns:
    |     None or True
    """

    # Ensure that the seat exists.
    seat = get_seat(seat_id)
    if not seat:
        return None

    # Remove the seat
    db.session.delete(seat)
    db.session.commit()
    return True


def update_seat(seat_id, seat_data):
    """
    Updates a single seat with the json passed in.

    Currently the row/column values are not updated since the seat will most
    likely not be moved around after the seat is created.

    Can return three types of values.

    Seat: The updated version of the seat.

    False: An error occurred in trying to update the seat.

    None: The seat does not exist.

    | parameters:
    |     seat_id: int
    |     seat_data: JSON {price}

    | Returns:
    |     Seat, False, None
    """

    # Attempt to load a seat
    seat = get_seat(seat_id)

    # If the seat does not exist, return None to signify that it does not.
    if not seat:
        return None

    seat.price = json_checker(seat_data, "price", seat.price)

    db.session.add(seat)
    db.session.commit()

    return seat


def create_play(play_data):
    """
    Creates a play with the info passed in.

    The date must be passed in as a formatted string: %Y-%m-%d

    The time must be passed in as a formatted string: %H:%M

    Returns an error or the Play depending on whether or not the play creation
    was successful.

    If no seat information was passed in, this will autogenerate an 8x12 grid
    of seats to go with the play.

    | Parameters:
    |     play_data: JSON: {date, seats: {...}, description, name}

    | Returns:
    |     Play, Dict
    """

    name = json_checker(play_data, "name", None)
    dates = json_checker(play_data, "dates", None)
    times = json_checker(play_data, "times", None)
    description = json_checker(play_data, "description", "")
    default_price = json_checker(play_data, "default_price", 50)
    active = json_checker(play_data, "active", True)
    seats = json_checker(play_data, "seats", None)

    if not name:
        return {400: "'name' key is required."}

    if not dates:
        return {400: "'date' key is required."}

    if not times:
        return {400: "'times' key is required."}

    # Create the play in the database. We must have the play created before
    # we are able to create any seats, dates, or times for it
    play = Play(name=name, description=description,
                default_price=default_price, active=active)
    db.session.add(play)
    db.session.commit()

    if seats:
        seats = list(seats.keys())
        for seat in list(play_data['seats'].keys()):
            create_seat(play_data['seats'][seat])
    else:
        # Create an 8x12 grid of seats.
        for i in range(0, 9):
            for j in range(0, 13):
                seat = {
                    "row": i,
                    "column": j,
                    "price": default_price,
                    "play_id": play.id
                }
                create_seat(seat)

    # Create the dates for this play
    for date in dates:
        date_json = {"date": date['date'], "play_id": play.id}
        create_date(date_json)

    for time in times:
        time_json = {"time": time['time'], "play_id": play.id}
        create_time(time_json)

    return play


def delete_play(play_id):
    """
    Deletes a play and all associated seats.

    | Parameters:
    |     play_id: int

    | Returns:
    |     None or True
    """

    # Ensure that the play exists.
    play = get_play(play_id)
    if not play:
        return None

    # Remove the play
    db.session.delete(play)
    db.session.commit()
    return True


def update_play(play_json):
    """
    Updates the play identified by play_id with the play_json. The play info
    should be JSON data and can be generated with the serialize_play()
    function from routes/route_functions.

    This can return 3 different states.

    Play: The updated play information
    False: The play was unable to be updated (ie: Errors were encountered)
    None: The play requested does not exist.

    | Parameters:
    |     play_id:   int
    |     play_json: JSON {date, seats: {1: {seat JSON}, 2: ...} }

    | Returns:
    |     Play, False, None
    """

    play_id = json_checker(play_json, "id", None)

    if not play_id:
        return {400: "'id' key is required."}

    # Attempt to get a play
    play = get_play(play_id)

    # If no play exists, return None to signify that the play does not exist.
    if not play:
        return {404: "Play not found"}

    play.name = json_checker(play_json, "name", play.name)
    dates = json_checker(play_json, "dates", None)
    times = json_checker(play_json, "times", None)
    play.active = json_checker(play_json, "active", play.active)
    play.description = json_checker(play_json, "description", play.description)
    play.default_price = json_checker(play_json,
                                      "default_price", play.default_price)

    play_dates = [date.date for date in play.dates]
    play_times = [time.time for time in play.times]

    for date in dates:
        if date['date'] is None:
            continue
        if not date['date'] in play_dates:
            date['play_id'] = play.id
            play.dates.append(create_date(date))

    for time in times:
        if time['time'] is None:
            continue
        if not time['time'] in play_times:
            time['play_id'] = play.id
            play.times.append(create_time(time))

    db.session.add(play)
    db.session.commit()

    # Update the seats
    try:
        updated_seats = list(play_json['seats'].keys())
        for seat in updated_seats:
            update_seat(seat, play_json['seats'][seat])
    except KeyError:
        # Updated seat information may not have been passed in. This is ok to
        # skip
        pass

    # Query the database for the updated play.
    # Not entirely necessary, but seems like a good thing to do.
    play = get_play(play_id)
    return play


def create_time(time_json):
    """
    Creates a time in the database.

    | Parameters:
    |     time_json: {time, play_id}

    | Returns:
    |     Error or Date
    """

    time = json_checker(time_json, "time", None)
    play_id = json_checker(time_json, "play_id", None)

    if not time:
        return {"error": "'time' key is required.", "status": 400}

    if not play_id:
        return {"error": "'play' key is required", "status": 400}

    time = Time(time=time, play_id=play_id)

    db.session.add(time)
    db.session.commit()

    return time


def get_reservation(seat_id, date_id, time_id):
    """
    Gets the reservation for the seat at a particular date and time.

    | Parameters:
    |     seat_id: int
    |     date_id: int
    |     time_id: int

    | Returns:
    |     error or Reservation
    """

    # Check to see if the reservation exists
    reservation = Reservation.query.filter_by(seat_id=seat_id, date_id=date_id,
                                              time_id=time_id).first()
    if not reservation:
        return {"error": "No reservation found", "status": 404}

    return reservation


def get_users(modifiers):
    """
    Gets the specified amount of users and returns them to the caller.

    | Parameters:
    |     modifiers: JSON {per_page, page, adminonly, useronly}

    | Returns:
    |     list(Users)
    """

    try:
        per_page = modifiers['per_page']
    except KeyError:
        per_page = 25

    try:
        page = modifiers['page']
    except KeyError:
        page = 1

    try:
        if modifiers['adminonly']:
            return get_admin_users(page, per_page)
    except KeyError:
        pass

    try:
        useronly = modifiers['useronly']
    except KeyError:
        useronly = False

    if useronly:
        users = User.query.filter_by(is_admin=False).paginate(
            page=page, per_page=per_page
        )

    else:
        users = User.query.order_by(User.id).paginate(page=page,
                                                      per_page=per_page)
    return users.items


def get_admin_users(page, per_page):
    """
    Gets the specified amount of administrative users and returns them to the
    caller.

    | Parameters:
    |     page: Which page to get
    |     per_page: How many users to place per page

    | Returns:
    |     list(Users)
    """
    users = User.query.filter_by(is_admin=True).paginate(page=page,
                                                         per_page=per_page)

    return users.items


def create_user(user_json):
    """
    Creates a new user from the JSON passed in.

    Required fields are email, password, confirmation, first_name, last_name

    | Parameters:
    |     user_json: JSON {email, password, confirmation, first_name, ....}

    | Returns:
    |     dict OR User
    """

    email = json_checker(user_json, "email", None)
    first_name = json_checker(user_json, "first_name", None)
    last_name = json_checker(user_json, "last_name", None)
    address = json_checker(user_json, "address", "")
    apartment = json_checker(user_json, "apartment", "")
    zip_code = json_checker(user_json, "zip_code", "")
    city = json_checker(user_json, "city", "")
    state = json_checker(user_json, "state", "")
    is_admin = json_checker(user_json, "is_admin", "")
    password = json_checker(user_json, "password", None)
    confirmation = json_checker(user_json, "confirmation", None)

    if not email:
        return {400: "'email' key is required"}

    if not first_name:
        return {400: "'first_name' key is required."}

    if not last_name:
        return {400: "'last_name' key is required"}

    if not password:
        return {400: "'password' key is required."}

    if not confirmation:
        return {400: "'confirmation' key is required."}

    # Verify that the password and confirmation match
    if not password == confirmation:
        return {400: "Password and password confirmation do not match."}

    # Verify that a user with this email address does not already exist
    user = User.query.filter_by(email=email).first()
    if user:
        return {400: "Email already in use."}

    user = User(email=email, first_name=first_name, last_name=last_name,
                address=address, apartment=apartment, zip_code=zip_code,
                city=city, state=state, is_admin=is_admin, password=password)

    db.session.add(user)
    db.session.commit()
    return user


def edit_password(user_json):
    """
    Edits the password of the specified user.

    | Parameters:
    |     user_json: JSON {userid, password, confirmation}

    | Returns:
    |     User or Error
    """

    user = json_checker(user_json, "userid", None)
    password = json_checker(user_json, "password", None)
    confirmation = json_checker(user_json, "confirmation", None)

    if not user:
        return {"error": "'user' key is required", "status": 400}

    if not password:
        return {"error": "'password' key is required", "status": 400}

    if not confirmation:
        return {"error": "'confirmation' key is required", "status": 400}

    # Check to see if the user exists
    user = User.query.filter_by(id=user).first()

    if not user:
        return {"error": "User not found.", "status": 404}

    # Check that the password and confirmation match

    if not password == confirmation:
        return {"error": "password and confirmation do not match",
                "status": 400}

    # Finally, we can update the user's password
    user.password = password

    db.session.add(user)
    db.session.commit()

    return user


def delete_user(user_json):
    """
    Deletes the user specified by id in the user json.

    | Parameters:
    |     user_json: JSON {id}

    | Returns:
    |     dict OR True
    """

    userid = json_checker(user_json, "id", None)

    if not userid:
        return {400: "'id' is required."}

    # Verify that the user exists.
    user = User.query.filter_by(id=userid).first()

    if user == current_user:
        return {400: "Cannot delete the currently logged in user."}

    db.session.delete(user)
    db.session.commit()

    return True


def edit_user(user_json):
    """
    Edits the user specified by the JSON passed in.

    If any errors arise, the user will not be edited and an error will be
    returned.

    | Parameters:
    |     user_json: {userid, first_name, last_name, address, apartment....}

    | Returns:
    |     dict OR User
    """

    # Check to see if the user even exists.
    try:
        user = User.query.filter_by(id=user_json['id']).first()

        if not user:
            return {404: "User not found."}
    except KeyError:
        return {400: "'id' is required."}

    # Load up all the remaining values.
    email = json_checker(user_json, "email", user.email)
    first_name = json_checker(user_json, "first_name", user.first_name)
    last_name = json_checker(user_json, "last_name", user.last_name)
    address = json_checker(user_json, "address", user.address)
    apartment = json_checker(user_json, "apartment", user.apartment)
    zip_code = json_checker(user_json, "zip_code", user.zip_code)
    city = json_checker(user_json, "city", user.city)
    state = json_checker(user_json, "state", user.state)
    is_admin = json_checker(user_json, "is_admin", user.is_admin)
    password = json_checker(user_json, "password", user.password)

    # Check to see if the user's password is the same as the current password
    if not password == user.password:
        # Gotta check the confirmation as well
        confirmation = json_checker(user_json, "confirmation",
                                    None)

        if not confirmation == password:
            return {400: "Passwords do not match"}

    # Check if the user's email is changing. If so, we need to check and
    # make sure it isn't a duplicate
    if not email == user.email:
        test_user = User.query.filter_by(email=email).first()
        if test_user:
            return {400: "Email address already in use."}

    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.address = address
    user.apartment = apartment
    user.zip_code = zip_code
    user.city = city
    user.state = state
    user.password = password
    user.is_admin = is_admin

    db.session.add(user)
    db.session.commit()
    return user
