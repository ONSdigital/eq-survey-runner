#!/bin/bash
#
# Run project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh

# Use default environment vars for localhost if not already set
export EQ_CLOUDWATCH_LOGGING=False

export EQ_RABBITMQ_ENABLED=False

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

echo "Environment variables in use:"
env | grep EQ_

set -o pipefail

function display_result {
  RESULT=$1
  EXIT_STATUS=$2
  TEST=$3

  if [ $RESULT -ne 0 ]; then
    echo -e "\033[31m$TEST failed\033[0m"
    exit $EXIT_STATUS
  else
    echo -e "\033[32m$TEST passed\033[0m"
  fi
}

flake8 --max-complexity 10 --count
display_result $? 1 "Code style check"

py.test --cov=app --cov-report xml $@ $1
display_result $? 2 "Unit tests"

# Run front end tests
npm config set python python2.7
yarn test
display_result $? 1 "Front end tests"
