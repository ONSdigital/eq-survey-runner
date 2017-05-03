#!/usr/bin/env bash
current_dir=$(dirname "${BASH_SOURCE[0]}")
parent_dir=$(dirname "${current_dir}")
path_to_parent="$( cd "${parent_dir}" && pwd )"
schema_dir="${path_to_parent}"/data
temp_dir="${path_to_parent}"/temp

# Clone translation schema
git clone --branch v1.1.0 --depth 1 https://github.com/ONSdigital/eq-translations.git "${temp_dir}"/eq-translations
"${temp_dir}"/eq-translations/scripts/run_translate_all_surveys.sh "${schema_dir}"
# Delete repo
rm -rf "${temp_dir}"
