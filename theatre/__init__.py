from . import app

models = app.models

db = app.db

migrate = app.migrate
login_manager = app.login_manager

application = app.build_app()
