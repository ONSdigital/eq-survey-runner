import os

from structlog import get_logger

logger = get_logger()


def ensure_min(value, minimum):
    if value < minimum:
        logger.warning('value below minimum', value=value, minimum=minimum)
        return minimum
    return value


def parse_mode(string):
    return string.upper() != 'FALSE'


def read_file(file_name):
    if file_name and os.path.isfile(file_name):
        logger.debug('reading from file', filename=file_name)
        with open(file_name, 'r') as file:
            contents = file.read()
            return contents
    else:
        logger.info('Did not load file because filename supplied was None or not a file', filename=file_name)
        return None


def get_env_or_fail(key):
    value = os.getenv(key)
    if value is None:
        raise Exception("Setting '{}' Missing".format(key))

    return value


EQ_MINIMIZE_ASSETS = parse_mode(os.getenv('EQ_MINIMIZE_ASSETS', 'True'))
# max request payload size in bytes
MAX_CONTENT_LENGTH = int(os.getenv('EQ_MAX_HTTP_POST_CONTENT_LENGTH', '65536'))

EQ_PROFILING = parse_mode(os.getenv('EQ_PROFILING', 'False'))
EQ_ENABLE_LIVE_RELOAD = parse_mode(os.getenv('EQ_ENABLE_LIVE_RELOAD', 'False'))

EQ_SECRETS_FILE = os.getenv('EQ_SECRETS_FILE', 'secrets.yml')
EQ_KEYS_FILE = os.getenv('EQ_KEYS_FILE', 'keys.yml')

EQ_SUBMISSION_BACKEND = os.getenv('EQ_SUBMISSION_BACKEND')
EQ_GCS_SUBMISSION_BUCKET_ID = os.getenv('EQ_GCS_SUBMISSION_BUCKET_ID')

EQ_RABBITMQ_HOST = os.getenv('EQ_RABBITMQ_HOST')
EQ_RABBITMQ_HOST_SECONDARY = os.getenv('EQ_RABBITMQ_HOST_SECONDARY')
EQ_RABBITMQ_PORT = int(os.getenv('EQ_RABBITMQ_PORT', '5672'))
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'submit_q')

EQ_SESSION_TIMEOUT_SECONDS = int(os.getenv('EQ_SESSION_TIMEOUT_SECONDS', str(45 * 60)))
EQ_UA_ID = os.getenv('EQ_UA_ID', '')
EQ_NEW_RELIC_ENABLED = parse_mode(os.getenv('EQ_NEW_RELIC_ENABLED', 'False'))
EQ_APPLICATION_VERSION_PATH = '.application-version'
EQ_APPLICATION_VERSION = read_file(EQ_APPLICATION_VERSION_PATH)

EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER', 'postgresql')
EQ_SERVER_SIDE_STORAGE_DATABASE_HOST = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_HOST')
EQ_SERVER_SIDE_STORAGE_DATABASE_PORT = int(os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_PORT', '5432'))
EQ_SERVER_SIDE_STORAGE_DATABASE_NAME = os.getenv('EQ_SERVER_SIDE_STORAGE_DATABASE_NAME', 'digitaleqrds')
EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS = ensure_min(int(os.getenv('EQ_SERVER_SIDE_STORAGE_USER_ID_ITERATIONS', '10000')),
                                                       1000)

EQ_STORAGE_BACKEND = os.getenv('EQ_STORAGE_BACKEND', 'datastore')
EQ_DATASTORE_EMULATOR_CREDENTIALS = parse_mode(os.getenv('EQ_DATASTORE_EMULATOR_CREDENTIALS', 'False'))
EQ_DYNAMODB_ENDPOINT = os.getenv('EQ_DYNAMODB_ENDPOINT')
EQ_DYNAMODB_MAX_RETRIES = int(os.getenv('EQ_DYNAMODB_MAX_RETRIES', '5'))
EQ_DYNAMODB_MAX_POOL_CONNECTIONS = int(os.getenv('EQ_DYNAMODB_MAX_POOL_CONNECTIONS', '30'))
EQ_SUBMITTED_RESPONSES_TABLE_NAME = get_env_or_fail('EQ_SUBMITTED_RESPONSES_TABLE_NAME')
EQ_QUESTIONNAIRE_STATE_TABLE_NAME = get_env_or_fail('EQ_QUESTIONNAIRE_STATE_TABLE_NAME')
EQ_SESSION_TABLE_NAME = get_env_or_fail('EQ_SESSION_TABLE_NAME')
EQ_USED_JTI_CLAIM_TABLE_NAME = get_env_or_fail('EQ_USED_JTI_CLAIM_TABLE_NAME')

EQ_REDIS_HOST = get_env_or_fail('EQ_REDIS_HOST')
EQ_REDIS_PORT = get_env_or_fail('EQ_REDIS_PORT')

EQ_DEV_MODE = parse_mode(os.getenv('EQ_DEV_MODE', 'False'))
EQ_ENABLE_CACHE = parse_mode(os.getenv('EQ_ENABLE_CACHE', 'True'))
EQ_ENABLE_FLASK_DEBUG_TOOLBAR = parse_mode(os.getenv('EQ_ENABLE_FLASK_DEBUG_TOOLBAR', 'False'))
EQ_ENABLE_SECURE_SESSION_COOKIE = parse_mode(os.getenv('EQ_ENABLE_SECURE_SESSION_COOKIE', 'True'))

EQ_JWT_LEEWAY_IN_SECONDS = 120
DEFAULT_LOCALE = 'en_GB'

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

USER_IK = 'user_ik'
EQ_SESSION_ID = 'eq-session-id'

EQ_LIST_ITEM_ID_LENGTH = 6
