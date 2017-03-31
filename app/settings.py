import json
import os

import credstash
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


def read_file(file_name):
    if os.path.isfile(file_name):
        logger.debug("reading from file", filename=file_name)
        f = open(file_name, "r")
        contents = f.read()
        return contents
    else:
        return None

EQ_DEV_MODE = parse_mode(os.getenv("EQ_DEV_MODE", "False"))
EQ_DEV_KEYS = parse_mode(os.getenv("EQ_DEV_KEYS", "False"))

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
EQ_NEW_RELIC_CONFIG_FILE = os.getenv('EQ_NEW_RELIC_CONFIG_FILE', './newrelic.ini')
EQ_SCHEMA_DIRECTORY = os.getenv('EQ_SCHEMA_DIRECTORY', 'app/data')
EQ_SESSION_TIMEOUT_SECONDS = int(os.getenv('EQ_SESSION_TIMEOUT_SECONDS', 45 * 60))
EQ_SESSION_TIMEOUT_GRACE_PERIOD_SECONDS = int(os.getenv('EQ_SESSION_TIMEOUT_GRACE_PERIOD_SECONDS', '30'))
EQ_SESSION_TIMEOUT_PROMPT_SECONDS = int(os.getenv('EQ_SESSION_TIMEOUT_PROMPT_SECONDS', 120))
EQ_SECRET_KEY = os.getenv('EQ_SECRET_KEY', os.urandom(24) if EQ_DEV_KEYS else credstash.getSecret("EQ_SECRET_KEY"))
EQ_UA_ID = os.getenv('EQ_UA_ID', '')
EQ_NEW_RELIC_ENABLED = os.getenv("EQ_NEW_RELIC_ENABLED", "False") == "True"
EQ_APPLICATION_VERSION_PATH = '.application-version'
EQ_APPLICATION_VERSION = read_file(EQ_APPLICATION_VERSION_PATH)

EQ_SERVER_SIDE_STORAGE_ENCRYPTION = parse_mode(os.getenv('EQ_SERVER_SIDE_STORAGE_ENCRYPTION', 'True'))
EQ_SERVER_SIDE_STORAGE_DATABASE_URL = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_URL', 'sqlite:////tmp/questionnaire.db')
EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_COUNT = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_CONNECT_RETRY_COUNT', 10)
EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_DELAY_SECONDS = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_CONNECT_RETRY_DELAY_SECONDS', 6)
EQ_SERVER_SIDE_STORAGE_USER_ID_SALT = os.getenv('EQ_SERVER_SIDE_STORAGE_USER_ID_SALT', 'luke.skywalker.r2d2.c3p0')
EQ_SERVER_SIDE_STORAGE_USER_IK_SALT = os.getenv('EQ_SERVER_SIDE_STORAGE_USER_IK_SALT', 'jabba.leia.organa.solo')
EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_PEPPER = os.getenv('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER', 'boba.fett.ig88.xizor')
EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS = ensure_min(os.getenv('EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS', 10000), 1000)

EQ_ENABLE_CACHE = parse_mode(os.getenv("EQ_ENABLE_CACHE", "True"))
EQ_ENABLE_FLASK_DEBUG_TOOLBAR = parse_mode(os.getenv("EQ_ENABLE_FLASK_DEBUG_TOOLBAR", "False"))

_KEYS = [
    'EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY',
    'EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY',
    'EQ_SUBMISSION_SDX_PUBLIC_KEY',
    'EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY',

    # Only used in DEV MODE:
    'EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY',
    'EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY',
]

_PASSWORDS = [
    'EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD',
    'EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD',
    'EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD',
]

if EQ_DEV_KEYS:
    dev_keys = json.loads(read_file('.dev_keys.json'))

# Load keys and passwords
for key_name in _KEYS:
    vars()[key_name] = dev_keys[key_name] if EQ_DEV_KEYS else credstash.getSecret(key_name)

for password_name in _PASSWORDS:
    vars()[password_name] = dev_keys[password_name] if EQ_DEV_KEYS else credstash.getSecret(password_name)  # assigns attribute to this module

# Date Format expected by SDX
SDX_DATE_FORMAT = "%d/%m/%Y"
