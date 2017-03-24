#!/bin/bash
#
# Run all project tests
#

set -e

if [ ! -f "./scripts/run.sh" ]; then
    echo "./scripts/run.sh not found. Are you running in the root of eq-survey-runner?"
    exit 1
fi

EQ_RUN_LOCAL_TESTS=True EQ_RUN_FUNCTIONAL_TESTS=True EQ_RUN_LOCAL_LINT=True ./scripts/run.sh

