#!/bin/bash

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_RABBITMQ_ENABLED" ]; then
  export EQ_RABBITMQ_ENABLED=False
fi

if [ -z "$EQ_ENABLE_CACHE" ]; then
  export EQ_ENABLE_CACHE=True
fi

if [ -z "$EQ_MINIMIZE_ASSETS" ]; then
  export EQ_MINIMIZE_ASSETS=False
fi

if [ -z "$EQ_SECRET_KEY" ]; then
  export EQ_SECRET_KEY="SuperSecretDeveloperKey"
fi

if [ -z "$EQ_SERVER_SIDE_STORAGE_USER_ID_SALT" ]; then
  export EQ_SERVER_SIDE_STORAGE_USER_ID_SALT="developer.user.id.salt"
fi

if [ -z "$EQ_SERVER_SIDE_STORAGE_USER_IK_SALT" ]; then
  export EQ_SERVER_SIDE_STORAGE_USER_IK_SALT="developer.user.ik.salt"
fi

if [ -z "$EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER" ]; then
  export EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER="developer.storage.encryption.pepper"
fi

if [ -z "$EQ_RABBITMQ_URL" ]; then
  export EQ_RABBITMQ_URL="amqp://localhost:5672/%2F"
fi

if [ -z "$EQ_RABBITMQ_URL_SECONDARY" ]; then
  export EQ_RABBITMQ_URL_SECONDARY="amqp://localhost:5672/%2F"
fi

if [ -z "$EQ_SERVER_SIDE_STORAGE_DATABASE_URL" ]; then
  export EQ_SERVER_SIDE_STORAGE_DATABASE_URL="sqlite:////tmp/questionnaire.db"
fi
