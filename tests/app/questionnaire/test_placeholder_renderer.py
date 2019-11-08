from unittest.mock import Mock

from app.data_model.answer_store import AnswerStore
from app.questionnaire.placeholder_renderer import (
    PlaceholderRenderer,
    find_pointers_containing,
)
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from tests.app.app_context_test_case import AppContextTestCase


class TestPlaceholderRenderer(AppContextTestCase):
    def setUp(self):
        super().setUp()

        self.question_json = {
            'id': 'confirm-date-of-birth-proxy',
            'title': 'Confirm date of birth',
            'type': 'General',
            'answers': [
                {
                    'id': 'confirm-date-of-birth-answer-proxy',
                    'mandatory': True,
                    'options': [
                        {
                            'label': {
                                'text': '{person_name_possessive} age is {age_in_years}. Is this correct?',
                                'placeholders': [
                                    {
                                        'placeholder': 'person_name_possessive',
                                        'transforms': [
                                            {
                                                'arguments': {
                                                    'delimiter': ' ',
                                                    'list_to_concatenate': {
                                                        'identifier': [
                                                            'first-name',
                                                            'last-name',
                                                        ],
                                                        'source': 'answers',
                                                    },
                                                },
                                                'transform': 'concatenate_list',
                                            },
                                            {
                                                'arguments': {
                                                    'string_to_format': {
                                                        'source': 'previous_transform'
                                                    }
                                                },
                                                'transform': 'format_possessive',
                                            },
                                        ],
                                    },
                                    {
                                        'placeholder': 'age_in_years',
                                        'transforms': [
                                            {
                                                'transform': 'calculate_years_difference',
                                                'arguments': {
                                                    'first_date': {
                                                        'source': 'answers',
                                                        'identifier': 'date-of-birth-answer',
                                                    },
                                                    'second_date': {'value': 'now'},
                                                },
                                            }
                                        ],
                                    },
                                ],
                            },
                            'value': 'Yes',
                        },
                        {
                            'label': 'No, I need to change their date of birth',
                            'value': 'No',
                        },
                    ],
                    'type': 'Radio',
                }
            ],
        }

        self.pointers = list(
            find_pointers_containing(self.question_json, 'placeholders')
        )

    def test_correct_pointers(self):
        assert self.pointers[0] == '/answers/0/options/0/label'

    def test_renders_pointer(self):
        mock_transform = {
            'transform': 'calculate_years_difference',
            'arguments': {
                'first_date': {
                    'source': 'answers',
                    'identifier': 'date-of-birth-answer',
                },
                'second_date': {'value': '2019-02-01'},
            },
        }

        json_to_render = self.question_json.copy()
        json_to_render['answers'][0]['options'][0]['label']['placeholders'][1][
            'transforms'
        ][0] = mock_transform

        renderer = PlaceholderRenderer(
            language='en',
            schema=QuestionnaireSchema({}),
            answer_store=AnswerStore(
                [
                    {'answer_id': 'first-name', 'value': 'Hal'},
                    {'answer_id': 'last-name', 'value': 'Abelson'},
                    {'answer_id': 'date-of-birth-answer', 'value': '1991-01-01'},
                ]
            ),
        )

        rendered = renderer.render_pointer(
            self.question_json, '/answers/0/options/0/label', list_item_id=None
        )

        assert rendered == 'Hal Abelson’s age is 28. Is this correct?'

    def test_renders_json(self):
        mock_transform = {
            'transform': 'calculate_years_difference',
            'arguments': {
                'first_date': {
                    'source': 'answers',
                    'identifier': 'date-of-birth-answer',
                },
                'second_date': {'value': '2019-02-01'},
            },
        }
        json_to_render = self.question_json.copy()
        json_to_render['answers'][0]['options'][0]['label']['placeholders'][1][
            'transforms'
        ][0] = mock_transform

        renderer = PlaceholderRenderer(
            language='en',
            schema=QuestionnaireSchema({}),
            answer_store=AnswerStore(
                [
                    {'answer_id': 'first-name', 'value': 'Alfred'},
                    {'answer_id': 'last-name', 'value': 'Aho'},
                    {'answer_id': 'date-of-birth-answer', 'value': '1986-01-01'},
                ]
            ),
        )

        rendered_schema = renderer.render(json_to_render, list_item_id=None)
        rendered_label = rendered_schema['answers'][0]['options'][0]['label']

        assert rendered_label == 'Alfred Aho’s age is 33. Is this correct?'

    def test_renders_json_uses_language(self):
        mock_transform = {
            'transform': 'calculate_years_difference',
            'arguments': {
                'first_date': {
                    'source': 'answers',
                    'identifier': 'date-of-birth-answer',
                },
                'second_date': {'value': '2019-02-01'},
            },
        }
        json_to_render = self.question_json.copy()
        json_to_render['answers'][0]['options'][0]['label']['placeholders'][1][
            'transforms'
        ][0] = mock_transform

        renderer = PlaceholderRenderer(
            language='cy',
            schema=QuestionnaireSchema({}),
            answer_store=AnswerStore(
                [
                    {'answer_id': 'first-name', 'value': 'Alfred'},
                    {'answer_id': 'last-name', 'value': 'Aho'},
                    {'answer_id': 'date-of-birth-answer', 'value': '1986-01-01'},
                ]
            ),
        )

        rendered_schema = renderer.render(json_to_render, list_item_id=None)
        rendered_label = rendered_schema['answers'][0]['options'][0]['label']

        assert rendered_label == 'Alfred Aho age is 33. Is this correct?'

    def test_errors_on_invalid_pointer(self):
        renderer = PlaceholderRenderer(language='en', schema=Mock())

        with self.assertRaises(ValueError):
            renderer.render_pointer(self.question_json, '/title', list_item_id=None)

    def test_errors_on_invalid_json(self):
        renderer = PlaceholderRenderer(language='en', schema=Mock())

        with self.assertRaises(ValueError):
            dict_to_render = {'invalid': {'no': 'placeholders', 'in': 'this'}}
            renderer.render_pointer(dict_to_render, '/invalid', list_item_id=None)
