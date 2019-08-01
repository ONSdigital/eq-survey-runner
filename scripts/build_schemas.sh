#!/usr/bin/env bash

set -e

# Build schema for each region
for region_code in GB-WLS GB-ENG GB-NIR; do
    # Lowercase the region code and replace '-' with '_'
    FORMATTED_REGION_CODE=$(echo "${region_code}" | tr '[:upper:]' '[:lower:]' | tr - _)

    CENSUS_DATE="2019-10-13"
    CENSUS_MONTH_YEAR_DATE="2019-10"

    CENSUS_TYPES=("individual" "household")

    for census_type in "${CENSUS_TYPES[@]}"; do

        DESTINATION_FILE="data/en/census_${census_type}_${FORMATTED_REGION_CODE}.json"

        if [[ "$region_code" = "GB-NIR" ]]; then
            SOURCE_FILE="data-source/jsonnet/northern-ireland/census_${census_type}.jsonnet"

            jsonnet --tla-str region_code="${region_code}" --tla-str census_date="${CENSUS_DATE}" "${SOURCE_FILE}" > "${DESTINATION_FILE}"
        else
            SOURCE_FILE="data-source/jsonnet/england-wales/census_${census_type}.jsonnet"

            jsonnet --tla-str region_code="${region_code}" --tla-str census_date="${CENSUS_DATE}" --tla-str census_month_year_date="${CENSUS_MONTH_YEAR_DATE}" "${SOURCE_FILE}" > "${DESTINATION_FILE}"
        fi

        echo "Built ${DESTINATION_FILE}"
    done
done

# Move newly built schemas to 'en' dir
mkdir -p data/en
mv data-source/jsonnet/*.json data/en
cp data-source/json/*.json data/en
