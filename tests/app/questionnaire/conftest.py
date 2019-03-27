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
