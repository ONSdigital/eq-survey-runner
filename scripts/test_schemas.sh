#!/usr/bin/env bash

docker pull onsdigital/eq-schema-validator
validator="$(docker run -d -p 5001:5000 onsdigital/eq-schema-validator)"

sleep 3

green="$(tput setaf 2)"
red="$(tput setaf 1)"
default="$(tput sgr0)"
checks=4

until [ "$checks" == 0 ]; do
    response="$(curl -so /dev/null -w '%{http_code}' http://localhost:5001/status)"

    if [ "$response" != "200" ]; then
        echo "${red}---Error: Schema Validator Not Reachable---"
        echo "HTTP Status: $response"
        if [ "$checks"  != 1 ]; then
            echo -e "Retrying...${default}\\n"
            sleep 5
        else
            echo -e "Exiting...${default}\\n"
            exit
        fi
        (( checks-- ))
    else
        (( checks=0 ))
    fi

done

exit=0

echo "---Testing Schemas---"
failed=0
passed=0

for schema in $(find "$1" -name '*.json'); do

    result="$(curl -s -w 'HTTPSTATUS:%{http_code}' -X POST -H "Content-Type: application/json" -d @"$schema" http://localhost:5001/validate | tr -d '\n')"
    result_response="${result//*HTTPSTATUS:/}"
    result_body="${result//HTTPSTATUS:*/}"

    if [ "$result_response" == "200" ] && [ "$result_body" == "{}" ]; then
        echo -e "${green}$schema - PASSED${default}"
        (( passed++ ))
    else
        echo -e "\\n${red}$schema - FAILED"
        echo "HTTP Status @ /validate: [$result_response]"
        echo -e "Error: [$result_body]${default}\\n"
        (( failed++ ))
        exit=1
    fi

done

echo -e "\\n${green}$passed Passed${default} - ${red}$failed Failed${default}"

docker rm -f "$validator"
exit "$exit"
