from flask import Flask
from config import ConfigDevelopment


def create_app(config_class=ConfigDevelopment):
    app = Flask(__name__, static_folder="static")

    app.config.from_object(config_class)

    from app.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    return app
