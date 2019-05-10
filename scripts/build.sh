#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$( cd "$( dirname "${DIR}"/../../)" && pwd )"

cd "${DIR}"/.. || exit

echo "Loading Templates"
"${DIR}"/load_templates.sh

echo "Building schemas"
"${DIR}"/build_schemas.sh

echo "Compiling translated schemas"
"${DIR}"/translate_schemas.sh

printf $(git rev-parse HEAD) > .application-version
