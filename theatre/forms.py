from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField
from wtforms.fields import FormField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import ModelForm, ModelFieldList
from theatre.app import models


class LoginForm(FlaskForm):
    """
    A form used by users to sign in to the service.
    """
    # We check for the email address to log in.
    # The administrative user will have whatever email the customer created
    # during the initial site setup.
    email = StringField("Email", validators=[DataRequired(), Length(max=256)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=8)])


class SignupForm(FlaskForm):
    """
    A form used by users to sign up for the service.
    """
    email = StringField("Email", validators=[DataRequired(), Length(max=256)])
    first_name = StringField("First Name",
                             validators=[DataRequired(), Length(max=64)])
    last_name = StringField("Last Name",
                            validators=[DataRequired(), Length(max=64)])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(min=8)])
    confirmation = PasswordField("Password Confirmation",
                                 validators=[DataRequired(),
                                             Length(min=8)])


class UserForm(FlaskForm):
    """
    Used to create new users on the site.
    """
    email = StringField("Email", validators=[DataRequired(), Length(max=256)])
    first_name = StringField("First Name",
                             validators=[DataRequired(), Length(max=64)])
    last_name = StringField("Last Name",
                            validators=[DataRequired(), Length(max=64)])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(min=8)])
    confirmation = PasswordField("Password Confirmation",
                                 validators=[DataRequired(),
                                             Length(min=8)])
    address = StringField("Address", validators=[Length(max=256)])
    apartment = StringField("Apartment", validators=[Length(max=32)])
    zip_code = StringField("Zip Code", validators=[Length(max=16)])
    city = StringField("City", validators=[Length(max=64)])
    state = StringField("State", validators=[Length(max=2)])
    is_admin = BooleanField("Admin?")
    submit = SubmitField("Edit User")


class PasswordForm(FlaskForm):
    """
    Used by users to modify their password on the site.
    """
    password = PasswordField("Password", validators=[Length(min=8)])
    confirmation = PasswordField("Password Confirmation",
                                 validators=[Length(min=8)])
    submit = SubmitField("Update Password")


class ModifyUserForm(FlaskForm):
    """
    Used by administrators to modify users on the site. This form removes the
    data required validators so fields do not need to be present.
    """
    email = StringField("Email", validators=[Length(max=256)])
    first_name = StringField("First Name", validators=[Length(max=64)])
    last_name = StringField("Last Name", validators=[Length(max=64)])
    address = StringField("Address", validators=[Length(max=256)])
    apartment = StringField("Apartment", validators=[Length(max=32)])
    zip_code = StringField("Zip Code", validators=[Length(max=16)])
    city = StringField("City", validators=[Length(max=64)])
    state = StringField("State", validators=[Length(max=2)])
    is_admin = BooleanField("Admin?")
    submit = SubmitField("Edit User")


class DateForm(ModelForm):
    """
    A form that displays a date object.
    """
    class Meta:
        model = models.Date


class TimeForm(ModelForm):
    """
    A form that displays a time object.
    """
    class Meta:
        model = models.Time


class PlayForm(ModelForm):
    """
    Used to create and modify plays.
    """
    class Meta:
        model = models.Play

    dates = ModelFieldList(FormField(DateForm), min_entries=1, max_entries=20)
    times = ModelFieldList(FormField(TimeForm), min_entries=1, max_entries=20)
    submit = SubmitField("Create Play")
