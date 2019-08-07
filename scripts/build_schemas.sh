#!/usr/bin/env bash

set -e

mkdir -p data/en

# Build schema for each region
for region_code in GB-WLS GB-ENG GB-NIR; do
    # Lowercase the region code and replace '-' with '_'
    FORMATTED_REGION_CODE=$(echo "${region_code}" | tr '[:upper:]' '[:lower:]' | tr - _)

    CENSUS_DATE="2019-10-13"
    CENSUS_MONTH_YEAR_DATE="2019-10"

    for census_type in "individual" "household"; do

        DESTINATION_FILE="data/en/census_${census_type}_${FORMATTED_REGION_CODE}.json"

        if [[ "$region_code" = "GB-NIR" ]]; then
            SOURCE_FILE="data-source/jsonnet/northern-ireland/census_${census_type}.jsonnet"

            if [ -f "$SOURCE_FILE" ]; then
                jsonnet --tla-str region_code="${region_code}" --tla-str census_date="${CENSUS_DATE}" "${SOURCE_FILE}" > "${DESTINATION_FILE}"
            else
                echo "Ignoring $SOURCE_FILE as it does not exist"
            fi
        else
            SOURCE_FILE="data-source/jsonnet/england-wales/census_${census_type}.jsonnet"

            jsonnet --tla-str region_code="${region_code}" --tla-str census_date="${CENSUS_DATE}" --tla-str census_month_year_date="${CENSUS_MONTH_YEAR_DATE}" "${SOURCE_FILE}" > "${DESTINATION_FILE}"
        fi

        echo "Built ${DESTINATION_FILE}"
    done
done

# Move newly built schemas to 'en' dir
cp data-source/json/*.json data/en
