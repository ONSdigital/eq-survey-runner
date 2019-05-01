# 5. Simplify URLs and extend to support repeating effectively

## Context

The current URL structure used in runner is too long and overloaded. The URL should be as clean and readable as possible.

The current URL structure of runner is:
```
/questionnaire/<eq_id>/<survey_id>/<collection_exercise_id>/<group_id>/<group_instance>/<block_id>
```

Which generates URLs that look like:
```
/questionnaire/1/0005/e9521994-e475-46cc-ae90-8ce4727e908f/pay-pattern/0/pay-pattern-frequency
```

- `eq_id`, `survey_id` and `collection_exercise_id` are unnecessary as we can get that information from the session
- `group_id` isn't needed as all `block_id`s are unique within a given schema and we can look up the group id
- `group_instance` shouldn't be required for blocks that aren't repeating (currently it defaults to 0)  

Removing these from the URL effectively reduces the example above to:
```
/questionnaire/pay-pattern-frequency
```

## Decision

### Block ids are the root urls

```
/<block_id>
/do-you-live-here
/what-is-your-name
/i-dont-live-here
```

- No group id and unnecessary zero based group instance 
- Easy to identify simple non repeating blocks

### Blocks that drive repeats (list creators)

```
/<block_id>
/does-anyone-else-live-here
/<list_identifier>/<add_block_id>
/<list_identifier>/<list_item_id>/<edit_block_id>
/<list_identifier>/<list_item_id>/<remove_block_id>
```

- Listing blocks have a list property declaring what list they populate
- The repeat identifier is generated when adding something to the list
- The repeat identifier is a short (6 characters?) randomly generated string
- Repeat identifiers are persisted to the questionnaire state to keep track of items added to the list
- The schema defines the relationship between the listing and add/change/remove blocks

### Blocks that repeat from a listing

```
/<list_identifier>/<list_item_id>/<block_id>
/householders/<list_item_id>/proxy
/householders/<list_item_id>/sex
/householders/<list_item_id>/date-of-birth
```

- `list_identifier` is a schema defined name for a list that can be created
- `list_item_id` identifies an item in that list
- List ids cannot clash with block ids
- A list can be populated by one or more list creator blocks e.g. "does anyone else live here?" and "is there anyone temporarily away?"

## Consequences

- Cleaner and more readable URLs
- Simpler routing and piping
- Repeats based on anything other than a list will not be possible. This isn't a required feature right now and if a need is identified we can explore what would be required.
