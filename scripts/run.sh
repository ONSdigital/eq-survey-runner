#!/bin/bash
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run.sh

set -e

#if [[ "$EQ_RUN_LOCAL_LINT" = True ]]; then
#    echo "Running Local Lint Tests"
#    ./scripts/run_lint.sh
#
#    echo "Testing schemas"
#    ./scripts/test_schemas.sh data/en
#    ./scripts/test_schemas.sh data/cy
#fi
#
#if [[ "$EQ_RUN_LOCAL_TESTS" = True ]]; then
#    echo "Running Local Unit Tests"
#    printf $(git rev-parse HEAD) > .application-version
#    ./scripts/run_tests_unit.sh
#fi

if [[ "$EQ_RUN_LOCAL" = True ]]; then
    echo "Running Datastore Emulator"
    docker run -d -it -p 8432:8432 knarz/datastore-emulator:latest

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

    until curl --output /dev/null --silent --head --fail http://localhost:5000/status; do
        printf '.'
        sleep 5
    done
fi

if [[ "$EQ_RUN_DOCKER_UP" = True ]]; then
    echo "Running Docker compose"
    ./scripts/build.sh
    docker-compose --version
    docker-compose build
    docker-compose up -d
fi

if [[ "$EQ_RUN_FUNCTIONAL_TESTS" = True ]]; then
    echo "Running Functional tests"
    ./scripts/run_tests_functional.sh
fi
