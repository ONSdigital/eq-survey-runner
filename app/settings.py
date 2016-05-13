import os
import logging
import pytz


logger = logging.getLogger(__name__)


def parse_mode(str):
    return str.upper() != 'FALSE'


def get_key(key_name):
    if key_name:
        """
        TODO remove these once the encrypted key story is finished
        :return:
        """
        logger.debug("Opening file %", key_name)
        key = open(key_name, 'r')
        contents = key.read()
        logger.debug("Key is %s", contents)
        return contents
    else:
        return None

EQ_MINIMIZE_ASSETS = parse_mode(os.getenv('EQ_MINIMIZE_ASSETS', 'False'))

EQ_PROFILING = parse_mode(os.getenv('EQ_PROFILING', 'False'))

EQ_RABBITMQ_URL = os.getenv('EQ_RABBITMQ_URL', 'amqp://localhost:5672/%2F')
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'eq-submissions')
EQ_RABBITMQ_TEST_QUEUE_NAME = os.getenv('EQ_RABBITMQ_TEST_QUEUE_NAME', 'eq-test')
EQ_RABBITMQ_ENABLED = parse_mode(os.getenv('EQ_RABBITMQ_ENABLED', 'True'))
EQ_GIT_REF = os.getenv('EQ_GIT_REF', 'unknown')
EQ_NEW_RELIC_CONFIG_FILE = os.getenv('EQ_NEW_RELIC_CONFIG_FILE', './newrelic.ini')
EQ_SR_LOG_GROUP = os.getenv('EQ_SR_LOG_GROUP', os.getenv('USER', 'UNKNOWN') + '-local')
EQ_LOG_LEVEL = os.getenv('EQ_LOG_LEVEL', 'INFO')
EQ_CLOUDWATCH_LOGGING = parse_mode(os.getenv("EQ_CLOUDWATCH_LOGGING", 'True'))
EQ_SCHEMA_DIRECTORY = os.getenv('EQ_SCHEMA_DIRECTORY', 'app/data')
EQ_SESSION_TIMEOUT = int(os.getenv('EQ_SESSION_TIMEOUT', '28800'))
EQ_SECRET_KEY = os.getenv('EQ_SECRET_KEY', os.urandom(24))
EQ_UA_ID = os.getenv('EQ_UA_ID', '')


EQ_SERVER_SIDE_STORAGE = parse_mode(os.getenv('EQ_SERVER_SIDE_STORAGE', 'False'))
EQ_SERVER_SIDE_STORAGE_TYPE = os.getenv('EQ_SERVER_SIDE_STORAGE_TYPE', 'DATABASE')
EQ_SERVER_SIDE_STORAGE_ENCRYPTION = parse_mode(os.getenv('EQ_SERVER_SIDE_STORAGE_ENCRYPTION', 'False'))
EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY = os.getenv('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY', "lord.darth.vader").encode()
EQ_SERVER_SIDE_STORAGE_DATABASE_URL = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_URL', 'sqlite:////tmp/questionnaire.db')
EQ_SERVER_SIDE_STORAGE_SALT = os.getenv('EQ_SERVER_SIDE_STORAGE_SALT', 'luke.skywalker.r2d2.c3p0')

EQ_SPLUNK_LOGGING = parse_mode(os.getenv('EQ_SPLUNK_LOGGING', 'False'))
EQ_SPLUNK_HOST = os.getenv('EQ_SPLUNK_HOST')
EQ_SPLUNK_PORT = os.getenv('EQ_SPLUNK_PORT')
EQ_SPLUNK_USERNAME = os.getenv('EQ_SPLUNK_USERNAME')
EQ_SPLUNK_PASSWORD = os.getenv('EQ_SPLUNK_PASSWORD')
EQ_SPLUNK_INDEX = os.getenv('EQ_SPLUNK_INDEX')

EQ_DEV_MODE = parse_mode(os.getenv("EQ_DEV_MODE", "False"))

_KEYS = {
    'EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY':    "./jwt-test-keys/sdc-user-authentication-signing-rrm-public-key.pem",
    'EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY':    "./jwt-test-keys/sdc-user-authentication-encryption-sr-private-key.pem",
    'EQ_SUBMISSION_SDX_PUBLIC_KEY':             "./jwt-test-keys/sdc-submission-encryption-sdx-public-key.pem",
    'EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY':     "./jwt-test-keys/sdc-submission-signing-sr-private-key.pem",

    # Only used in DEV MODE:
    'EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY':   "./jwt-test-keys/sdc-user-authentication-signing-rrm-private-key.pem",
    'EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY':     "./jwt-test-keys/sdc-user-authentication-encryption-sr-public-key.pem"
}

_PASSWORDS = {
    'EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD':   "digitaleq",
    'EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD':    "digitaleq",
    'EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD':  "digitaleq"
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

DISPLAY_DATETIME_FORMAT = '%A %d %B %Y at %H:%M'
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
EUROPE_LONDON = pytz.timezone("Europe/London")

# JWT configurations
EQ_JWT_LEEWAY_IN_SECONDS = 120
