import os

from app import settings

from babel.dates import get_timezone

basedir = os.path.abspath(os.path.dirname(__file__))

BABEL_DEFAULT_LOCALE = 'en'
BABEL_DEFAULT_TIMEZONE = get_timezone('Europe/London')


class Config(object):
    DEBUG = True
    NOTIFY_HTTP_PROTO = 'http'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.getenv('SR_COOKIE_SECRET')

    STATIC_URL_PATH = '/admin/static'
    ASSET_PATH = STATIC_URL_PATH + '/'


class Test(Config):
    DEBUG = True
    SECRET_KEY = settings.EQ_SECRET_KEY
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = get_timezone('Europe/London')


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SECRET_KEY = settings.EQ_SECRET_KEY


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
