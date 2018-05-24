#!/bin/bash

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_DEVELOPER_LOGGING" ]; then
    export EQ_DEVELOPER_LOGGING=True
fi

if [ -z "$EQ_ENABLE_LIVE_RELOAD" ]; then
    export EQ_ENABLE_LIVE_RELOAD=True
fi

if [ -z "$EQ_ENABLE_SECURE_SESSION_COOKIE" ]; then
    export EQ_ENABLE_SECURE_SESSION_COOKIE=False
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

if [ -z "$EQ_SUBMITTED_RESPONSES_TABLE_NAME" ]; then
  export EQ_SUBMITTED_RESPONSES_TABLE_NAME="dev-submitted-responses"
fi

if [ -z "$EQ_QUESTIONNAIRE_STATE_TABLE_NAME" ]; then
  export EQ_QUESTIONNAIRE_STATE_TABLE_NAME="dev-questionnaire-state"
fi

if [ -z "$EQ_SESSION_TABLE_NAME" ]; then
  export EQ_SESSION_TABLE_NAME="dev-eq-session"
fi

if [ -z "$EQ_USED_JTI_CLAIM_TABLE_NAME" ]; then
  export EQ_USED_JTI_CLAIM_TABLE_NAME="dev-used-jti-claim"
fi

if [ -z "$EQ_DYNAMODB_ENABLED" ]; then
  export EQ_DYNAMODB_ENABLED=False
fi

if [ -z "$EQ_DYNAMODB_ENDPOINT" ]; then
  export EQ_DYNAMODB_ENDPOINT="http://localhost:6060"
fi

export FLASK_DEBUG=1

python scripts/generate_secrets.py jwt-test-secrets/
python -m sdc.crypto.scripts.generate_keys jwt-test-keys/
