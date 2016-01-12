from flask import request
from config import LANGUAGES

def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys()) or 'cy'
