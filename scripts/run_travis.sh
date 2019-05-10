#!/bin/bash
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_travis.sh

set -e

echo "Building"
./scripts/build.sh

echo "Running schema tests"
./scripts/test_schemas.sh data/en

echo "Running lint tests"
./scripts/run_lint.sh

echo "Running unit tests"
./scripts/run_tests_unit.sh

echo "Running Docker compose"
docker-compose --version
docker-compose up --build -d

echo "Running Functional tests"
./scripts/run_tests_functional.sh
