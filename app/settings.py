import os


EQ_RABBITMQ_URL = os.getenv('EQ_RABBITMQ_URL', 'amqp://admin:admin@localhost:5672/%2F')
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'eq-submissions')
EQ_RABBITMQ_TEST_QUEUE_NAME = os.getenv('EQ_RABBITMQ_TEST_QUEUE_NAME', 'eq-test')
EQ_PRODUCTION = os.getenv("EQ_PRODUCTION", False)
EQ_RRM_PUBLIC_KEY = os.getenv('EQ_RRM_PUBLIC_KEY')
EQ_SR_PRIVATE_KEY = os.getenv('EQ_SR_PRIVATE_KEY')
