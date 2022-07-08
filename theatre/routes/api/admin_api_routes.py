from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from theatre.app import models
from theatre.routes.api import admin as api
from theatre.routes.route_functions import serialize_play, serialize_seat
from theatre.routes.route_functions import serialize_reservation
"""
The admin API needs to allow the admin user to do the following:
1) Create plays
2) Edit plays
3) Delete plays
4) Edit Seats in plays
5) Run reports

The API uses different HTTP requests to determine what to do with an API
request. For example, in the case of plays,
1) GET = get an instance of a play
2) POST = creates a new play
3) PUT = updates a play with new information
4) DELETE = removes a play

The primary communication methodology between the frontend and the backend
will be over HTTP(S) with data being transferred as JSON where required.

Since HTTP forms submitted by browsers do NOT have a way of sending anything
other than GET/POST requests, we will have to use a little bit of javascript
to ensure that the forms are sent with the proper HTTP method.

Places where this could use a LOT of improvement:

Error messages SHOULD be made to be more actionable. Right now, they are
very generic. This is because I didn't have time to work on them more.
"""


db = models.db


admin_api = Blueprint("admin_api", __name__, url_prefix="/api/admin/")


@admin_api.before_request
def check_admin():
    """
    Checks to see if the current user is an administrator.

    If the user is not an administrator, it redirects them to the site's index
    page.
    """
    try:
        if not current_user.is_admin:
            return {"error": "Unauthorized"}, 403
    except AttributeError:
        return {"error": "Unauthorized"}, 403


# Test route that we can use to verify that the API is accessible.
@admin_api.route("test/")
@login_required
def test_route():
    """
    URL: /api/admin/test/

    Method: GET

    Test route to verify that the api is responsive. Returns the API version.

    Paramters:

    | Returns:
    |     JSON {api_version}
    """

    # Apparently flask automatically converts non-template returns to JSON.
    # Very handy to know.
    # The number after the tuple will be the HTTP status code.

    return {"api_version": "1.0.0"}, 200


# Play creation.
@admin_api.route("play/", methods=["POST"])
@login_required
def create_play():
    """
    URL: /admin/api/play/

    Method: POST

    Creates a new play. The play information is created with any information
    that is passed in the POST request.

    Parameters:

    | Returns:
    |     JSON String
    """
    play = api.create_play(request.get_json())

    if play is None:
        return {"error": "Invalid play data"}, 400

    if isinstance(play, dict):
        # An error was returned.
        return jsonify(play)
    return serialize_play(play), 200


# Play viewing.
@admin_api.route("play/<play_id>", methods=["GET"])
@login_required
def get_play(play_id):
    """
    URL: /api/admin/play/play_id

    Method: GET

    Gets information about the play with id == play_id.

    | Parameters:
    |     play_id: int

    | Returns:
    |     JSON String
    """
    play = api.get_play(play_id)

    if not play:
        return {"error": f"Play {play_id} not found"}, 404
    return serialize_play(play), 200


# Play modification.
@admin_api.route("play/<play_id>", methods=["PUT"])
@login_required
def update_play(play_id):
    """
    URL: /admin/api/play/play_id

    Method: PUT

    Updates the play with id == play_id.

    | Parameters:
    |     play_id: int

    | Returns:
    |     JSON String
    """

    play = api.get_play(play_id)

    if not play:
        return {"error", "Play does not exist."}, 404

    play = api.update_play(request.get_json(), play_id)

    # If any errors occured, this will already be a dict
    if isinstance(play, dict):
        return jsonify(play)

    return serialize_play(play), 200


# Play deletion.
@admin_api.route("play/<play_id>", methods=["DELETE"])
@login_required
def delete_play(play_id):
    """
    URL: /admin/api/play/play_id

    Method: POST

    Deletes the play with id == play_id

    | Parameters:
    |     play_id: int

    | Returns:
    |     JSON String
    """

    result = api.delete_play(play_id)

    if not result:
        return {"error": f"Play {play_id} does not exist."}, 404

    return {"error": f"Play number {play_id} deleted"}, 200


# Seat creation.
@admin_api.route("seat/", methods=["POST"])
@login_required
def create_seat():
    """
    URL: /admin/api/seat/

    Method: POST

    Creates a new play. The seat information is created with any information
    that is passed in the POST request.

    | Parameters:

    | Returns:
    |     JSON String
    """
    JSON = request.get_json()
    # A seat must pass in which play it is linked to
    try:
        play = api.get_play(JSON['play'])
        if not play:
            return {"error": "Play does not exist."}, 404
    except KeyError:
        return {"error": "'play' key is required."}, 400

    seat = api.create_seat(JSON, play)

    # The seat data will be a dict if any errors have occurred.
    if isinstance(seat, dict):
        return jsonify(dict)
    return serialize_seat(seat), 200


# Seat viewing.
@admin_api.route("seat/<seat_id>", methods=["GET"])
@login_required
def get_seat(seat_id):
    """
    URL: /admin/api/seat/seat_id

    Method: GET

    Gets information about the seat with the id == seat_id.

    | Parameters:
    |     seat_id: int

    | Returns:
    |     JSON String
    """
    seat = api.get_seat(seat_id)
    if not seat:
        return {"error": f"Seat {seat_id} not found"}, 404
    return serialize_seat(seat), 200


# Seat modification.
@admin_api.route("seat/<seat_id>", methods=["PUT"])
@login_required
def update_seat(seat_id):
    """
    URL: /api/admin/seat/seat_id

    Method: PUT

    Updates the seat with the id == seat_id.

    | Parameters:
    |     seat_id: int

    | Returns:
    |     JSON String
    """

    JSON = request.get_json()
    seat = api.update_seat(seat_id, JSON)

    if not seat:
        return {"error": "Error creating seat"}, 400

    return serialize_seat(seat), 200


# Seat deletion.
@admin_api.route("seat/<seat_id>", methods=["DELETE"])
@login_required
def delete_seat(seat_id):
    """
    URL: /api/admin/seat/seat_id

    Method: DELETE

    Deletes the seat with id == seat_id

    | Parameters:
    |     seat_id: int

    | Returns:
    |     JSON String
    """
    result = api.delete_seat(seat_id)
    if not result:
        return {"error": f"Play {seat_id} does not exist."}, 404
    return {"success": f"Play number {seat_id} deleted"}, 200


@admin_api.route(
    "reservation/<int:seat_id>/<int:date_id>/<int:time_id>",
    methods=["GET"]
    )
@login_required
def get_reservation(seat_id, date_id, time_id):
    """
    URL: /api/admin/reservation/seat_id/date_id/time_id

    Method: GET

    | Parameters:
    |     seat_id: int
    |     date_id: int
    |     time_id: int

    | Returns:
    |     JSON
    """

    reservation = api.get_reservation(seat_id, date_id, time_id)

    if isinstance(reservation, dict):
        return {"error": reservation['error']}, reservation['status']

    return serialize_reservation(reservation)


@admin_api.route("play/int:<play_id>/times/")
@login_required
def get_play_times(play_id):
    """
    URL: /api/admin/play/<play_id>/times/

    Method: GET

    | Parameters:
    |     play_id: int

    | Returns:
    |     JSON String
    """

    pass
