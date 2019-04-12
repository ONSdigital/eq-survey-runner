#!/bin/bash

# NOTE: This script expects to be run from the project root with
# ./scripts/lint_jsonnet.sh

failures=0
while read file; do 
  jsonnet fmt --test -i $file
  if [ $? -ne 0 ]; then
    echo "'$file' failed Jsonnet format check. Run 'jsonnet fmt -i $file' to fix."
    (( failures+= 1 ))
  fi
done < <(find ./data-source -name '*.jsonnet' -o -name '*.libsonnet')

if [ "$failures" -gt 0 ]; then
  exit 1
fi
