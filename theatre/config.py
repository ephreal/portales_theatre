import os
import datetime
import logging


basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DB_NAME = 'portales_theatre'
    DB_USER = 'portales_theatre'
    # Password the database user must use to access the database
    SECRET_KEY = "123"

    # URI for the database.
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{SECRET_KEY}@' \
                              f'localhost/{DB_NAME}'
    # Suppress warning about the sqlalchemy track notifications.
    # This will be disabled by default in the future.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Comment out the following when going live
    # With this uncommented, files are not cached in the webbrowser. This lets
    # changes to CSS take effect immediately.
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(seconds=0)

    # Configure logging for the application
    LOGLEVEL = logging.INFO
    LOGFILE = f"{basedir}/theatre.log"
    logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=LOGLEVEL)
