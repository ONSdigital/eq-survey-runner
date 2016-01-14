import os
from babel.dates import get_timezone

basedir = os.path.abspath(os.path.dirname(__file__))

LANGUAGES = {
    'en': 'English',
    'cy': 'Welsh (Cymraeg)',
    'gd': 'Gaelic (Scots Gaelic)'
}

BABEL_DEFAULT_LOCALE = 'cy'
BABEL_DEFAULT_TIMEZONE = get_timezone('Europe/London')


class Config(object):
    DEBUG = True
    WTF_CSRF_ENABLED = True
    NOTIFY_HTTP_PROTO = 'http'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.getenv('SR_COOKIE_SECRET')

    STATIC_URL_PATH = '/admin/static'
    ASSET_PATH = STATIC_URL_PATH + '/'


class Test(Config):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "not-so-secret"


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = "not-so-secret"


class Live(Config):
    DEBUG = False
    SR_HTTP_PROTO = 'https'


class Staging(Config):
    DEBUG = False


configs = {
    'development': Development,
    'preview': Live,
    'staging': Staging,
    'production': Live,
    'test': Test,
}
