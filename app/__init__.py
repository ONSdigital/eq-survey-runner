import os
from datetime import timedelta, datetime

import pytz
from flask import Flask, render_template
from config import configs

from .main.views.healthcheck import HealthCheck


DISPLAY_DATETIME_FORMAT = '%A %d %B %Y at %H:%M'
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
EUROPE_LONDON = pytz.timezone("Europe/London")


def create_app(config_name):
    application = Flask(__name__)

    from .main import main as main_blueprint
    application.register_blueprint(main_blueprint)
    main_blueprint.config = application.config.copy()
    return application
