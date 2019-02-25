#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$( cd "$( dirname "${DIR}"/../../)" && pwd )"

cd "${DIR}"/.. || exit

if [[ ! -s "static" ]]; then
  echo "Compiling static assets"
  yarn compile
fi

if [[ -z "$EQ_RUN_LOCAL_LINT" ]]; then
  echo "Running Local Lint Tests"
  ./scripts/run_lint.sh

  echo "Testing schemas"
  "${DIR}"/test_schemas.sh data/en
  "${DIR}"/test_schemas.sh data/cy
fi

printf $(git rev-parse HEAD) > .application-version
