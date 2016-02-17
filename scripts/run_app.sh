#!/bin/bash
if [ -n "$VIRTUAL_ENV" ]; then
  echo "Already in virtual environment $VIRTUAL_ENV"
else
  echo "You need to be in a virtual environment please!"
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR

if [ -z "$EQ_RRM_PUBLIC_KEY" ]; then
  export EQ_RRM_PUBLIC_KEY=`cat $DIR/../jwt-test-keys/rrm-public.pem`
fi

if [ -z "$EQ_SR_PRIVATE_KEY" ]; then
  export EQ_SR_PRIVATE_KEY=`cat $DIR/../jwt-test-keys/sr-private.pem`
fi

# Output the current git revision
if [ -z "$EQ_GIT_REF" ]; then
  export EQ_GIT_REF=`git rev-parse HEAD`
fi

# Use default environment vars for localhost if not already set

echo "Environment variables in use:"
env | grep EQ_

npm install
npm run compile

python application.py runserver
