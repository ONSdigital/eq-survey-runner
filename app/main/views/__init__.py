# This line exposes the main_blueprint instance to modules at this level
from .questionnaire import questionnaire_blueprint    # NOQA
from .root import root_blueprint    # NOQA
from flask import current_app    # NOQA
