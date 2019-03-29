#!/bin/sh 

if [ -x "$(command -v jsonnet)" ]; then
  jsonnet --ext-str census_date="2019-09-01" data-source/census_individual.jsonnet > data-source/census_individual.json
  gulp format:census
  mv data-source/*.json data/en
else
  echo "Jsonnet not available - skipping schema build"
fi
