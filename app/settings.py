import os

from structlog import get_logger

from app.missing_setting_exception import MissingSettingException

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
    if file_name and os.path.isfile(file_name):
        logger.debug("reading from file", filename=file_name)
        f = open(file_name, "r")
        contents = f.read()
        return contents
    else:
        logger.info("Did not load file because filename supplied was None or not a file", file_name=file_name)
        return None


def get_env_or_fail(key):
    value = os.getenv(key)
    if value is None:
        raise MissingSettingException("Setting '{}' Missing".format(key))

    return value


EQ_MINIMIZE_ASSETS = parse_mode(os.getenv('EQ_MINIMIZE_ASSETS', 'False'))
# max request payload size in bytes
MAX_CONTENT_LENGTH = os.getenv('EQ_MAX_HTTP_POST_CONTENT_LENGTH', 65536)

# max number of repeats from a rule
EQ_MAX_NUM_REPEATS = os.getenv('EQ_MAX_NUM_REPEATS', 25)

EQ_PROFILING = parse_mode(os.getenv('EQ_PROFILING', 'False'))

EQ_RABBITMQ_URL = get_env_or_fail('EQ_RABBITMQ_URL')
EQ_RABBITMQ_URL_SECONDARY = get_env_or_fail('EQ_RABBITMQ_URL_SECONDARY')
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'submit_q')
EQ_RABBITMQ_ENABLED = parse_mode(os.getenv('EQ_RABBITMQ_ENABLED', 'True'))
EQ_NEW_RELIC_CONFIG_FILE = os.getenv('EQ_NEW_RELIC_CONFIG_FILE', './newrelic.ini')
EQ_SCHEMA_DIRECTORY = os.getenv('EQ_SCHEMA_DIRECTORY', 'data')
EQ_SESSION_TIMEOUT_SECONDS = int(os.getenv('EQ_SESSION_TIMEOUT_SECONDS', 45 * 60))
EQ_SESSION_TIMEOUT_GRACE_PERIOD_SECONDS = int(os.getenv('EQ_SESSION_TIMEOUT_GRACE_PERIOD_SECONDS', '30'))
EQ_SESSION_TIMEOUT_PROMPT_SECONDS = int(os.getenv('EQ_SESSION_TIMEOUT_PROMPT_SECONDS', 120))
EQ_SECRET_KEY = get_env_or_fail('EQ_SECRET_KEY')
EQ_UA_ID = os.getenv('EQ_UA_ID', '')
EQ_NEW_RELIC_ENABLED = parse_mode(os.getenv("EQ_NEW_RELIC_ENABLED", "False"))
EQ_APPLICATION_VERSION_PATH = '.application-version'
EQ_APPLICATION_VERSION = read_file(EQ_APPLICATION_VERSION_PATH)

EQ_SERVER_SIDE_STORAGE_ENCRYPTION = parse_mode(os.getenv('EQ_SERVER_SIDE_STORAGE_ENCRYPTION', 'True'))
EQ_SERVER_SIDE_STORAGE_DATABASE_URL = get_env_or_fail('EQ_SERVER_SIDE_STORAGE_DATABASE_URL')
EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_COUNT = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_CONNECT_RETRY_COUNT', 10)
EQ_SERVER_SIDE_STORAGE_DATABASE_SETUP_RETRY_DELAY_SECONDS = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_CONNECT_RETRY_DELAY_SECONDS', 6)
EQ_SERVER_SIDE_STORAGE_USER_ID_SALT = get_env_or_fail('EQ_SERVER_SIDE_STORAGE_USER_ID_SALT')
EQ_SERVER_SIDE_STORAGE_USER_IK_SALT = get_env_or_fail('EQ_SERVER_SIDE_STORAGE_USER_IK_SALT')
EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER = get_env_or_fail('EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER')
EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS = ensure_min(os.getenv('EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS', 10000), 1000)

EQ_DEV_MODE = parse_mode(os.getenv("EQ_DEV_MODE", "False"))
EQ_ENABLE_CACHE = parse_mode(os.getenv("EQ_ENABLE_CACHE", "True"))
EQ_ENABLE_FLASK_DEBUG_TOOLBAR = parse_mode(os.getenv("EQ_ENABLE_FLASK_DEBUG_TOOLBAR", "False"))

EQ_JWT_LEEWAY_IN_SECONDS = 120

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
    vars()[key_name] = read_file(path)  # assigns attribute to this module

for password_name, dev_default in _PASSWORDS.items():
    password = os.getenv(password_name, dev_default if EQ_DEV_MODE else None)
    vars()[password_name] = password  # assigns attribute to this module

# Date Format expected by SDX
SDX_DATE_FORMAT = "%d/%m/%Y"
