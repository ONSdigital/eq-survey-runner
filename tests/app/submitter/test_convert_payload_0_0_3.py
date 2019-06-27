import simplejson as json

from app.data_model.answer_store import AnswerStore
from app.data_model.answer import Answer
from app.data_model.list_store import ListStore
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.location import Location
from app.submitter.converter import convert_answers
from tests.app.submitter.schema import make_schema, load_schema


def test_convert_answers_to_payload_0_0_3(fake_questionnaire_store):
    full_routing_path = [
        Location(block_id='about you'),
        Location(block_id='where you live'),
    ]

    fake_questionnaire_store.answer_store = AnswerStore(
        [
            Answer('name', 'Joe Bloggs', None).to_dict(),
            Answer('address', '62 Somewhere', None).to_dict(),
        ]
    )

    questionnaire = {
        'survey_id': '021',
        'data_version': '0.0.3',
        'sections': [
            {
                'id': 'household-section',
                'groups': [
                    {
                        'id': 'personal details',
                        'blocks': [
                            {
                                'id': 'about you',
                                'type': 'Question',
                                'question': {
                                    'id': 'crisps-question',
                                    'answers': [{'id': 'name', 'type': 'TextField'}],
                                },
                            }
                        ],
                    },
                    {
                        'id': 'household',
                        'blocks': [
                            {
                                'id': 'where you live',
                                'type': 'Question',
                                'question': {
                                    'id': 'crisps-question',
                                    'answers': [{'id': 'address', 'type': 'TextField'}],
                                },
                            }
                        ],
                    },
                ],
            }
        ],
    }

    # When
    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, full_routing_path
    )

    # Then
    assert len(answer_object['data']) == 2
    assert answer_object['data'][0].value == 'Joe Bloggs'
    assert answer_object['data'][1].value, '62 Somewhere'


def test_convert_payload_0_0_3_multiple_answers(fake_questionnaire_store):
    routing_path = [Location(block_id='crisps')]
    answers = AnswerStore(
        [Answer('crisps-answer', ['Ready salted', 'Sweet chilli']).to_dict()]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'favourite-food',
        'crisps',
        {
            'id': 'crisps-question',
            'answers': [
                {
                    'id': 'crisps-answer',
                    'type': 'Checkbox',
                    'options': [
                        {'label': 'Ready salted', 'value': 'Ready salted'},
                        {'label': 'Sweet chilli', 'value': 'Sweet chilli'},
                        {'label': 'Cheese and onion', 'value': 'Cheese and onion'},
                    ],
                }
            ],
        },
    )

    # When
    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )
    # Then
    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == ['Ready salted', 'Sweet chilli']


def test_radio_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='radio-block')]
    answers = AnswerStore([Answer('radio-answer', 'Coffee').to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'radio-group',
        'radio-block',
        {
            'id': 'radio-question',
            'answers': [
                {
                    'type': 'Radio',
                    'id': 'radio-answer',
                    'options': [
                        {'label': 'Coffee', 'value': 'Coffee'},
                        {'label': 'Tea', 'value': 'Tea'},
                    ],
                }
            ],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == 'Coffee'


def test_number_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='number-block')]
    answers = AnswerStore([Answer('number-answer', 1.755).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'number-group',
        'number-block',
        {
            'id': 'number-question',
            'answers': [{'id': 'number-answer', 'type': 'Number'}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == 1.755


def test_percentage_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='percentage-block')]
    answers = AnswerStore([Answer('percentage-answer', 99).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'percentage-group',
        'percentage-block',
        {
            'id': 'percentage-question',
            'answers': [{'id': 'percentage-answer', 'type': 'Percentage'}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == 99


def test_textarea_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='textarea-block')]
    answers = AnswerStore(
        [Answer('textarea-answer', 'This is an example text!').to_dict()]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'textarea-group',
        'textarea-block',
        {
            'id': 'textarea-question',
            'answers': [{'id': 'textarea-answer', 'type': 'TextArea'}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == 'This is an example text!'


def test_currency_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='currency-block')]
    answers = AnswerStore([Answer('currency-answer', 100).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'currency-group',
        'currency-block',
        {
            'id': 'currency-question',
            'answers': [{'id': 'currency-answer', 'type': 'Currency'}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == 100


def test_dropdown_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='dropdown-block')]
    answers = AnswerStore([Answer('dropdown-answer', 'Rugby is better!').to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'dropdown-group',
        'dropdown-block',
        {
            'id': 'dropdown-question',
            'answers': [
                {
                    'id': 'dropdown-answer',
                    'type': 'Dropdown',
                    'options': [
                        {'label': 'Liverpool', 'value': 'Liverpool'},
                        {'label': 'Chelsea', 'value': 'Chelsea'},
                        {'label': 'Rugby is better!', 'value': 'Rugby is better!'},
                    ],
                }
            ],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    # Then
    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == 'Rugby is better!'


def test_date_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='date-block')]
    answers = AnswerStore(
        [
            Answer('single-date-answer', '01-01-1990').to_dict(),
            Answer('month-year-answer', '01-1990').to_dict(),
        ]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'date-group',
        'date-block',
        {
            'id': 'single-date-question',
            'answers': [{'id': 'single-date-answer', 'type': 'Date'}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1

    assert answer_object['data'][0].value == '01-01-1990'


def test_month_year_date_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='date-block')]
    answers = AnswerStore(
        [
            Answer('single-date-answer', '01-01-1990').to_dict(),
            Answer('month-year-answer', '01-1990').to_dict(),
        ]
    )
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'date-group',
        'date-block',
        {
            'id': 'month-year-question',
            'answers': [{'id': 'month-year-answer', 'type': 'MonthYearDate'}],
        },
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1

    assert answer_object['data'][0].value == '01-1990'


def test_unit_answer(fake_questionnaire_store):
    routing_path = [Location(block_id='unit-block')]
    answers = AnswerStore([Answer('unit-answer', 10).to_dict()])
    fake_questionnaire_store.answer_store = answers

    questionnaire = make_schema(
        '0.0.3',
        'section-1',
        'unit-group',
        'unit-block',
        {'id': 'unit-question', 'answers': [{'id': 'unit-answer', 'type': 'Unit'}]},
    )

    answer_object = convert_answers(
        QuestionnaireSchema(questionnaire), fake_questionnaire_store, routing_path
    )

    assert len(answer_object['data']) == 1
    assert answer_object['data'][0].value == 10


def test_list_item_conversion(fake_questionnaire_store):
    routing_path = [
        Location(block_id='list-collector'),
        Location(block_id='next-interstitial'),
        Location(block_id='another-list-collector-block'),
        Location(block_id='summary'),
    ]

    answer_objects = [
        {'answer_id': 'first-name', 'value': '1', 'list_item_id': 'xJlKBy'},
        {'answer_id': 'last-name', 'value': '1', 'list_item_id': 'xJlKBy'},
        {'answer_id': 'first-name', 'value': '2', 'list_item_id': 'RfAGDc'},
        {'answer_id': 'last-name', 'value': '2', 'list_item_id': 'RfAGDc'},
        {'answer_id': 'anyone-else', 'value': 'No'},
        {'answer_id': 'another-anyone-else', 'value': 'No'},
        {'answer_id': 'extraneous-answer', 'value': 'Bad', 'list_item_id': '123'},
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore({'people': ['xJlKBy', 'RfAGDc']})

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema('test_list_collector')

    output = convert_answers(schema, fake_questionnaire_store, routing_path)

    del answer_objects[-1]

    data_dict = json.loads(json.dumps(output['data'], for_json=True))

    assert sorted(answer_objects, key=lambda x: x['answer_id']) == sorted(
        data_dict, key=lambda x: x['answer_id']
    )


def test_list_item_conversion_empty_list(fake_questionnaire_store):
    """ Test that the list store is populated with an empty list for lists which
    do not have answers yet."""
    routing_path = [
        Location(block_id='list-collector'),
        Location(block_id='next-interstitial'),
        Location(block_id='another-list-collector-block'),
        Location(block_id='summary'),
    ]

    answer_objects = [
        {'answer_id': 'last-name', 'value': '2', 'list_item_id': 'RfAGDc'},
        {'answer_id': 'anyone-else', 'value': 'No'},
        {'answer_id': 'another-anyone-else', 'value': 'No'},
        {'answer_id': 'extraneous-answer', 'value': 'Bad', 'list_item_id': '123'},
    ]

    answers = AnswerStore(answer_objects)

    list_store = ListStore({})

    fake_questionnaire_store.answer_store = answers
    fake_questionnaire_store.list_store = list_store

    schema = load_schema('test_list_collector')

    output = convert_answers(schema, fake_questionnaire_store, routing_path)

    # Answers not on the routing path
    del answer_objects[0]
    del answer_objects[-1]

    data_dict = json.loads(json.dumps(output['data'], for_json=True))

    assert sorted(answer_objects, key=lambda x: x['answer_id']) == sorted(
        data_dict, key=lambda x: x['answer_id']
    )
