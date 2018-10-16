#!/usr/bin/env bash -e
: "
In order to run translations the following steps must be done:
'brew install translate-toolkit'

replace {LANGUAGE} with the language to translate to, cy (Welsh) / gd (Gaelic)

'pybabel init -i app/translations/messages.pot -d app/translations -l {LANGUAGE}'
'csv2po app/translations/{LANGUAGE}.csv app/translations/{LANGUAGE}/LC_MESSAGES/messages.po'
"

pybabel compile -d app/translations
