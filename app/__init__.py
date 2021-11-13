"""Initialize Flask application."""
from flask import Flask  # type: ignore
from flask.logging import default_handler  # type: ignore
from flask_cors import CORS  # type: ignore

from config import get_config_from_env


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config_from_env())

    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["CORS_HEADERS"] = "Content-Type"

    from app import telegram

    app.register_blueprint(telegram.bp)

    return app
