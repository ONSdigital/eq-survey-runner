#!/bin/bash

if [ -n "$VIRTUAL_ENV" ]; then
  echo "Already in virtual environment $VIRTUAL_ENV"
else
  echo "You need to be in a virtual environment please!"
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


if [ "${TRAVIS}" ]; then
  # Reduce logging on TRAVIS builds
  export EQ_LOG_LEVEL=WARNING
  export EQ_WERKZEUG_LOG_LEVEL=WARNING
fi

source ${DIR}/dev_settings.sh

# Use default environment vars for localhost if not already set

echo "Environment variables in use:"
env | grep EQ_

${DIR}/build.sh

if [ -z "${TRAVIS}" ]; then
  python application.py runserver
else
  python application.py runserver &
fi
