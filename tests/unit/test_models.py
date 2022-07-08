from theatre.models import User


def test_new_user():
    """
    GIVEN a user model
    WHEN a new user is created
    THEN check that user is initialized properly
    """

    first_name = "John"
    last_name = "Doe"
    fullname = "John Doe"

    user = User(first_name=first_name, last_name=last_name)

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.full_name == fullname


def test_set_password():
    """
    GIVEN a user
    WHEN a new password is set
    THEN check that the password is hashed properly
    """

    user = User(password="test")

    assert user.check_password("test") is True
    assert user.password != "test"
