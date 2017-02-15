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

if [ -z "$EQ_FUNCTIONAL_TEST_SUITES" ]; then
    export EQ_FUNCTIONAL_TEST_SUITES="core"
fi

if [ -z "$EQ_FUNCTIONAL_TEST_ENV" ]; then
    export EQ_FUNCTIONAL_TEST_ENV="local"
fi

echo "Running front end functional tests [${EQ_FUNCTIONAL_TEST_SUITES}]"
yarn test_functional -- --suite ${EQ_FUNCTIONAL_TEST_SUITES} --env ${EQ_FUNCTIONAL_TEST_ENV}

display_result $? 5 "Front end functional tests"
