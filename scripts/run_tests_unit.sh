#!/bin/bash
#
# Run unit tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests_unit.sh
set -o pipefail

echo "starting docker..."
PUBSUB_CONTAINER_ID=$(docker run --rm -d --publish 8681:8681 -e PUBSUB_PROJECT1=my-test-project,test-topic-id messagebird/gcloud-pubsub-emulator:latest)
function finish {
  echo "killing docker..."
  docker rm -vf $PUBSUB_CONTAINER_ID
}
trap finish EXIT

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

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${DIR}/dev_settings.sh

echo "Environment variables in use:"
env | grep EQ_

py.test -n auto --cov=app --cov-report html "$@"
display_result $? 3 "Unit tests"
