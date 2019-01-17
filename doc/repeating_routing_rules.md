## Routing Rules - Repeats

---

#### Types of Repeats

*1. [until](repeating_routing_rules.md#repeat-type-until)*<br/>
*2. [answer_count](repeating_routing_rules.md#repeat-type-answer_count--answer_count_minus_one)*<br/>
*3. [answer_count_minus_one](repeating_routing_rules.md#repeat-type-answer_count--answer_count_minus_one)*<br/>
*4. [answer_value](repeating_routing_rules.md#repeat-type-answer_value)*

---

### Repeat Type: until

Used to repeat a group *until* a specified condition is satisfied.

##### Context

Commonly used to gather members in a household. Applied to a group which consists of multiple blocks.

##### Example

```json
"routing_rules": [{
    "repeat": {
        "type": "until",
        "when": [{
            "id": "repeating-anyone-else",
            "condition": "equals",
            "value": "No"
        }]
    }
}]
```

The above routing rule will repeat the group until the value to the answer with the id `repeating-anyone-else` is `No`. In a household example, the first block asks the user if they would like to add any more members and the second block is the name input block for the new member. 

Since both blocks are within the same repeating group, we use this routing rule in conjunction with a skip condition which is applied to the second block. This condition skips the second block when they have answered `No` to the first block.

```json
"skip_conditions": [{
    "when": [{
        "id": "repeating-anyone-else",
        "condition": "equals",
        "value": "No"
    }]
}]
```

Schema used: [test_routing_repeat_until.json](../data/en/test_routing_repeat_until.json)

---

### Repeat Type: answer_count / answer_count_minus_one

**answer_count**: Used to repeat a group `n` times, where `n` is the count of answers for a specified `answer_id` or a list of `answer_ids`.

**answer_count_minus_one**: One less than the value for `answer_count`

These *answer_id/ids* are commonly from another repeating group. For example, 1 repeating group to gather a list of household members, and a 2nd repeating group which repeats for each of the household members added.


##### Context


**answer_count**: Commonly used to gather additional details about each member of the household the user has added. For example, gender etc.

**answer_count_minus_one**: Used to gather relationship between the household members.

##### Example

```json
"routing_rules": [{
    "repeat": {
        "type": "answer_count",
        "answer_id": "household-member"
    }
}]
```

or

```json
"routing_rules": [{
    "repeat": {
        "type": "answer_count",
        "answer_ids": [
            "other-household-member",
            "student-household-member"
        ]
    }
}]
```

Adding 2 `other-household-member` and 1 `student-household-member` will mean, the group that has the above routing rule applied would repeat 3 times.

With `"type": "answer_count_minus_one"`, for this scenario the group would repeat twice.

---

### Repeat Type: answer_value

Used to repeat a group `n` times, where `n` is an integer provided by the user.

##### Context

Commonly used to obtain household visitor's details for the number of visitors specified by the user.

##### Example

```json
"routing_rules": [{
    "repeat": {
        "type": "answer_value",
        "answer_id": "overnight-visitors-answer"
    }
}]
```

A value of 3 for the answer *(overnight-visitors-answer)* would result in the group with this repeat rule to repeat 3 times.
