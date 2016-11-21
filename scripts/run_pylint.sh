#!/bin/bash
#
# Run project through pylint
#
# Currently doesn't lint ./tests folder (add to end of pylint line to include)
#
# NOTE: This script expects to be run from the project root with
# ./scripts/run_pylint.sh

pylint --rcfile=.pylintrc ./app
