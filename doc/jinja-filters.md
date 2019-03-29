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

## format_date
Formats a date string, which can be in the format "YYYY-MM-DD", "YYYY-MM" or "YYYY".
The output will be of the form "d MMMM YYYY", "MMMM YYYY" or "YYYY" depending on value passed.
If the value is not a string it will just return the initial value.
Uses Babel's [format_date](http://babel.pocoo.org/en/latest/api/dates.html#babel.dates.format_date).

##### Parameters: 
- value:    String value representing a datetime. Allowable formats "YYYY-MM-DD", "YYYY-MM" or "YYYY".

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
