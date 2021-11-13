import os
from typing import Type


class Config(object):
    # Flask.
    DEBUG = True
    FLASK_ENV = os.getenv("FLASK_ENV", "DEBUG")
    # Telegram.
    TELEGRAM_TOKEN = ""


class ProductionConfig(Config):
    DEBUG = False
    # Telegram.
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")


class DebugConfig(Config):
    DEBUG = True
    # Telegram.
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_TEST", "")


class TestConfig(Config):
    DEBUG = True
    # Telegram.
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN_TEST", "")


def get_config_from_env() -> Type[Config]:
    if Config.FLASK_ENV == "DEBUG":
        return DebugConfig
    elif Config.FLASK_ENV == "PROD":
        return ProductionConfig
    elif Config.FLASK_ENV == "TEST":
        return TestConfig
    else:
        raise NotImplementedError("Unknown environment %s" % Config.FLASK_ENV)
