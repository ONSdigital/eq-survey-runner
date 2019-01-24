### Group Instance & Group Instance IDs

---

It is recommended that you familiarise yourself with [*repeating routing rules*](repeating_routing_rules.md) before proceeding with this.

Group Instance / Instance IDs are used to identify the instance of an answer acquired from a repeating group.

#### Group Instance (Index)
An answer can have multiple instances, the *group_instance* tracks this instance and is part of the [*Location*](../app/questionnaire/location.py) object which consists of *group_id*, *group_instance*, and the *block_id*.
Currently, `group_instance` is always used as it is part of the Location. Any non-repeating answers will have a `group_instance` of `0` by default.

##### Group Instance - Repeats

The routing [*path*](../app/questionnaire/path_finder.py) is a list of *Location* objects which is created by following routing rules and evaluating skip conditions for all groups and blocks in the schema. 
*The generation of the routing path is carried out on every request.*

When generating the Path, for each group in the schema, we increment the *group_instance* based on the number of times the group repeats. The *no. of repeats* is determined based on the evaluation of the `repeat` rule on each group. 


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
The *no. of repeats* we will have for the above routing rule is based on the number of answers we have with the answer id *repeating-anyone-else* to which the answer is not `"No"`. The *no. of repeats* is incremented for each answer we have with matching id until the routing rule evaluates to *True*.
If there are no answers yet, it will repeat once.

---

#### Group Instance ID

Unlike `group_instance`, the `group_instance_id` is used only when a *Location* has group dependencies. A `group_instance_id` is a *UUID4* string which represents the instance of an answer. 
Locations without dependencies are given the default value of `None` for the `group_instance_id`. 

*The instance of an answer is also stored in `answer_instance` as part of the [Answer](../app/data_model/answer.py) object. However, `answer_instance` is now deprecated in favour of `group_instance_id`.*


##### What defines a group dependency?
A group dependency is a mapping of a `group_id` to the block ids that drive that group. For example if *"group-x"* repeats based on an answer in *"block-a"*, then *"group-x"* is dependent on the driving *"block-a"* - `{ 'group-x': ['block-a'] }`.

Using repeating groups as an example. If `block A` collects a list of people's names and `block B` collects details about each person in the list that `block A` collected, we can say that `block B` is dependent on `block A` being answered. In this scenario, we refer to `block B` as a `dependent` and `block A` as a `driver`. 
A group can also have multiple dependencies. 

When parsing the schema, a [*GroupDependencies*](../app/questionnaire/group_dependencies.py) object is created which stores all the dependencies for a schema by walking through the repeating routing rules.


*GroupDependencies* holds a list of dependents, group drivers and block drivers.


> ***dependents*** (key, value) - the group that is dependent and its dependencies.

> ***group drivers*** - list of blocks driving a group dependency (used with answer_ids)

> ***block drivers*** - list of blocks driving a group dependency (used with answer_id)

We only store unique group/block drivers.

Dependencies for a group is evaluated if the group has any of the following types of repeats:
- `answer_count`
- `answer_count_minus_one`

For groups with either of these repeat types, if the group also has a `skip_condition` then the `id` used in the `when` clause will also be added to the list of dependencies.


An answer is given a `group_instance_id` for the following scenarios:
 - the location's `group_id` is listed as a dependent or a group driver.
 - the location's `block_id` is listed as a group or block driver.

If either of the above conditions are true then the answer is allocated a new `group_instance_id` if there are no existing answers for the given Location.
If the current Locations `group_id` is listed as a ***dependent*** (relies on another group/block) then the current answer is given the same `group_instance_id` as the driver.
To do this, we get a list of all `group_instance_id` for each group/block driver then use the `group_instance` from the current Location to return the matching `group_instance_id`.

##### Example
Schema used: [test_routing_repeat_until.json](../data/en/test_routing_repeat_until.json)

This schema gathers a list of household members then asks for each member's gender.

The first group gathers the primary household member's name.
```json
"blocks": [{
    "id": "primary-name-block",
    "questions": [{
        ...
        "title": "Please enter your name",
        "answers": [{
            "id": "primary-name",
            "label": "First Name",
            "mandatory": true,
            "type": "TextField"
        }]
    }]
}]
```

The second group gather any additional household members, this is a repeating group which repeats `until` the user answers `No` to `repeating-anyone-else` question.

```
{
                ...
                "routing_rules": [{
                    "repeat": {
                        "type": "until",
                        "when": [{
                            "id": "repeating-anyone-else",
                            "condition": "equals",
                            "value": "No"
                        }]
                    }
                }],
                "blocks": [{
                        ...
                            "answers": [{
                                "type": "Radio",
                                "id": "repeating-anyone-else",
                                "mandatory": true,
                                "options": [{
                                        "label": "Yes",
                                        "value": "Yes"
                                    },
                                    {
                                        "label": "No",
                                        "value": "No"
                                    }
                                ]
                            }]
                        ...
                    },
                    {
                        "type": "Question",
                        "id": "repeating-name-block",
                        "questions": [{
                            "id": "repeating-name-question",
                            "title": "Who else lives here?",
                            "type": "General",
                            "answers": [{
                                "id": "repeating-name",
                                "label": "First Name",
                                "mandatory": true,
                                "type": "TextField"
                            }]
                        }]
                    }
                ]
```

The final group gather each member's gender.

```json
{
    "id": "sex-group",
    "routing_rules": [{
        "repeat": {
            "type": "answer_count",
            "answer_ids": [
                "primary-name",
                "repeating-name"
            ]
        }
    }],
    "blocks": [{
        "questions": [{
            "id": "sex-question",
            "title": "What is {{ group_instances[group_instance_id]['repeating-name']|default(group_instances[group_instance_id]['primary-name']) }}'s sex?",
            "answers": [{
                "id": "sex-answer",
                "mandatory": true,
                "type": "Radio",
                "options": [{
                        "label": "Male",
                        "value": "Male"
                    },
                    {
                        "label": "Female",
                        "value": "Female"
                    }
                ]
            }]
        }]
    }]
}
```

Dependencies for the above schema would be the following:

```json
{
  "group_drivers": [
    "primary-name-block",
    "repeating-name-block"
  ],
  "block_drivers": [],
  "sex-group": [
    "primary-name-block",
    "repeating-name-block"
  ]
}
```

The above would result in `group_instance_id` being given to answers in the block `primary-name-block` and `repeating-name-block`.

* Note: Any answer in a *dependent* group `(sex-group)` would get given the same `group_instance_id` which maps to the `group_instance_id` for each answer from the *driving* group. This is how we map the answers together.

So adding 2 members (1 primary, 1 additional) would result in the following:

```json
[
  {
    "answer_id": "primary-name",
    "answer_instance": 0,
    "group_instance": 0,
    "group_instance_id": "5323f640-dee7-4698-be0e-761e6e962c06",
    "value": "John Doe"
  },
  {
    "answer_id": "repeating-anyone-else",
    "answer_instance": 0,
    "group_instance": 0,
    "group_instance_id": null,
    "value": "Yes"
  },
  {
    "answer_id": "repeating-name",
    "answer_instance": 0,
    "group_instance": 0,
    "group_instance_id": "b7645072-2bc5-4051-8d94-46af9e9e849b",
    "value": "Jane Doe"
  },
  {
    "answer_id": "repeating-anyone-else",
    "answer_instance": 0,
    "group_instance": 1,
    "group_instance_id": null,
    "value": "No"
  },
  {
    "answer_id": "sex-answer",
    "answer_instance": 0,
    "group_instance": 0,
    "group_instance_id": "5323f640-dee7-4698-be0e-761e6e962c06",
    "value": "Male"
  },
  {
    "answer_id": "sex-answer",
    "answer_instance": 0,
    "group_instance": 1,
    "group_instance_id": "b7645072-2bc5-4051-8d94-46af9e9e849b",
    "value": "Female"
  }
]
```

The `group_instance_id` for each of the `sex-answer` answers maps to the `primary-name` and `repeating-name` answer. As previously mentioned, the mapping is done as follows:

```python
current_location = Location(group_id='member-group', group_instance=0, block_id='sex-answer')

# The 'member-group' is a dependent and depends on ("primary-name-block", "repeating-name-block")
# Get all answer_ids for each driver.
answer_ids = ['primary-name', 'repeating-name']

# Get all group_instance_ids for each of these answer_ids from the answer_store
group_instance_ids = ['5323f640-dee7-4698-be0e-761e6e962c06', 'b7645072-2bc5-4051-8d94-46af9e9e849b']

# So the current locations group_instance_id would be same as the drivers group_instance_id for the same index (group_instance)
dependent_group_instance = group_instance_ids[current_location.group_instance]

# The same thing is done for the next location which would have a `group_instance` of 1, hence returning 'b7645072-2bc5-4051-8d94-46af9e9e849b'.
```
Source: [_get_dependent_group_instance](../app/helpers/schema_helpers.py)

Since we were repeating for each answer in two different groups *(primary-name, repeating-name)*, the `group_instance` does not match up, hence the use of `group_instance_id`.
