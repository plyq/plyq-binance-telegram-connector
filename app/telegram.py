"""Telegram endpoints are specified here."""

from flask import Blueprint, abort, request  # type: ignore
from flask.globals import current_app  # type: ignore

from app.thirdparty.tgsdk import TelegramBot
from config import get_config_from_env  # type: ignore

bp = Blueprint("routes", __name__)
telegram_bot = TelegramBot(get_config_from_env().TELEGRAM_TOKEN)


@bp.route("/send", methods=["POST"])
def send():
    """Send message to telegram bot.

    :returns: bot response
    """
    data = request.get_json()
    try:
        message = data["message"]
        chat = data["chat"]
    except KeyError:
        abort(404)
    response, status = telegram_bot.send(chat, message)
    return response, status


@bp.route("/check", methods=["GET"])
def check():
    """Get telegram bot info.

    :returns: bot response
    """
    response, status = telegram_bot.check()
    return response, status
