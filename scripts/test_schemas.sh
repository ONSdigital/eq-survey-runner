#!/usr/bin/env bash

docker pull onsdigital/eq-schema-validator
validator=$(docker run -d -p 5001:5000 onsdigital/eq-schema-validator)

sleep 3

echo "Testing Schemas"

exit=0

for schema in $(find $1 -name '*.json');
do
echo $schema
result=$(curl -X POST -H "Content-Type: text/plain" --data "$(cat $schema)" http://localhost:5001/validate 2>/dev/null)
if [ "$result" != "{}" ] && [ "$result" != "" ]; then
echo "---Schema Failed Validation---"
echo "Error: [$result]"
exit=1
else
echo "ok: [$result]"
fi
done

docker rm -f $validator

exit $exit
