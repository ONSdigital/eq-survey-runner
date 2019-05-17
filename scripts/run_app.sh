#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source ${DIR}/dev_settings.sh

# Use default environment vars for localhost if not already set

echo "Environment variables in use:"
env | grep EQ_

${DIR}/build.sh

FLASK_APP=application.py FLASK_ENV=development flask run
