from .config import Config
from . import models
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import sys
import logging


basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(basedir)

# Create any items that will be used in the app
migrate = Migrate()
login_manager = LoginManager()

# note: All models must be imported here for use
db = models.db
Seat = models.Seat
Play = models.Play


def build_app():

    logging.info("Website is starting up.")
    app = Flask(__name__)
    app.config.from_object(Config())
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    logging.info("Registering routes.")
    with app.app_context():
        from .routes import admin
        from .routes import auth
        from .routes import client
        from .routes.api import admin_api_routes
        from .routes.api import client_api_routes
        from .routes.api import report_api_routes
        from .routes import routes

        app.register_blueprint(admin.admin)
        app.register_blueprint(auth.auth)
        app.register_blueprint(client.client)
        app.register_blueprint(admin_api_routes.admin_api)
        app.register_blueprint(client_api_routes.client_api)
        app.register_blueprint(report_api_routes.report_api)
        app.register_blueprint(routes.theatre)

        logging.info("Routes have been registered")
        logging.info("Creating database objects (if they do not exist).")

        db.create_all()

    return app
