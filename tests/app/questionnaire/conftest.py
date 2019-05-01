import pytest

@pytest.fixture()
def question_variant_schema():
    return {
        'sections': [{
            'id': 'section1',
            'groups': [{
                'id': 'group1',
                'title': 'Group 1',
                'blocks': [
                    {
                        'id': 'block1',
                        'type': 'Question',
                        'title': 'Block 1',
                        'question_variants': [
                            {
                                'when': [{
                                    'id': 'when-answer',
                                    'condition': 'equals',
                                    'value': 'yes'
                                }],
                                'question': {
                                    'id': 'question1',
                                    'title': 'Question 1, Yes',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'label': 'Answer 1 Variant 1'
                                        }
                                    ]
                                }
                            },
                            {
                                'when': [{
                                    'id': 'when-answer',
                                    'condition': 'not equals',
                                    'value': 'yes'
                                }],
                                'question': {
                                    'id': 'question1',
                                    'title': 'Question 1, No',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'label': 'Answer 1 Variant 2'
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }]
        }]
    }

@pytest.fixture()
def list_collector_variant_schema():
    return {
        'sections': [
            {
                'id': 'section',
                'groups': [
                    {
                        'id': 'group',
                        'title': 'List',
                        'blocks': [
                            {
                                'id': 'block1',
                                'type': 'ListCollector',
                                'populates_list': 'people',
                                'add_answer': {
                                    'id': 'answer1',
                                    'value': 'Yes'
                                },
                                'remove_answer': {
                                    'id': 'remove-confirmation',
                                    'value': 'Yes'
                                },
                                'question_variants': [
                                    {
                                        'question': {
                                            'id': 'confirmation-question',
                                            'type': 'General',
                                            'title': 'Collector, Yes',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Collector Answer 1 Variant Yes'
                                                }
                                            ]
                                        },
                                        'when': [{
                                            'id': 'when-answer',
                                            'condition': 'equals',
                                            'value': 'yes'
                                        }],
                                    },
                                    {
                                        'question': {
                                            'id': 'confirmation-question',
                                            'type': 'General',
                                            'title': 'Collector, No',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Collector Answer 1 Variant No'
                                                }
                                            ]
                                        },
                                        'when': [{
                                            'id': 'when-answer',
                                            'condition': 'equals',
                                            'value': 'no'
                                        }],
                                    }
                                ],
                                'add_block': {
                                    'id': 'add-person',
                                    'type': 'Question',
                                    'question_variants': [
                                        {
                                            'question': {
                                                'id': 'add-question',
                                                'type': 'General',
                                                'title': 'Add, Yes',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant Yes'
                                                    }
                                                ]
                                            },
                                            'when': [{
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'yes'
                                            }],
                                        },
                                        {
                                            'question': {
                                                'id': 'add-question',
                                                'type': 'General',
                                                'title': 'Add, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant Yes'
                                                    }
                                                ]
                                            },
                                            'when': [{
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'no'
                                            }],
                                        }
                                    ]
                                },
                                'edit_block': {
                                    'id': 'edit-person',
                                    'type': 'Question',
                                    'question_variants': [
                                        {
                                            'question': {
                                                'id': 'edit-question',
                                                'type': 'General',
                                                'title': 'Edit, Yes',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant Yes'
                                                    }
                                                ]
                                            },
                                            'when': [{
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'yes'
                                            }],
                                        },
                                        {
                                            'question': {
                                                'id': 'edit-question',
                                                'type': 'General',
                                                'title': 'Edit, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant No'
                                                    }
                                                ]
                                            },
                                            'when': [{
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'no'
                                            }],
                                        }
                                    ]
                                },
                                'remove_block': {
                                    'id': 'remove-person',
                                    'type': 'Question',
                                    'question_variants': [
                                        {
                                            'question': {
                                                'id': 'remove-question',
                                                'type': 'General',
                                                'title': 'Remove, Yes',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant Yes'
                                                    }
                                                ]
                                            },
                                            'when': [{
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'yes'
                                            }],
                                        },
                                        {
                                            'question': {
                                                'id': 'remove-question',
                                                'type': 'General',
                                                'title': 'Remove, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant No'
                                                    }
                                                ]
                                            },
                                            'when': [{
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'no'
                                            }],
                                        }
                                    ]
                                }
                            }
                            ]
                    }]
            }]
    }

@pytest.fixture()
def content_variant_schema():
    return {
        'sections': [{
            'id': 'section1',
            'groups': [{
                'id': 'group1',
                'title': 'Group 1',
                'blocks': [
                    {
                        'id': 'block1',
                        'type': 'Question',
                        'title': 'Block 1',
                        'content_variants': [
                            {
                                'content': [{
                                    'title': 'You are over 16'
                                }],
                                'when': [{
                                    'id': 'age-answer',
                                    'condition': 'greater than',
                                    'value': '16'
                                }]
                            },
                            {
                                'content': [{
                                    'title': 'You are under 16'
                                }],
                                'when': [{
                                    'id': 'age-answer',
                                    'condition': 'less than or equal to',
                                    'value': '16'
                                }]
                            },
                            {
                                'content': [{
                                    'title': 'You are ageless'
                                }],
                                'when': [{
                                    'id': 'age-answer',
                                    'condition': 'not set',
                                }]
                            }
                        ]
                    }
                ]
            }]
        }]
    }

@pytest.fixture()
def question_schema():
    return {
        'sections': [{
            'id': 'section1',
            'groups': [{
                'id': 'group1',
                'title': 'Group 1',
                'blocks': [
                    {
                        'id': 'block1',
                        'type': 'Question',
                        'title': 'Block 1',
                        'question': {
                            'id': 'question1',
                            'title': 'A Question',
                            'answers': [
                                {
                                    'id': 'answer1',
                                    'label': 'Answer 1'
                                }
                            ]
                        }
                    }
                ]
            }]
        }]
    }
