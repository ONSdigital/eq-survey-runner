import os


def parse_mode(str):
    return str.upper() != 'FALSE'

EQ_RABBITMQ_URL = os.getenv('EQ_RABBITMQ_URL', 'amqp://admin:admin@localhost:5672/%2F')
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'eq-submissions')
EQ_RABBITMQ_TEST_QUEUE_NAME = os.getenv('EQ_RABBITMQ_TEST_QUEUE_NAME', 'eq-test')
EQ_PRODUCTION = parse_mode(os.getenv("EQ_PRODUCTION", 'True'))
EQ_RRM_PUBLIC_KEY = os.getenv('EQ_RRM_PUBLIC_KEY')
EQ_SR_PRIVATE_KEY = os.getenv('EQ_SR_PRIVATE_KEY')
EQ_GIT_REF = os.getenv('EQ_GIT_REF', None)
EQ_NEW_RELIC_CONFIG_FILE = os.getenv('EQ_NEW_RELIC_CONFIG_FILE', './newrelic.ini')
EQ_SR_LOG_GROUP = os.getenv('EQ_SR_LOG_GROUP', os.getenv('USER', 'UNKNOWN') + '-local')
EQ_LOG_LEVEL = os.getenv('EQ_LOG_LEVEL', 'INFO')
EQ_SCHEMA_DIRECTORY = os.getenv('EQ_SCHEMA_DIRECTORY', 'app/data')
EQ_SESSION_TIMEOUT = int(os.getenv('EQ_SESSION_TIMEOUT', '1800'))
EQ_SECRET_KEY = os.getenv('EQ_SECRET_KEY', 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT')
