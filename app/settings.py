import os

import pytz
from structlog import get_logger

logger = get_logger()


def ensure_min(value, minimum):
    if value < minimum:
        logger.warning('value below minimum', value=value, minimum=minimum)
        return minimum
    else:
        return value


def parse_mode(string):
    return string.upper() != 'FALSE'


def get_key(_key_name):
    if _key_name:
        logger.debug("reading key from file", filename=_key_name)
        key = open(_key_name, 'r')
        contents = key.read()
        return contents
    else:
        return None

EQ_MINIMIZE_ASSETS = parse_mode(os.getenv('EQ_MINIMIZE_ASSETS', 'False'))
# max request payload size in bytes
EQ_MAX_HTTP_POST_CONTENT_LENGTH = os.getenv('EQ_MAX_HTTP_POST_CONTENT_LENGTH', 65536)

# max number of repeats from a rule
EQ_MAX_NUM_REPEATS = os.getenv('EQ_MAX_NUM_REPEATS', 25)

EQ_PROFILING = parse_mode(os.getenv('EQ_PROFILING', 'False'))

EQ_RABBITMQ_URL = os.getenv('EQ_RABBITMQ_URL', 'amqp://localhost:5672/%2F')
EQ_RABBITMQ_URL_SECONDARY = os.getenv('EQ_RABBITMQ_URL_SECONDARY', 'amqp://localhost:5672/%2F')
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'eq-submissions')
EQ_RABBITMQ_TEST_QUEUE_NAME = os.getenv('EQ_RABBITMQ_TEST_QUEUE_NAME', 'eq-test')
EQ_RABBITMQ_ENABLED = parse_mode(os.getenv('EQ_RABBITMQ_ENABLED', 'True'))
EQ_GIT_REF = os.getenv('EQ_GIT_REF', 'unknown')
EQ_NEW_RELIC_CONFIG_FILE = os.getenv('EQ_NEW_RELIC_CONFIG_FILE', './newrelic.ini')
EQ_SCHEMA_DIRECTORY = os.getenv('EQ_SCHEMA_DIRECTORY', 'app/data')
EQ_SESSION_TIMEOUT = int(os.getenv('EQ_SESSION_TIMEOUT', '28800'))
EQ_SECRET_KEY = os.getenv('EQ_SECRET_KEY', os.urandom(24))
EQ_UA_ID = os.getenv('EQ_UA_ID', '')
EQ_MAX_REPLAY_COUNT = os.getenv('EQ_REPLAY_COUNT', 50)


EQ_SERVER_SIDE_STORAGE_ENCRYPTION = parse_mode(os.getenv('EQ_SERVER_SIDE_STORAGE_ENCRYPTION', 'True'))
EQ_SERVER_SIDE_STORAGE_DATABASE_URL = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_URL', 'sqlite:////tmp/questionnaire.db')
EQ_SERVER_SIDE_STORAGE_USER_ID_SALT = os.getenv('EQ_SERVER_SIDE_STORAGE_USER_ID_SALT', 'luke.skywalker.r2d2.c3p0')
EQ_SERVER_SIDE_STORAGE_USER_IK_SALT = os.getenv('EQ_SERVER_SIDE_STORAGE_USER_IK_SALT', 'jabba.leia.organa.solo')
EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_PEPPER = os.getenv('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER', 'boba.fett.ig88.xizor')
EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS = ensure_min(os.getenv('EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS', 10000), 1000)

EQ_DEV_MODE = parse_mode(os.getenv("EQ_DEV_MODE", "False"))
EQ_ENABLE_CACHE = parse_mode(os.getenv("EQ_ENABLE_CACHE", "True"))
EQ_ENABLE_FLASK_DEBUG_TOOLBAR = parse_mode(os.getenv("EQ_ENABLE_FLASK_DEBUG_TOOLBAR", "False"))

_KEYS = {
    'EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY':    "./jwt-test-keys/sdc-user-authentication-signing-rrm-public-key.pem",
    'EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY':    "./jwt-test-keys/sdc-user-authentication-encryption-sr-private-key.pem",
    'EQ_SUBMISSION_SDX_PUBLIC_KEY':             "./jwt-test-keys/sdc-submission-encryption-sdx-public-key.pem",
    'EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY':     "./jwt-test-keys/sdc-submission-signing-sr-private-key.pem",

    # Only used in DEV MODE:
    'EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY':   "./jwt-test-keys/sdc-user-authentication-signing-rrm-private-key.pem",
    'EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY':     "./jwt-test-keys/sdc-user-authentication-encryption-sr-public-key.pem",
}

_PASSWORDS = {
    'EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD':   "digitaleq",
    'EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD':    "digitaleq",
    'EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD':  "digitaleq",
}

# Load keys and passwords, but only allow developer mode defaults if EQ_DEV_MODE
# has been enabled explicitly...
for key_name, dev_location in _KEYS.items():
    path = os.getenv(key_name, dev_location if EQ_DEV_MODE else None)
    vars()[key_name] = get_key(path)  # assigns attribute to this module

for password_name, dev_default in _PASSWORDS.items():
    password = os.getenv(password_name, dev_default if EQ_DEV_MODE else None)
    vars()[password_name] = password  # assigns attribute to this module


# non configurable settings
# date format when displayed to the user
DISPLAY_DATETIME_FORMAT = '%A %d %B %Y at %H:%M'

# Date Format expected by SDX
SDX_DATE_FORMAT = "%d/%m/%Y"
EUROPE_LONDON = pytz.timezone("Europe/London")

# JWT configurations
EQ_JWT_LEEWAY_IN_SECONDS = 120

EQ_ROLE_PERMISSIONS = {'admin': ['flush']}
