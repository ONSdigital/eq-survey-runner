#!/bin/bash
if [ -n "$VIRTUAL_ENV" ]; then
  echo "Already in virtual environment $VIRTUAL_ENV"
else
  echo "You need to be in a virtual environment please!"
fi

# Use default environment vars for localhost if not already set

echo "Environment variables in use:"
env | grep EQ_

python application.py runserver
