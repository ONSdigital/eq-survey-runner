#!/bin/bash
#
# Run all project tests
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_tests.sh

set -e

EQ_RUN_LOCAL_TESTS=True EQ_RUN_FUNCTIONAL_TESTS=True EQ_RUN_LOCAL_LINT=True ./scripts/run.sh

