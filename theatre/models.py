from flask_sqlalchemy import SQLAlchemy
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import widgets
db = SQLAlchemy()


# Our base user class. View the flask-login documentation for what the
# UserMixin class provides.
class User(db.Model, UserMixin):
    """
    | id:            The primary key for the user
    | authenticated: Whether or not the user has logged in.
    | password:      A password hashed with werkzeug.generate_password_hash
    | email:         A string containing the user's email address
    | first_name:     A string containing the user's first name
    | last_name:     A string containing the user's last name
    | is_admin:      A boolean determining whether or not the user is an admin
    | address:       User Address
    | apartment:     The apartment number or letter for the user's address
    | zip_code:      The zip code for the customer's address
    | state:         The state that the user lives in.
    | city:          The city that the user lives in
    | reservations:  Any reservation the user has made for a play
    """
    id = db.Column(db.Integer, primary_key=True)
    authenticated = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, default=False)
    address = db.Column(db.String(256))
    apartment = db.Column(db.String(32))
    zip_code = db.Column(db.String(16))
    state = db.Column(db.String(16))
    city = db.Column(db.String(64))
    reservations = db.relationship("Reservation", backref="user",
                                   lazy="select")

    @property
    def is_authenticated(self):
        return self.authenticated

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def password(self):
        return self.password_hash

    def get_id(self):
        return self.id

    def hash_password(self, password):
        """
        Hashes the password passed in and returns it to the caller.

        | Parameters:
        |     password: unhashed, cleartext string

        | Returns:
        |     password: Hashed password
        """

        password = generate_password_hash(password, method='pbkdf2:sha256',
                                          salt_length=16)

        return password

    @password.setter
    def password(self, password):
        """
        Updates the password on the user model.

        | Parameters:
        |     password: unhashed, cleartext string

        | Returns:
        |     None
        """

        # password = self.hash_password(password)
        self.password_hash = self.hash_password(password)

    def check_password(self, password):
        """
        Checks to see if the password provided matches the current password
        for the user.

        Parameters:

            password: unhashed, cleartext string

        Returns:

            None
        """

        if check_password_hash(self.password_hash, password):
            return True
        return False


# Our seat object
class Seat(db.Model):
    """
    | id:        The id of the seat
    | price:     The cost of the seat.
    | play_id:   The play that is associated with this seat.
    | row:       The row that the seat is in. 0 is the closest to the stage.
    | column:    The column that the seat is in. 0 is the furthest left.

    | Backref Mappings
    |     reservations: The that have been made for this seat
    """
    id = db.Column(db.Integer, primary_key=True)
    column = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), default=0)
    row = db.Column(db.Integer, nullable=False)
    play_id = db.Column(db.Integer, db.ForeignKey("play.id"))
    reservations = db.relationship("Reservation", backref="seat",
                                   lazy="select")


# Our play object
class Play(db.Model):
    """
    | id:            The id of the play
    | dates:         The dates the play will show
    | times:         The times the play will show on the dates
    | default_price: The default price for the seats in this play
    | name:          The name of the play
    | seats:         The seats associated with this play
    | active:        Whether or not the play is active (can have seats
    |                reserved)
    | description:   Description of what the play will be about.
    | reservations:  seats that have been reserved for a particular date and
    |                time
    """
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True, info={"label": "Active?"})
    default_price = db.Column(db.Numeric(10, 2), default=0,
                              info={"label": "Default Price"})
    description = db.Column(db.String(4096),
                            info={"label": "Description",
                                  "widget": widgets.TextArea()})
    name = db.Column(db.String(256), nullable=False, info={'label': "Name"})
    seats = db.relationship("Seat", backref="play", lazy="select",
                            cascade="all, delete, delete-orphan")
    dates = db.relationship("Date", backref="play", lazy="select",
                            cascade="all, delete, delete-orphan")
    times = db.relationship("Time", backref="play", lazy="select",
                            cascade="all, delete, delete-orphan")
    reservations = db.relationship("Reservation", backref="play",
                                   cascade="all, delete, delete-orphan",
                                   lazy="select")


class Reservation(db.Model):
    """
    Allows us to easily access the times and dates that a seat for a play has
    been reserved.

    | id:       The id of the Reservation
    | date_id:  The id of the Date for the play
    | time_id:  The id for the Time of the time
    | seat_id:  The Seat id this reservation is for
    | play_id:  The Play id this reservation is for
    | user_id:  The id of the user who make the reservation
    | price:    The price that the reservation was made for
    | reserved: The date the reservation was made

    | Backref Mappings
    |     play: The play this reservation is for
    |     seat: The seat that was reserved
    |     date: The date the reservation was made for
    |     time: The time the reservation was made for
    |     user: The user who made the reservation
    """
    id = db.Column(db.Integer, primary_key=True)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id'))
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'))
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'))
    play_id = db.Column(db.Integer, db.ForeignKey('play.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reserved = db.Column(db.Date)
    price = db.Column(db.Integer, nullable=False)


class Date(db.Model):
    """
    Stores the dates that the play is time on.

    | id:           The ID of the date
    | date:         The date of the play
    | play_id:      An integer representing the Play this date belongs to

    | Backref Mappings
    |     reservations: The reservations made on this date
    |     play:         The play this date is associated with
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False,
                     info={"description": "The day the play takes place on"})
    reservations = db.relationship("Reservation", backref="date",
                                   lazy="select")
    play_id = db.Column(db.Integer, db.ForeignKey('play.id'))


class Time(db.Model):
    """
    Stores the times that the play is time on

    | id:      The id of the time
    | time:    The time the play is shown
    | play_id: An integer representing a play

    | Backref Mappings
    |     reservations: The reservations made at this time
    |     play:         The play this time is associated with.
    """
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time, nullable=False,
                     info={"description": "When the play will start"})
    play_id = db.Column(db.Integer, db.ForeignKey("play.id"))
    reservations = db.relationship("Reservation", backref="time",
                                   lazy="select")
