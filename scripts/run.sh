#!/bin/bash
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run.sh

set -e

if [ "$EQ_RUN_DOCKER_UP" = True ]; then
    echo "Running Docker compose"
    docker-compose --version
    docker-compose up -d
fi

if [ "$EQ_RUN_DOCKER_TESTS" = True ]; then
    echo "Running Docker unit tests"
    docker --version
    docker build -t onsdigital/eq-survey-runner .
    docker build -t onsdigital/eq-survey-runner-unit-tests -f Dockerfile.test .
    docker run onsdigital/eq-survey-runner-unit-tests
fi

if [ "$EQ_RUN_LOCAL_LINT" = True ]; then
    echo "Running Local Lint Tests"
    ./scripts/run_lint.sh
fi

if [ "$EQ_RUN_LOCAL_TESTS" = True ]; then
    echo "Running Local Unit Tests"
    printf $(git rev-parse HEAD) > .application-version
    ./scripts/run_tests_unit.sh
fi

if [ "$EQ_RUN_LOCAL" = True ]; then
    echo "Running Local App"
    ./scripts/run_app.sh
fi


if [ "$EQ_RUN_FUNCTIONAL_TESTS" = True ]; then
    echo "Running Functional tests"
    ./scripts/run_tests_functional.sh
fi


