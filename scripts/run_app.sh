#!/bin/bash

function open_url {
  sleep 5
  echo $1
  open -a "/Applications/Google Chrome.app" $1
}

function run_python {
    if [ -z "${DOCKER}" ]; then
      python "$@"
    else
      python3 "$@"
    fi
}

if [ -n "$VIRTUAL_ENV" ]; then
  echo "Already in virtual environment $VIRTUAL_ENV"
else
  echo "You need to be in a virtual environment please!"
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR


# Output the current git revision
if [ -z "$EQ_GIT_REF" ]; then
  export EQ_GIT_REF=`git rev-parse HEAD`
fi

if [ -z "$EQ_CLOUDWATCH_LOGGING" ]; then
  export EQ_CLOUDWATCH_LOGGING=False
fi

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_RABBITMQ_ENABLED" ]; then
  export EQ_RABBITMQ_ENABLED=False
fi

# Use default environment vars for localhost if not already set

echo "Environment variables in use:"
env | grep EQ_

if [ ! -s "app/static" ]; then
  npm install
  npm run compile
fi

url="`run_python token_generator.py`"

if [ -z "${TRAVIS}" ]; then
  open_url $url &
  run_python application.py runserver
else
  run_python application.py runserver &
fi
