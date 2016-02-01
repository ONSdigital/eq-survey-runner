import os

EQ_RRM_PUBLIC_KEY = os.getenv('EQ_RRM_PUBLIC_KEY', './jwt-test-keys/rrm-public.pem')
EQ_SR_PRIVATE_KEY = os.getenv('EQ_SR_PRIVATE_KEY', './jwt-test-keys/sr-private.pem')
EQ_RABBITMQ_URL = os.getenv('EQ_RABBITMQ_URL', 'warren-rabbitmq1.eq.ons.digital')
EQ_RABBITMQ_QUEUE_NAME = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'eq-submissions')
EQ_RABBITMQ_TEST_QUEUE_NAME = os.getenv('EQ_RABBITMQ_TEST_QUEUE_NAME', 'eq-test')
EQ_RABBITMQ_USER = os.getenv('EQ_RABBITMQ_USER', 'admin')
EQ_RABBITMQ_PASSWORD = os.getenv('EQ_RABBITMQ_PASSWORD', 'admin')
