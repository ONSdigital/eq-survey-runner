# Jinja Filters Used by Schemas


## format_number
Returns the given number with the appropriate thousands grouping and decimal separator as determined by the locale.
Uses Babel's [format_decimal](http://babel.pocoo.org/en/latest/api/numbers.html#babel.numbers.format_decimal) from `number.py`.

##### Parameters: 
- value: A single numeric value.

##### Context:
Most commonly used to display a previous answer's numeric value in a following question.
```
Of the <em>{{answers['total-number-employees']|format_number}}</em> total employees employed on 14 December 2018, how many male and female employees worked the following hours?
```

##### Examples:
```
Input:          Output:
"100000000"     "100,000,000"
"123.40"        "123.4"
```

## format_currency
Returns a formatted currency value. 
Uses Babel's [format_currency](http://babel.pocoo.org/en/latest/api/numbers.html#babel.numbers.format_currency) from `number.py`.

##### Parameters: 
- value:    A single numeric value.
- currency: An optional currency in format 'GBP' (default), 'EUR' etc.

##### Context:
Most commonly used to display a previous answer's currency value in a following question.
```
Of the <em>{{format_currency(answers['total-retail-turnover-answer'])}}</em> total retail turnover, what was the value of internet sales?
```

##### Examples:
```
Input:              Output:
("11.99", "GBP")    "<span class='date'>£11.99</span>"
("11000", "USD")    "<span class='date'>US$11,000.00</span>"
```

## format_address_list
This accepts two lists of address values.
If all the items in the first address list are empty or 'undefined' then we use the second address.

##### Parameters: 
- first_address:    List of address values
- second_address:   List of address values

##### Context:
Used to display a full address for use in a description. 
Used where there is potential that a respondent may provide a new address. 
Therefore it will use that respondent entered address if present otherwise the initial address passed as metadata.
```
{{ format_address_list ([answers['address-line1'], answers['address-line2'], answers['locality'], answers['town-name'], answers['postcode']], [metadata['address_line1'], metadata['address_line2'], metadata['locality'], metadata['town_name'], metadata['postcode']]) }}
```

##### Examples:
```
first_address = ["44", "High Stret", "", "Big City", ""]
second_address = ["123", "Testy", "Place", "Newport", "NP5 7AR"]

Input:                              Output:
(first_address, second_address)     "44<br />High Street<br />Big City"

first_address = [Undefined(), Undefined(), Undefined()]
second_address = ["123", "Testy", "Place", "Newport", "NP5 7AR"]

Input:                              Output:
(first_address, second_address)     "123<br />Testy<br />Place<br />Newport<br />NP5 7AR",
```


## get_current_date
Returns the current date.

##### Parameters: 
- N/A

##### Context:
No real usage but a single question in Census currently only for test purposes.
```
The number of visitors staying in the household on {{ get_current_date() }}
```

##### Example:
```
Output:
<span class='date'>27 December 2018</span>
```

## format_date
Formats a date string, which can be in the format "yyyy-MM-DD", "yyyy-MM" or "yyyy".
The output will be of the form "d MMMM yyyy", "MMMM yyyy" or "yyyy" depending on value passed.
If the value is not a string it will just return the initial value.
Uses Babel's [format_date](http://babel.pocoo.org/en/latest/api/dates.html#babel.dates.format_date).

##### Parameters: 
- value:    String value representing a datetime. Allowable formats "yyyy-MM-DD", "yyyy-MM" or "yyyy".

##### Context:
Used when a date is used in a question.
```
Are you able to report for the period from {{metadata['ref_p_start_date']|format_date}} to {{metadata['ref_p_end_date']|format_date}}?
```

##### Examples:
```
Input:          Output:
"2019-01-01"    "<span class='date'>1 January 2019</span>"
"2019-01"       "<span class='date'>January 2019</span>"
"2019"          "<span class='date'>2019</span>"
```


## format_date_custom
Returns a date in a defined format. In most cases in order to include the day of the week.
Uses Babel's [format_datetime](http://babel.pocoo.org/en/latest/api/dates.html#babel.dates.format_datetime).

##### Parameters: 
- value:        String value representing a datetime. Allowable formats "yyyy-MM-DD".
- date_format:  Format of the date to return. Default 'EEEE d MMMM yyyy'

##### Context:
Used in LMS for both Questions and Options in order to add day of week to a date. 
Often combined with `calculate_offset_from_weekday_in_last_whole_week` filter.
```
Did you have a paid job, either as an employee or self-employed, in the week {{ calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {}) | format_date_custom( 'EEEE d MMMM yyyy' ) }} to {{ calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {}, 'SU') | format_date_custom( 'EEEE d MMMM yyyy' ) }}
 
As an option:
{{calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {}, 'MO') | format_date_custom('EEEE dd MMMM') }}
```

##### Examples:
```
Input:                              Output:
("2018-08-14", "EEEE d MMMM yyyy")  "<span class='date'>Tuesday 14 August 2018</span>"
("2018-08-14", "EEEE d MMMM")       "<span class='date'>Tuesday 14 August</span>"
("2018-08-14", "EEEE d")            "<span class='date'>Tuesday 14</span>"
("2018-08-14", "d MMMM yyyy")       "<span class='date'>14 August 2018</span>"
```

## format_conditional_date
This is to be used when passing multiple dates as multiple arguments. It will return the first valid date formatted.

##### Parameters: 
- *dates:   Multiple date values

##### Context:
Used when you have a list of dates where only one is to be displayed in a priority order. 
The most common use is when a respondent has the option to report for different dates other than the passed metadata period.
If the respondent therefore enters a new reporting period then those dates would be displayed rather than the metadata period.
```
For the period {{ format_conditional_date (answers['period-from'], metadata['ref_p_start_date'])}} to {{ format_conditional_date (answers['period-to'], metadata['ref_p_end_date'])}}, what was the value of {{ first_non_empty_item(metadata['trad_as'], metadata['ru_name']) }}’s <em>total retail turnover</em>?
```

##### Examples:
```
Input:                              Output:
("2016-01-13", "2018-12-30")        "<span class='date'>13 January 2016</span>"
("2016-01-13", None)                "<span class='date'>13 January 2016</span>"
(None, "2018-12-30")                "<span class='date'>30 December 2018</span>"
```

## calculate_offset_from_weekday_in_last_whole_week
Offsets a date from a particular day of the week in the previous week. 
Intended to be used to generate reference date ranges around a particular date
The offsets will always be based on one day of the week in the previous Mon-Sun

##### Parameters: 
- input_datetime:   The datetime (or date) to offset. Defaults to today's date.
- offset:           Dictionary of the number of days, weeks, or years to offset by as integer values
- day_of_week:      The day of the previous week to offset from (two letter abbreviation). Default 'MO'

##### Context:
Used in LMS for both Questions and Options. 
Used for LMS as they would like reference dates that are more relevant to time you're filling in the survey.
Often combined with `format_date_custom` filter.
```
If you had been offered a job in the week starting {{ calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {}) | format_date_custom( 'EEEE d MMMM' ) }} would you be able to start before {{ calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {'weeks':2}) | format_date_custom( 'EEEE d MMMM' ) }}?

As an option:
{{calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {}, 'MO') | format_date_custom('EEEE dd MMMM') }}
```

##### Examples:
```
Input:                              Output:
("2018-08-10", {}, "SU")            "2018-08-05"  # Friday outputs previous Sunday
("2018-08-10", {}, "FR")            "2018-08-03"  # Friday outputs previous Friday
("2018-08-10", {"years": 1}, "FR")  "2019-08-03"  # Friday outputs previous Friday + 1 year

("2018-08-05", {}, "SU")            "2018-07-29"  # Sunday outputs previous Sunday (Must be a full week)
("2018-08-05", {"weeks": 1}, "SU")  "2018-08-05"  # Previous Sunday with +1 week offset

("2018-08-06", {}, "SU")            "2018-08-05"  # Monday outputs previous Sunday
("2018-08-06", {"days": -1}, "SU")  "2018-08-04"  # Previous Sunday with -1 day offset
```

## calculate_years_difference
Returns a difference in years between two dates.

##### Parameters: 
- from_str: datetime string of earliest date.
- to_str:   datetime string of later date. If set to 'now' will use today's date.

##### Context:
Used in Census to work out a person's age from a given date of birth:
```
You are {{ calculate_years_difference (answers['date-of-birth-answer'][group_instance], 'now') }} old. Is this correct?

As an option:
Yes, I am {{ calculate_years_difference (answers['date-of-birth-answer'][group_instance], 'now') }} old
```

##### Examples:
```
Input:                          Output:
("2017-01-30", "2018-01-30')    "1 year"
("2015-02-02", "2018-02-01")    "2 years"
("2016-02-29", "2017-02-28")    "1 year"
("2016-02-29", "2020-02-28")    "3 years"
```

## format_date_range_no_repeated_month_year
Format a date range, ensuring months and years are not repeated.
If the dates are in the same year, the first year (YYYY) will be removed.
If the dates are in the same month and year, the first year (YYYY) and month will be removed.

##### Parameters: 
- start_date:   Initial date in range.
- end_date:     Final date in range.
- date_format:  Format to return date in. Default is 'd MMMM yyyy'.

##### Context:
Used in LMS to simplify dates when often they are only a week apart.
```
Did you have a paid job, either as an employee or self-employed, in the week {{ format_date_range_no_repeated_month_year(calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {}), calculate_offset_from_weekday_in_last_whole_week(collection_metadata['started_at'], {}, 'SU'), 'EEEE d MMMM yyyy') }}?
```

##### Examples:
```
Input:                                              Output:
("2018-08-14", "2018-08-16", "EEEE d MMMM yyyy")    "<span class='date'>Tuesday 14</span> to <span class='date'>Thursday 16 August 2018</span>"
("2018-07-31", "2018-08-16", "EEEE d MMMM yyyy")    "<span class='date'>Tuesday 31 July</span> to <span class='date'>Thursday 16 August 2018</span>"
("2017-12-31", "2018-08-16", "EEEE d MMMM yyyy")    "<span class='date'>Sunday 31 December 2017</span> to <span class='date'>Thursday 16 August 2018</span>"
("2017-12-31", "2018-08-16", "MMMM yyyy")           "<span class='date'>December 2017</span> to <span class='date'>August 2018</span>"
("2018-08-14", "2018-08-16", "MMMM yyyy")           "<span class='date'>August 2018</span> to <span class='date'>August 2018</span>"
("2017-12-31", "2018-08-16", "yyyy")                "<span class='date'>2017</span> to <span class='date'>2018</span>"
("2017-07-31", "2018-08-16", "yyyy")                "<span class='date'>2017</span> to <span class='date'>2018</span>"
("2018-08-14", "2018-08-16", "EEEE d")              "<span class='date'>Tuesday 14</span> to <span class='date'>Thursday 16</span>"
```


## first_non_empty_item
Returns the first non empty value from a number of passed items.
Non empty discards None, 'undefined' or empty strings. It will allow 0 and False.

##### Parameters: 
- *items:   A number of items where some of them could have no value.

##### Context:
Can be used to return the first useable item when you're unsure if all the items you pass in will have a value.
Implemented to replace trad_as_or_ru_name hard coding. 
```
Did any significant changes occur to the total retail turnover for {{ first_non_empty_item(metadata['trad_as'], metadata['ru_name']) }}?
```

##### Examples:
```
Input:                          Output:
("", "Second", "", "Fourth")    "Second"
("", Undefined(), None, "0")    "0"
('', False, None, Undefined())  "False"
```


## format_household_name
Concatenates a list of names into a single space separated string.

##### Parameters: 
- names:    List of names to concatenate

##### Context:
To display a person's full name when the answers are entered as first, middle and last name. 
```
Are you <em>{{ [answers['first-name'][group_instance], answers['middle-names'][group_instance], answers['last-name'][group_instance]] | format_household_name }}<em>?
```

##### Examples:
```
Input:              Output:
["John", "Doe"]     "John Doe"
["John", ""]        "John"
["", "Doe"]         "Doe"
```


## format_household_name_possessive
Concatenates a list of names into a single space separated string and adds the possessive to the end (’s or just ’).

##### Parameters: 
- names:    List of names to concatenate

##### Context:
To display a person's full name when the answers are entered as first, middle and last name but also to express a person's possession within the question. 
```
What is {{[answers['first-name'][group_instance], answers['last-name'][group_instance]] | format_household_name_possessive }} date of birth?
```

##### Examples:
```
Input:              Output:
["John", "Doe"]     "John Doe's"
["John", "Jones"]   "John Jones'"
```

## format_unordered_list
Takes the first list from a list and wraps the items of that list in "ul" and "li" tags.

##### Parameters: 
- list_items:   List of a list of items to be wrapped into a html list

##### Context:
Lists selected pay patterns for MWSS. Used as a description: 
```
{{ answers['pay-pattern-frequency-answer']|format_unordered_list }}
```

##### Examples:
```
Input:                  Output:
[['item 1', 'item 2']]  "<ul><li>item 1</li><li>item 2</li></ul>"
```

## format_unordered_list_missing_items
Will take a list of items and a list of possible items and return the possible items that are not in the initial list.

##### Parameters: 
- possible_items:   All possible items 
- list_items:       Items actually present.

##### Context:
Used to return items that have not been selected from a Checkbox in e-commerce. Used as a description.
```
{{ format_unordered_list_missing_items(['Online ordering or reservation/booking', 'Description of goods or services, price lists', 'Order tracking', 'The possibility for visitors to customise or design the goods or services online', 'Personalised content for regular/repeat visitors', 'Links or references to this business’ social media profiles'], answers['answer1836']) }}
```

##### Examples:
```
possible_items = ['item 1', 'item 2', 'item 3', 'item 4']
list_items = [['item 1', 'item 3']]

Input:                          Output:
(possible_items, list_items)    "<ul><li>item 2</li><li>item 4</li></ul>"
```


## format_household_summary
A merge of `format_household_name` and `format_unordered_list` in order to return a list of full names in "ul" and "li' tags 

##### Parameters: 
- names:    A list containing lists of first, middle and last names [[all first names], [all middle names], [all last names]]

##### Context:
Used in Census to list everybody currently added to who lives here section. Used in a description.
```
<h2 class='neptune'>Your household includes:</h2> {{ [answers['first-name'], answers['middle-names'], answers['last-name']]|format_household_summary }}
```

##### Example:
```
Input: ([
            ['fist1', 'first2', 'first3', 'first4'],
            ['middle1', '', '', 'middle4'],
            ['last1', 'last2', 'last3', '']
        ])

Ouput: "<ul>
            <li>first1 middle1 last1</li>
            <li>first2 last2</li>
            <li>first3 last3</li>
            <li>first4 middle4</li>
       </ul>"
```

## format_repeating_summary
Similar to `format_household_summary` but can handle lists from a series of sources.

##### Parameters: 
- items:        List of lists, If there is a third level of lists, these will be zipped together e.g. [['John', 'Smith'], [['Jane', 'Sarah'], ['Smith', 'Smith']]]
- delimiter:    Default space.

##### Context:
Used in LMS to list everybody currently added to who lives here section. Used in a description.
``` 
{{ [[answers['primary-household-member-first-name'], answers['primary-household-member-last-name']], [answers['other-household-member-first-name'], answers['other-household-member-last-name']], [answers['student-household-member-first-name'], answers['student-household-member-last-name']]] | format_repeating_summary }}
```

##### Examples:
```
Input: ([
            ['John', 'Smith'], 
            [
                ['Jane', 'Sarah'], 
                ['Smith', 'Smythe']
            ]
        ])

Ouput: "<ul>
            <li>John Smith</li>
            <li>Jane Smith</li>
            <li>Sarah Smythe</li>
       </ul>"

       
Input: ([
            [
                ['David', 'Sarah'], 
                ['Smith', 'Smythe']
            ]
        ])

Ouput: "<ul>
            <li>David Smith</li>
            <li>Sarah Smythe</li>
       </ul>"


Input: ([
            ['', 
             '51 Testing Gardens', 
             '', 
             'Bristol', 
             'BS9 1AW'
            ]
        ], 
        delimiter=', ')

Ouput: "<ul>
            <li>51 Testing Gardens, Bristol, BS9 1AW</li>
       </ul>"
```
