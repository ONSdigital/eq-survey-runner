# 7. Relationships

## Context

We need to be able to collect the (one way) relationships between list items. For example, given a list of items A, B and C, we need to be able to capture the relationships between A and B, A and C, and B and C. The previous implementation of relationships relied on group instance, functionality that has now been removed. Now that we have a new [url structure](0005-simplify-urls-and-extend-to-support-repeating-effectively.md) and [lists](0006-make-named-lists-a-first-class-construct.md), we can design how relationships will work.

## Decision

### URLs

The existing url design for lists provides an approach to asking questions related to a given list item:

```
/<list_identifier>/<list_item_id>/<block_id>
```

Using a list named "householders" and a block id of "relationships", the url for all relationships for a given list item would be:

```
/householders/<list_item_id>/relationships
```

Extending this to support a relationship to something, the url for an individual relation would be:

```
/householders/<list_item_id>/relationships/<related_list_item_id>
```

Where the `related_list_item_id` identifies what list item the relation is being formed with.


### Storing relationships

For each list item we need to store both the relationship and the other item it is related to. Extending the current answer store value format to support objects allows us to store this: 

```
{
  "answer_id": "relationship"
  "list_item_id": "a9hd8j",
  "value": {
    "relationship": "Father or Mother",
    "related_list_item_id": "kl9s3y"
  }
}
```

### Schema

The relationship block will be defined as one block in the schema. 

The question text for relationships is dynamic and changes dependent the two people the relationship is being asked of:

```
Thinking of {first_person_name}, how are they related to {second_person_name}
```

The first person name can be resolved by the current placeholder resolution for repeating questions - assume any reference to answer ids when in a repeating section should resolve to the answers for the list item being repeated over:

```
{
  "source": "answers",
  "identifiers": ["first-name", "last-name"],
}
```

The second person name is more difficult, as we will need to resolve the answers for a list item outside of the current repeat. Adding a `list_item_selector` property to the placeholder source definition provides a way to select a list item. This would be a fixed value used to resolve a list item id:

```
{
  "source": "answers",
  "list_item_selector": "related_list_item_id"
  "identifiers": ["first-name", "last-name"],
}
```

In this example runner would need to resolve `related_list_item_id` to the url parameter.

## Consequences

- We will be able to capture relationships between list items.
- Only the forward relationships, starting from the first list item, will be captured.
