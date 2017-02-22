#!/bin/bash
#
# Run all project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh

set -e

./scripts/run_tests_unit.sh
./scripts/run_tests_functional.sh

