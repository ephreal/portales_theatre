from flask import render_template, Blueprint, request, jsonify
from theatre.routes.api import client as api
from theatre.routes.route_functions import serialize_play, serialize_seat
from theatre.routes.route_functions import serialize_date, serialize_time
from theatre.routes.route_functions import serialize_reservation


client_api = Blueprint("client_api", __name__, url_prefix="/api/client")


@client_api.route("/api/client/test")
def test():
    return render_template("client/test.html")


# The client needs to be able to do the following
# 1) View plays
# 2) view Seats
# 3) Reserve Seats
# 4) Un-reserve seats
# 5) Give payment information
# 6) Check if a reservation already exists

# Play viewing
@client_api.route("/play/<play_id>", methods=["GET"])
def get_play(play_id):
    """
    URL: /api/client/play/play_id

    Method: GET

    Returns the play with id == play_id for the user to view.

    | Parameters:
    |     play_id: int

    | Returns:
    |     JSON String
    """
    play = api.get_play(play_id)

    if not play:
        return {"error": "Play not found."}, 404
    return serialize_play(play), 200


@client_api.route("/play/", methods=["POST"])
def create_play():
    """
    URL: /api/client/play/

    Method: POST

    Explicitly a denied action. Customers are not allowed to create plays.

    | Parameters:

    | Returns:
    |     JSON String
    """
    return {"error": "You must be an administrator to do this."}, 403


@client_api.route("/play/<play_id>", methods=["PUT"])
def update_play(play_id):
    """
    URL: /api/client/play/play_id

    Method: POST

    Explicitly a denied action. Customers are not allowed to modify plays.

    | Parameters:
    |     play_id: int

    | Returns:
    |     JSON String
    """
    return {"error": "You must be an administrator to do this."}, 403


@client_api.route("/play/<play_id>", methods=["DELETE"])
def delete_play(play_id):
    """
    URL: /api/client/play_id

    Method: DELETE

    Explicitly a denied action. Customers are not allowed to delete plays.

    | Parameters:
    |     play_id: int

    | Returns:
    |     JSON String
    """
    return {"error": "You must be an administrator to do this."}, 403


@client_api.route("/seat/<seat_id>", methods=["GET"])
def get_seat(seat_id):
    """
    URL: /api/client/seat/seat_id

    Method: GET

    Returns the seat with id == seat_id for the user to view.

    | Parameters:
    |     seat_id: int

    | Returns:
    |     JSON String
    """
    seat = api.get_seat(seat_id)

    if not seat:
        return {"error": "Seat not found."}, 404
    return serialize_seat(seat), 200


@client_api.route("/seat/", methods=["POST"])
def create_seat():
    """
    URL: /api/client/seat/

    Method: POST

    Explicitly a denied action. Customers are not allowed to create seats.

    | Parameters:

    | Returns:
    |     JSON String
    """
    return {"error": "You must be an administrator to do this."}, 403


@client_api.route("/seat/<seat_id>", methods=["PUT"])
def update_seat(seat_id):
    """
    URL: /api/client/seat/seat_id

    Method: PUT

    A denied action. Non-admin users may not directly modify seats.

    | Parameters:
    |     seat_id: int

    | Returns:
    |     JSON String
    """
    return {"error": "You must be an administrator to do this"}, 403


@client_api.route("/seat/<seat_id>", methods=["DELETE"])
def delete_seat(seat_id):
    """
    URL: /api/client/seat/seat_id

    Method: DELETE

    Explicitly a denied action. Customers are not allowed to delete seats.

    | Parameters:
    |     seat_id: int

    | Returns:
    |     JSON String
    """
    return {"error": "You must be an administrator to do this."}, 403


@client_api.route(
    "/reservations/<int:play_id>/<int:date_id>/<int:time_id>",
    methods=["GET"]
)
def get_reservations(play_id, date_id, time_id):
    """
    URL: /api/client/reservations/play_id/date_id/time_id

    Method: GET

    Parameters:

        None

    Returns:

        JSON String (error OR Reservations)
    """

    result = api.get_reservations(play_id, date_id, time_id)

    if isinstance(result, dict):
        return result

    reservations = [serialize_reservation(item) for item in result]
    return {"reservations": reservations}, 200


@client_api.route("/reservations/by_date/<date>")
def get_reservations_by_date(date):
    """
    URL: /api/client/reservations/by_date/<date>

    Method: GET

    | Parameters:
    |     date: YYYY-MM-DD formatted date

    | Returns:
    |     JSON String (error or Reservations)
    """
    reservations = api.get_reservations_by_date(date)

    if isinstance(reservations, dict):
        return reservations, reservations['status']

    stringified = []
    for reservation in reservations:
        stringified.append(serialize_reservation(reservation))

    return jsonify(stringified), 200


@client_api.route("/reservation/", methods=["POST"])
def make_reservation():
    """
    URL: /api/client/reservation/

    Method: POST

    Parameters:

        None

    Returns:

        JSON String (error OR Reservation)
    """

    JSON = request.get_json()

    reservation = api.create_reservation(JSON)

    # Check for errors.
    if isinstance(reservation, dict):
        return reservation

    # Otherwise, the reservation was created alright
    return serialize_reservation(reservation), 200


@client_api.route("/reservation/", methods=["DELETE"])
def remove_reservation():
    """
    URL: /api/client/reservation/

    Method: DELETE

    | Parameters:
    |     None

    | Returns:
    |     JSON String (error OR Reservation)
    """

    JSON = request.get_json()

    result = api.delete_reservation(JSON)

    # This receives a JSON dict no matter what happens
    return result, 200


@client_api.route("/reservation/<int:seat_id>/<int:date_id>/<int:time_id>")
def check_reservation(seat_id, date_id, time_id):
    """
    URL: /api/client/reservation/<seat_id>/<date_id>/<time_id>

    Method: GET

    | Parameters:
    |     seat_id: int
    |     date_id: int
    |     time_id: int

    | Returns:
    |     JSON String
    """

    reservation = api.check_reservation(seat_id, date_id, time_id)

    if isinstance(reservation, dict):
        return reservation, reservation['status']

    return serialize_reservation(reservation)


@client_api.route("/date/<int:date_id>")
def get_date(date_id):
    """
    URL: /api/client/date/<date_id>

    Method: GET

    | Parameters:
    |    date_id: int

    | Returns:
    |     JSON String
    """
    date = api.get_date(date_id)

    if isinstance(date, dict):
        return date, date['status']

    return serialize_date(date, False)


@client_api.route("/time/<int:time_id>")
def get_time(time_id):
    """
    URL: /api/client/date/<time_id>

    Method: GET

    | Parameters:
    |    time_id: int

    | Returns:
    |     JSON String
    """
    time = api.get_time(time_id)

    if isinstance(time, dict):
        return time, time['status']

    return serialize_time(time, False)
