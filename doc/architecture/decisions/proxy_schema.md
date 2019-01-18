# New proxy question schema format

## Issues with current schema format

Currently, the solution for proxy questions has some issues, most notably the inability to modify any part of the question apart from the question title.

Since only titles are currently changeable, routing and duplicated blocks have been used to resolve this, but this can cause issues when routing becomes complicated or changes need to be made later on.

### Example

```json
{
    "id": "example",
    "type": "Question",
    "questions": [{
        "id": "example-question",
        "titles": [{
                "value": "Did they work today?",
                "when": [{
                    "id": "proxy-check-answer",
                    "condition": "equals",
                    "value": "proxy"
                }]
            },
            {
                "value": "Did you do any work today?"
            }
        ],
        "type": "General",
        "answers": [{
            "id": "example-answer",
            "mandatory": true,
            "type": "Radio",
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
    }]
}
```

## Requirements of future solution

Must support proxy versions for the following features:

- Answer guidance
    - You / They
        - `How you define your ethnic group is up to you`
        - `How they define their ethnic group is up to them`
    - You / Name
        - `If you are self-employed in your own business, give the business name`
        - `If {proxy_person_name} is self-employed in their own business, give the business name.`
- Detail Answer
    - Label may change between proxy versions:
        - `Please describe your national identity`
        - `Please describe their national identity`
- Interstitial
    - Past / Present and by proxy
        - Past: `Answer the next set of questions for your last main job`
        - Past Proxy: `Answer the next set of questions for {proxy_name_posessive} last main job`
        - Current: `Answer the next set of questions for your main job`
        - Current Proxy: `Answer the next set of questions for {proxy_name_posessive} main job`
    - Same pattern would apply to section introductions if different to interstitials
- Response Options
    - Confirmation
        - `Yes, I am {age_years} old`
        - `Yes, {proxy_name} is {age_years} old`
        - `No, I need to change my date of birth`
        - `No, I need to change {proxy_name_posessive} date of birth`

## Possible solutions

### Questions to answer

- How should proxy be represented downstream?
    - If answer options are different, does the answer id need to be different?
- Does it need a seperate answer id for a different question text?
- Do we ever need to modify keys outside of the `questions` key? At this point, routing can be used instead.

### Multiple questions with skip conditions

Since we currently have the ability to add multiple questions per block, we can also add skip conditions on each question within a block. This allows us to only display one question depending on a proxy question.

```json
{
    "id": "example",
    "type": "Question",
    "questions": [{
        "id": "example-question",
        "title": "Did you do any work today?",
        "type": "General",
        "answers": [{
            "id": "example-answer",
            "mandatory": true,
            "type": "Radio",
            "options": [{
                    "label": "Yes",
                    "value": "Yes"
                },
                {
                    "label": "No",
                    "value": "No"
                }
            ]
        }],
        "skip_conditions": [{
            "when": [{
                "id": "proxy-check-answer",
                "condition": "equals",
                "value": "no"
            }],
        }]
    },
    {
        "id": "example-question-proxy",
        "title": "Did they do any work today?",
        "type": "General",
        "answers": [{
            "id": "example-answer-proxy",
            "mandatory": true,
            "type": "Radio",
            "options": [{
                    "label": "Yes",
                    "value": "Yes"
                },
                {
                    "label": "No",
                    "value": "No"
                }
            ]
        }],
        "skip_conditions": [{
            "when": [{
                "id": "proxy-check-answer",
                "condition": "equals",
                "value": "proxy"
            }],
        }]
    }]
}
```

#### Pros and Cons

- Pros:
    - Very flexible; every attribute of the question can be 'proxied'
    - Support already exists in runner
    - Gives similar flexibility to duplicating the block but avoids issues with routing (since routing is at the block level).
- Cons:
    - Very verbose; Even if only the title changes, the whole question is duplicated. This also means it is difficult to maintain by hand.
    - Authoring tool would need to be able to detect the difference between multiple questions and proxy questions.
    - Does not allow proxy version of block descriptions / type.
- Other:
    - Question and answer ids will be different for the proxy

### Multiple questions with overrides
Similar to above, this version allows multiple questions to be defined with skip conditions. The difference is that this avoids duplication by only specifying different fields in the second question.

```json
{
    "id": "example",
    "type": "Question",
    "questions": [{
        "id": "example-question",
        "title": "Did you do any work today?",
        "type": "General",
        "answers": [{
            "id": "example-answer",
            "mandatory": true,
            "type": "Radio",
            "options": [{
                    "label": "Yes",
                    "value": "Yes"
                },
                {
                    "label": "No",
                    "value": "No"
                }
            ]
        }],
        "skip_conditions": [{
            "when": [{
                "id": "proxy-check-answer",
                "condition": "equals",
                "value": "no"
            }],
        }]
    },
    {
        "title": "Did they do any work today?",
        "skip_conditions": [{
            "when": [{
                "id": "proxy-check-answer",
                "condition": "equals",
                "value": "proxy"
            }],
        }]
    }]
}
```

To make this clearer, it might be worth having a seperate field at the block level that would include overrides. This allows you to see override keys at the same level as question keys. In this example, a `question` object has been used rather than a list.

```json
{
    "id": "example",
    "type": "Question",
    "question": {
        "id": "example-question",
        "title": "Did you do any work today?",
        "type": "General",
        "answers": [{
            "id": "example-answer",
            "mandatory": true,
            "type": "Radio",
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
    },
    "question_overrides": [{
        "title": "Did someone else work today?",
        "when": [{
            "id": "proxy-check-answer",
            "condition": "equals",
            "value": "proxy"
        }],
    }]
}
```

This would mean removing the ability to have multiple questions in a schema. We may not want to do that. If `questions` is still a list, the override structure needs to be a little more complicated:

```json
{
    "id": "example",
    "type": "Question",
    "questions": [{
        "id": "example-question",
        "title": "Did you do any work today?",
        "type": "General",
        "answers": [{
            "id": "example-answer",
            "mandatory": true,
            "type": "Radio",
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
    }],
    "question_overrides": [
        [
            {
                "title": "Did someone else work today?",
                "when": [{
                    "id": "proxy-check-answer",
                    "condition": "equals",
                    "value": "proxy"
                }]
            },{
                "title": "Did someone else work yesterday?",
                "when": [{
                    "id": "proxy-check-answer",
                    "condition": "equals",
                    "value": "past-proxy"
                }],
            }
        ]
    ]
}
```

If both `questions` and `question_overrides` are lists, then another list can be nested in `question_overrides` to provide overrides for each of the `questions`. Since this is overriding a list, every option in the list needs to be added to the overrides. 

Alternatively we could use an index in the question_overrides:

```json
"question_overrides": [
    {
        "title": "Did someone else work today?",
        "when": [{
            "id": "proxy-check-answer",
            "condition": "equals",
            "value": "proxy"
        }],
        "question_index": 0
    }, {
        "title": "Did someone else work yesterday?",
        "when": [{
            "id": "proxy-check-answer",
            "condition": "equals",
            "value": "past-proxy"
        }],
        "question_index": 0
    }
]
```

For both of the previous two solutions, if `answers` are changed, the entire object would need to be replaced. It would also be possible to handle answers_overrides in the same way as question_overrides.

#### Pros and Cons
- Pros
    - Reduces verbosity of proxy questions.
    - Easier to maintain by hand
- Cons
    - Likely needs to be limited to top level keys.
    - Slightly less flexible than multiple questions.
    - May not be immediately obvious how overrides behaves without documentation.
- Other
    - The question and answer_ids would be different for proxies

### Current solution on all string types
We could extend the current solution for titles to all outher string fields on the question. This would increase schema complexity dramatically, but would reduce duplication quite significantly.

### Templating within strings to allow for variations.
Most of the examples for proxies could be acheived with templating on strings. This solution would not work for translations since words which were not originally templated may need to be changed in a translation.
