#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$( cd "$( dirname "${DIR}"/../../)" && pwd )"

cd "${DIR}"/.. || exit

echo "Loading Templates"
"${DIR}"/load_templates.sh

echo "Building schemas"
"${DIR}"/build_schemas.sh

echo "Translating schemas"
make translate

echo "Creating temporary household schemas based on individual schema in 'data' dir"

# Until household is delivered, temporarily create household schema as copies of the individual schema
cp data/en/census_individual_gb_wls.json data/en/census_household_gb_wls.json
cp data/en/census_individual_gb_eng.json data/en/census_household_gb_eng.json
cp data/en/census_individual_gb_nir.json data/en/census_household_gb_nir.json
cp data/cy/census_individual_gb_wls.json data/cy/census_household_gb_wls.json

printf $(git rev-parse HEAD) > .application-version
