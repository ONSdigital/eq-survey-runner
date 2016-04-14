import os
import logging
import pytz

logger = logging.getLogger(__name__)


def parse_mode(str):
    return str.upper() != 'FALSE'


def get_key(key_name):
    """
    TODO remove these once the encrypted key story is finished
    :return:
    """
    logger.debug("Opening file %", key_name)
    key = open(key_name, 'r')
    contents = key.read()
    logger.debug("Key is %s", contents)
    return contents

EQ_PROFILING = parse_mode(os.getenv('EQ_PROFILING', 'False'))

EQ_RABBITMQ_URL = os.getenv('EQ_RABBITMQ_URL', 'amqp://localhost:5672/%2F')
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'eq-submissions')
EQ_RABBITMQ_TEST_QUEUE_NAME = os.getenv('EQ_RABBITMQ_TEST_QUEUE_NAME', 'eq-test')
EQ_RABBITMQ_ENABLED = parse_mode(os.getenv('EQ_RABBITMQ_ENABLED', 'True'))
EQ_GIT_REF = os.getenv('EQ_GIT_REF', None)
EQ_NEW_RELIC_CONFIG_FILE = os.getenv('EQ_NEW_RELIC_CONFIG_FILE', './newrelic.ini')
EQ_SR_LOG_GROUP = os.getenv('EQ_SR_LOG_GROUP', os.getenv('USER', 'UNKNOWN') + '-local')
EQ_LOG_LEVEL = os.getenv('EQ_LOG_LEVEL', 'INFO')
EQ_CLOUDWATCH_LOGGING = parse_mode(os.getenv("EQ_CLOUDWATCH_LOGGING", 'True'))
EQ_SCHEMA_DIRECTORY = os.getenv('EQ_SCHEMA_DIRECTORY', 'app/data')
EQ_SESSION_TIMEOUT = int(os.getenv('EQ_SESSION_TIMEOUT', '28800'))
EQ_SECRET_KEY = os.getenv('EQ_SECRET_KEY', os.urandom(24))
EQ_UA_ID = os.getenv('EQ_UA_ID', '')

# keys for the RRM token exchange
EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY = get_key(os.getenv('EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY', "./jwt-test-keys/rrm-public.pem"))
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY = get_key(os.getenv('EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY', "./jwt-test-keys/sr-private.pem"))
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD = os.getenv("EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD", "digitaleq")

# keys for encryption of submissions
EQ_SUBMISSION_SDX_PUBLIC_KEY = get_key(os.getenv('EQ_SUBMISSION_SDX_PUBLIC_KEY', "./jwt-test-keys/sdx-public.pem"))
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY = get_key(os.getenv('EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY', "./jwt-test-keys/sr-private-encryption.pem"))
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD = os.getenv("EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD", "digitaleq")

# keys for the dev mode
EQ_DEV_MODE = parse_mode(os.getenv("EQ_DEV_MODE", "False"))
EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY = get_key(os.getenv('EQ_RRM_PRIVATE_KEY', "./jwt-test-keys/rrm-private.pem"))
EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY = get_key(os.getenv('EQ_SR_PUBLIC_KEY', "./jwt-test-keys/sr-public.pem"))

# non configurable settings

DISPLAY_DATETIME_FORMAT = '%A %d %B %Y at %H:%M'
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
EUROPE_LONDON = pytz.timezone("Europe/London")

# JWT configurations
EQ_JWT_LEEWAY_IN_SECONDS = 120
