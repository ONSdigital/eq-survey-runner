#!/bin/bash

if [ -n "$VIRTUAL_ENV" ]; then
  echo "Already in virtual environment $VIRTUAL_ENV"
else
  echo "You need to be in a virtual environment please!"
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "$DIR"


if [ "${TRAVIS}" ]; then
  # Reduce logging on TRAVIS builds
  export EQ_LOG_LEVEL=WARNING
  export EQ_WERKZEUG_LOG_LEVEL=WARNING
fi

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_RABBITMQ_ENABLED" ]; then
  export EQ_RABBITMQ_ENABLED=False
fi

if [ -z "$EQ_SECRET_KEY" ]; then
  export EQ_SECRET_KEY="SuperSecretDeveloperKey"
fi

# Use default environment vars for localhost if not already set

echo "Environment variables in use:"
env | grep EQ_

"${DIR}"/build.sh

if [ -z "${TRAVIS}" ]; then
  gunicorn -b 0.0.0.0:5000 application:application
else
  gunicorn -b 0.0.0.0:5000 application:application &
fi
