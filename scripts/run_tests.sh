#!/bin/bash
#
# Run all project tests
#

set -e

echo "Running schema tests"
./scripts/test_schemas.sh data/en

echo "Running lint tests"
./scripts/run_lint.sh

echo "Running unit tests"
./scripts/run_tests_unit.sh

echo "Running functional tests"
./scripts/run_tests_functional.sh