#!/usr/bin/env bash

if [[ -x "$(command -v jsonnet)" ]]; then
    # Build schemas for each region
    for region_code in GB-WLS GB-ENG; do
        SOURCE_FILE="data-source/census_individual.jsonnet"
        # Lowercase the region code and replace '-' with '_'
        FORMATTED_REGION_CODE=$(echo "${region_code}" | tr '[:upper:]' '[:lower:]' | tr - _)
        DESTINATION_FILE="data-source/census_individual_${FORMATTED_REGION_CODE}.json"

        jsonnet --tla-str region_code=${region_code} --tla-str census_date="2019-09-01" "${SOURCE_FILE}" > "${DESTINATION_FILE}"
        echo "Built ${DESTINATION_FILE}"
    done

    # Format Census JSON files
    yarn gulp format:census

    # Move newly built schemas to 'en' dir
    mv data-source/*.json data/en

else
    echo "Jsonnet not available - skipping schema build"
fi
