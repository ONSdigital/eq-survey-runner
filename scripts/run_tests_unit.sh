#!/bin/bash
#
# Run unit tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests_unit.sh

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

echo "Environment variables in use:"
env | grep EQ_

if [ -z "$EQ_DEV_MODE" ]; then
  export EQ_DEV_MODE=True
fi

if [ -z "$EQ_ENABLE_CACHE" ]; then
  export EQ_ENABLE_CACHE=True
fi

# Use default environment vars for localhost if not already set
export EQ_RABBITMQ_ENABLED=False

py.test --cov=app --cov-report xml
display_result $? 3 "Unit tests"
