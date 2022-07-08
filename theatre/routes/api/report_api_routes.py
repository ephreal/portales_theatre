from flask import Blueprint, request
from flask_login import login_required
from theatre.app import models
from theatre.routes.api import report as api
from theatre.routes.route_functions import serialize_play, serialize_seat
from theatre.routes.route_functions import serialize_reservation


report_api = Blueprint("report_api", __name__, url_prefix="/api/report/")


@report_api.route("date/<date>")
@login_required
def reservations_by_date(date):
    """
    URL: /api/report/date/<date>

    Method: GET

    Gets a list of all reservations that match a specific date. The date must
    be in YYYY-MM-DD formatting.

    Parameters:

        date: string
    """

    reservations = api.reservations_by_date(date)
    reservations = [serialize_reservation(res) for res in reservations]
    return {"reservations": reservations}, 200


@report_api.route("date_range/<start_date>/<end_date>", methods=["GET"])
@login_required
def reservations_by_date_range(start_date, end_date):
    """
    URL: /api/report/date_range/<start_date>/<end_date>

    Method: GET

    Gets a list of all reservations within a specific date range.

    | Parameters:
    |     start_date: string (YYYY-MM-DD)
    |     end_date: string (YYYY-MM-DD)

    | Returns:
    |     JSON
    """

    reservations = api.reservations_by_date_range(start_date, end_date)
    reservations = [serialize_reservation(res) for res in reservations]
    return {"reservations": reservations}, 200


@report_api.route("time/<time>")
@login_required
def report_by_time(time):
    """URL: /api/report/time/<time>

    Method: GET

    Gets a list of all reservations that match a specific time. The time must
    be in a HH:MM format.

    Parameters:

        time: string
    """
    report = api.reservations_by_time(time)
    return {"report": report}, 200
