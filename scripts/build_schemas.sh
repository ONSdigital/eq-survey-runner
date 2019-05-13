#!/usr/bin/env bash

set -e

# Build schemas for each region
for region_code in GB-WLS GB-ENG; do
    SOURCE_FILE="data-source/jsonnet/census_individual.jsonnet"
    # Lowercase the region code and replace '-' with '_'
    FORMATTED_REGION_CODE=$(echo "${region_code}" | tr '[:upper:]' '[:lower:]' | tr - _)
    DESTINATION_FILE="data-source/jsonnet/census_individual_${FORMATTED_REGION_CODE}.json"

    jsonnet --tla-str region_code=${region_code} --tla-str census_date="2019-09-01" "${SOURCE_FILE}" > "${DESTINATION_FILE}"
    echo "Built ${DESTINATION_FILE}"
done

# Move newly built schemas to 'en' dir
mkdir -p data/en
mv data-source/jsonnet/*.json data/en
cp data-source/json/*.json data/en
