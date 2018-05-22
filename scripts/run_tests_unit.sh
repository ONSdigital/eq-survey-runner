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

run_docker=true
if [ "$1" == "--local" ] || [ "$2" == "--local" ]; then
    run_docker=false
fi

if [ "$run_docker" == true ]; then
    docker pull onsdigital/eq-docker-dynamodb
    validator="$(docker run -d -p 5001:5000 onsdigital/eq-docker-dynamodb)"
    sleep 3
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${DIR}/dev_settings.sh

echo "Environment variables in use:"
env | grep EQ_

py.test --cov=app --cov-report html "$@"
display_result $? 3 "Unit tests"

if [ "$run_docker" == true ]; then
    docker rm -f "$validator"
fi
