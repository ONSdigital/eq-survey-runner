#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$( cd "$( dirname "${DIR}"/../../)" && pwd )"

cd "${DIR}"/.. || exit

echo "Generating schemas"
"${DIR}"/generate_schemas.py "${ROOT}/data/sources" "${ROOT}/data/en"

if [ ! -s "static" ]; then
  echo "Compiling web resources"
  yarn compile

  echo "Compiling translated schemas"
  "${DIR}"/translate_schemas.sh
fi

printf $(git rev-parse HEAD) > .application-version
