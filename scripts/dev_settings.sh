#!/bin/bash

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_DEVELOPER_LOGGING" ]; then
    export EQ_DEVELOPER_LOGGING=True
fi

if [ -z "$EQ_RABBITMQ_ENABLED" ]; then
  export EQ_RABBITMQ_ENABLED=False
fi

if [ -z "$EQ_RABBITMQ_HOST" ]; then
  export EQ_RABBITMQ_HOST="localhost"
fi

if [ -z "$EQ_RABBITMQ_HOST_SECONDARY" ]; then
  export EQ_RABBITMQ_HOST_SECONDARY="localhost"
fi

if [ -z "$SQLALCHEMY_DATABASE_URI" ]; then
  export SQLALCHEMY_DATABASE_URI="sqlite:////tmp/questionnaire.db"
fi

export FLASK_DEBUG=1

python scripts/generate_secrets.py jwt-test-secrets/
python -m sdc.crypto.scripts.generate_keys jwt-test-keys/
