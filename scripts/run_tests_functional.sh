#!/bin/bash
#
# Run functional tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests_functional.sh

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

# Run Functional tests
npm config set python python2.7

yarn test_unit_no_watch
display_result $? 4 "Front end unit tests"

echo "Generating functional test pages"
yarn generate_pages

echo "Running front end functional tests"
yarn test_functional

display_result $? 5 "Front end functional tests"

if [[ "$EQ_RUN_DOCKER_UP" = True ]]; then
    echo "Stopping Docker Containers"
    docker-compose down

    echo "Running Datastore Emulator"
    docker-compose run -d -p 8432:8432 datastore

    while true
    do
        sleep 5
        CONTENT=$(curl http://localhost:8432)
        if [[ $CONTENT = "Ok" ]]
        then
            break
        fi
        echo "$CONTENT"
    done

    echo "Running Local App"
    ./scripts/run_app.sh &

    until curl -o /dev/null -s -H -f http://localhost:5000/status; do
        printf '.'
        sleep 5
    done
fi

echo "Running census functional tests"
yarn test_census

display_result $? 6 "Front end census functional tests"
