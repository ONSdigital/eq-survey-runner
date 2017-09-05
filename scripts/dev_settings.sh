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

if [ -z "$EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER" ]; then
  export EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER="sqlite"
fi

if [ -z "$EQ_SERVER_SIDE_STORAGE_DATABASE_NAME" ]; then
  export EQ_SERVER_SIDE_STORAGE_DATABASE_NAME="//tmp/questionnaire.db"
fi

python scripts/generate_secrets.py jwt-test-keys/
