# pylint: disable=redefined-outer-name
import pytest

from app.data_model.answer_store import AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.placeholder_parser import PlaceholderParser


@pytest.fixture
def placeholder_list():
    return [
        {
            'placeholder': 'first_name',
            'value': {'source': 'answers', 'identifier': 'first-name'},
        }
    ]


@pytest.fixture
def answer_store():
    return AnswerStore([{'answer_id': 'first-name', 'value': 'Joe'}])


@pytest.fixture
def location():
    return Location('test-section', 'test-block', 'test-list', 'list_item_id')


@pytest.fixture
def parser(answer_store, location):
    return PlaceholderParser(
        language='en', answer_store=answer_store, location=location
    )


@pytest.fixture
def parser_with_list_item_id(answer_store, location):
    return PlaceholderParser(
        language='en',
        answer_store=answer_store,
        location=location,
        list_item_id='test-list-item-id',
    )


@pytest.fixture()
def question_variant_schema_evaluates_to_false():
    return {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'title': 'Group 1',
                        'blocks': [
                            {
                                'id': 'block1',
                                'type': 'Question',
                                'title': 'Block 1',
                                'question_variants': [
                                    {
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'yes',
                                            }
                                        ],
                                        'question': {
                                            'id': 'question1',
                                            'title': 'Question 1, Yes',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Answer 1 Variant 1',
                                                }
                                            ],
                                        },
                                    },
                                    {
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'no',
                                            }
                                        ],
                                        'question': {
                                            'id': 'question1',
                                            'title': 'Question 1, No',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Answer 1 Variant 2',
                                                }
                                            ],
                                        },
                                    },
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def question_variant_schema():
    return {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'title': 'Group 1',
                        'blocks': [
                            {
                                'id': 'block1',
                                'type': 'Question',
                                'title': 'Block 1',
                                'question_variants': [
                                    {
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'yes',
                                            }
                                        ],
                                        'question': {
                                            'id': 'question1',
                                            'title': 'Question 1, Yes',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Answer 1 Variant 1',
                                                }
                                            ],
                                        },
                                    },
                                    {
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'not equals',
                                                'value': 'yes',
                                            }
                                        ],
                                        'question': {
                                            'id': 'question1',
                                            'title': 'Question 1, No',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Answer 1 Variant 2',
                                                }
                                            ],
                                        },
                                    },
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def single_question_schema():
    return {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'title': 'Group 1',
                        'blocks': [
                            {
                                'id': 'block1',
                                'type': 'Question',
                                'title': 'Block 1',
                                'question': {
                                    'id': 'question1',
                                    'title': 'Question 1, Yes',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'label': 'Answer 1 Variant 1',
                                            'default': 'test',
                                        }
                                    ],
                                },
                            }
                        ],
                    }
                ],
            }
        ]
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
                                'for_list': 'people',
                                'add_answer': {'id': 'answer1', 'value': 'Yes'},
                                'remove_answer': {
                                    'id': 'remove-confirmation',
                                    'value': 'Yes',
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
                                                    'label': 'Collector Answer 1 Variant Yes',
                                                }
                                            ],
                                        },
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'yes',
                                            }
                                        ],
                                    },
                                    {
                                        'question': {
                                            'id': 'confirmation-question',
                                            'type': 'General',
                                            'title': 'Collector, No',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Collector Answer 1 Variant No',
                                                }
                                            ],
                                        },
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'no',
                                            }
                                        ],
                                    },
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
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'yes',
                                                }
                                            ],
                                        },
                                        {
                                            'question': {
                                                'id': 'add-question',
                                                'type': 'General',
                                                'title': 'Add, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'no',
                                                }
                                            ],
                                        },
                                    ],
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
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'yes',
                                                }
                                            ],
                                        },
                                        {
                                            'question': {
                                                'id': 'edit-question',
                                                'type': 'General',
                                                'title': 'Edit, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant No',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'no',
                                                }
                                            ],
                                        },
                                    ],
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
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'yes',
                                                }
                                            ],
                                        },
                                        {
                                            'question': {
                                                'id': 'remove-question',
                                                'type': 'General',
                                                'title': 'Remove, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant No',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'no',
                                                }
                                            ],
                                        },
                                    ],
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def content_variant_schema():
    return {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'title': 'Group 1',
                        'blocks': [
                            {
                                'id': 'block1',
                                'type': 'Question',
                                'title': 'Block 1',
                                'content_variants': [
                                    {
                                        'content': [{'title': 'You are over 16'}],
                                        'when': [
                                            {
                                                'id': 'age-answer',
                                                'condition': 'greater than',
                                                'value': '16',
                                            }
                                        ],
                                    },
                                    {
                                        'content': [{'title': 'You are under 16'}],
                                        'when': [
                                            {
                                                'id': 'age-answer',
                                                'condition': 'less than or equal to',
                                                'value': '16',
                                            }
                                        ],
                                    },
                                    {
                                        'content': [{'title': 'You are ageless'}],
                                        'when': [
                                            {'id': 'age-answer', 'condition': 'not set'}
                                        ],
                                    },
                                ],
                            }
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture()
def question_schema():
    return {
        'sections': [
            {
                'id': 'section1',
                'groups': [
                    {
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
                                    'answers': [{'id': 'answer1', 'label': 'Answer 1'}],
                                },
                            }
                        ],
                    }
                ],
            }
        ]
    }


# pylint: disable=line-too-long
@pytest.fixture()
def relationship_collector_schema():
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
                                'for_list': 'people',
                                'add_answer': {'id': 'answer1', 'value': 'Yes'},
                                'remove_answer': {
                                    'id': 'remove-confirmation',
                                    'value': 'Yes',
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
                                                    'label': 'Collector Answer 1 Variant Yes',
                                                }
                                            ],
                                        },
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'yes',
                                            }
                                        ],
                                    },
                                    {
                                        'question': {
                                            'id': 'confirmation-question',
                                            'type': 'General',
                                            'title': 'Collector, No',
                                            'answers': [
                                                {
                                                    'id': 'answer1',
                                                    'label': 'Collector Answer 1 Variant No',
                                                }
                                            ],
                                        },
                                        'when': [
                                            {
                                                'id': 'when-answer',
                                                'condition': 'equals',
                                                'value': 'no',
                                            }
                                        ],
                                    },
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
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'yes',
                                                }
                                            ],
                                        },
                                        {
                                            'question': {
                                                'id': 'add-question',
                                                'type': 'General',
                                                'title': 'Add, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'no',
                                                }
                                            ],
                                        },
                                    ],
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
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'yes',
                                                }
                                            ],
                                        },
                                        {
                                            'question': {
                                                'id': 'edit-question',
                                                'type': 'General',
                                                'title': 'Edit, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant No',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'no',
                                                }
                                            ],
                                        },
                                    ],
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
                                                        'label': 'Answer 1 Variant Yes',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'yes',
                                                }
                                            ],
                                        },
                                        {
                                            'question': {
                                                'id': 'remove-question',
                                                'type': 'General',
                                                'title': 'Remove, No',
                                                'answers': [
                                                    {
                                                        'id': 'answer1',
                                                        'label': 'Answer 1 Variant No',
                                                    }
                                                ],
                                            },
                                            'when': [
                                                {
                                                    'id': 'when-answer',
                                                    'condition': 'equals',
                                                    'value': 'no',
                                                }
                                            ],
                                        },
                                    ],
                                },
                            },
                            {
                                'type': 'RelationshipCollector',
                                'id': 'relationships',
                                'title': 'This will iterate over the people list, capturing the one way relationships.',
                                'for_list': 'people',
                                'question': {
                                    'id': 'relationship-question',
                                    'type': 'General',
                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>...</em>',
                                    'answers': [
                                        {
                                            'id': 'relationship-answer',
                                            'mandatory': True,
                                            'type': 'Relationship',
                                            'playback': '{second_person_name} is {first_person_name_possessive} <em>…</em>',
                                            'options': [
                                                {
                                                    'label': 'Husband or Wife',
                                                    'value': 'Husband or Wife',
                                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>husband or wife</em>',
                                                    'playback': '{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>',
                                                },
                                                {
                                                    'label': 'Legally registered civil partner',
                                                    'value': 'Legally registered civil partner',
                                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>legally registered civil partner</em>',
                                                    'playback': '{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>',
                                                },
                                                {
                                                    'label': 'Son or daughter',
                                                    'value': 'Son or daughter',
                                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>',
                                                    'playback': '{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>',
                                                },
                                            ],
                                        }
                                    ],
                                },
                            },
                            {
                                'type': 'RelationshipCollector',
                                'id': 'relationships-that-dont-point-to-list-collector',
                                'title': 'This will iterate over the people list, capturing the one way relationships.',
                                'for_list': 'not-people',
                                'question': {
                                    'id': 'relationship-question',
                                    'type': 'General',
                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>...</em>',
                                    'answers': [
                                        {
                                            'id': 'relationship-answer',
                                            'mandatory': True,
                                            'type': 'Relationship',
                                            'playback': '{second_person_name} is {first_person_name_possessive} <em>…</em>',
                                            'options': [
                                                {
                                                    'label': 'Husband or Wife',
                                                    'value': 'Husband or Wife',
                                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>husband or wife</em>',
                                                    'playback': '{second_person_name} is {first_person_name_possessive} <em>husband or wife</em>',
                                                },
                                                {
                                                    'label': 'Legally registered civil partner',
                                                    'value': 'Legally registered civil partner',
                                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>legally registered civil partner</em>',
                                                    'playback': '{second_person_name} is {first_person_name_possessive} <em>legally registered civil partner</em>',
                                                },
                                                {
                                                    'label': 'Son or daughter',
                                                    'value': 'Son or daughter',
                                                    'title': 'Thinking of {first_person_name}, {second_person_name} is their <em>son or daughter</em>',
                                                    'playback': '{second_person_name} is {first_person_name_possessive} <em>son or daughter</em>',
                                                },
                                            ],
                                        }
                                    ],
                                },
                            },
                        ],
                    }
                ],
            }
        ]
    }


@pytest.fixture
def section_with_repeating_list():
    return {
        'sections': [
            {
                'id': 'personal-details-section',
                'title': 'Personal Details',
                'repeat': {'for_list': 'people'},
                'groups': [
                    {
                        'id': 'personal-details-group',
                        'title': 'Personal Details',
                        'blocks': [
                            {
                                'id': 'proxy',
                                'question': {
                                    'answers': [
                                        {
                                            'default': 'Yes',
                                            'id': 'proxy-answer',
                                            'mandatory': False,
                                            'options': [
                                                {
                                                    'label': 'No, I’m answering for myself',
                                                    'value': 'No',
                                                },
                                                {'label': 'Yes', 'value': 'Yes'},
                                            ],
                                            'type': 'Radio',
                                        }
                                    ],
                                    'id': 'proxy-question',
                                    'title': 'Are you answering the questions on behalf of someone else?',
                                    'type': 'General',
                                },
                                'type': 'Question',
                            }
                        ],
                    }
                ],
            }
        ]
    }
