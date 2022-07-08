from theatre import models, db
from theatre.routes.api.shared import get_play, get_seat, json_checker
from theatre.routes.api import shared
from flask_login import current_user
from datetime import datetime

# This file implements the report API

Date = models.Date
Play = models.Play
Reservation = models.Reservation
User = models.User
Time = models.Time


def reservations_by_date(date):
    """
    Assuming that date is a string representing a date formatted in iso8601
    (YYYY-MM-DD)
    """
    date = datetime.strptime(date, "%Y-%m-%d").date()
    reservations = Reservation.query.filter_by(reserved=date).all()

    return reservations


def reservations_by_date_range(start_date, end_date):
    """
    Gets a list of all dates within the ranges specified (inclusive).

    | Parameters:
    |     start_date: string (YYYY-MM-DD)
    |     end_date: string (YYYY-MM-DD)

    | Returns:
    |     Dict (error) or list (Dates)
    """

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    reservations = Reservation.query.filter(
        Reservation.reserved >= start_date).filter(
        Reservation.reserved <= end_date).all()

    return reservations


def reservations_by_time(time):

    """
    Assuming that time is a string reprenting a time formatted in %H:%M
    Returns reservations
    """
    time = datetime.strptime(time, "%H:%M")
    times = Time.query.filter_by(time=time).all()
    reservations = []
    for time in times:
        res = Reservation.query.filter_by(time_id=time.id).all()
        reservations.extend(res)

    return reservations
