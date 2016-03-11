#!/bin/bash

function open_url {
  sleep 1
  open -a "/Applications/Google Chrome.app" $1
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

# Use default environment vars for localhost if not already set

echo "Environment variables in use:"
env | grep EQ_

if [ ! -s "app/static" ]; then
  npm install
  npm run compile
fi

url="`python token_generator.py`"

echo $url
open_url $url &
python application.py runserver


