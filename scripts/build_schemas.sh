#!/usr/bin/env bash

set -e

# Build schema for each region
for region_code in GB-WLS GB-ENG GB-NIR; do
    # Lowercase the region code and replace '-' with '_'
    FORMATTED_REGION_CODE=$(echo "${region_code}" | tr '[:upper:]' '[:lower:]' | tr - _)
    DESTINATION_FILE="data-source/jsonnet/census_individual_${FORMATTED_REGION_CODE}.json"

    if [[ "$region_code" = "GB-NIR" ]]; then
        SOURCE_FILE="data-source/jsonnet/northern-ireland/census_individual.jsonnet"
    else
        SOURCE_FILE="data-source/jsonnet/england-wales/census_individual.jsonnet"
    fi

    jsonnet --tla-str region_code="${region_code}" --tla-str census_date="2019-06-20" "${SOURCE_FILE}" > "${DESTINATION_FILE}"

    echo "Built ${DESTINATION_FILE}"
done

# Move newly built schemas to 'en' dir
mkdir -p data/en
mv data-source/jsonnet/*.json data/en
cp data-source/json/*.json data/en
echo "Moved newly built schemas to 'data/en' dir"
