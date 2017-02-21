#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
if [ ! -s "static" ]; then
  echo "Compiling web resources"
  yarn compile

  echo "Compiling translated schemas"
  $DIR/translate_schemas.sh
fi
