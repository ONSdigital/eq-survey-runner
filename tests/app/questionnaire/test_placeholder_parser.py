import unittest

from app.data_model.answer_store import AnswerStore
from app.questionnaire.placeholder_parser import PlaceholderParser


class TestPlaceholderParser(unittest.TestCase):
    def test_parse_placeholders(self):
        placeholder_list = [{
            'placeholder': 'first_name',
            'value': {
                'source': 'answers',
                'identifier': 'first-name'
            }
        }]

        answer_store = AnswerStore([
            {
                'answer_id': 'first-name',
                'value': 'Joe'
            }
        ])

        parser = PlaceholderParser(language='en',
                                   answer_store=answer_store)
        placeholders = parser.parse(placeholder_list)

        self.assertIsInstance(placeholders, dict)

        assert 'first_name' in placeholders


class TestPlaceholder(unittest.TestCase):

    @staticmethod
    def test_previous_answer_placeholder():
        placeholder_list = [{
            'placeholder': 'first_name',
            'value': {
                'source': 'answers',
                'identifier': 'first-name'
            }
        }]

        first_name = 'Joe'

        answer_store = AnswerStore([
            {
                'answer_id': 'first-name',
                'value': first_name
            }
        ])

        parser = PlaceholderParser(language='en',
                                   answer_store=answer_store)
        placeholders = parser.parse(placeholder_list)

        assert first_name == placeholders['first_name']

    @staticmethod
    def test_metadata_placeholder():
        placeholder_list = [{
            'placeholder': 'period',
            'value': {
                'source': 'metadata',
                'identifier': 'period_str'
            }
        }]

        period_str = 'Aug 2018'
        parser = PlaceholderParser(language='en', metadata={
            'period_str': period_str
        })

        placeholders = parser.parse(placeholder_list)
        assert period_str == placeholders['period']

    @staticmethod
    def test_previous_answer_transform_placeholder():
        placeholder_list = [{
            'placeholder': 'total_turnover',
            'transforms': [
                {
                    'transform': 'format_currency',
                    'arguments': {
                        'number': {
                            'source': 'answers',
                            'identifier': 'total-retail-turnover-answer'
                        }
                    }
                }
            ]
        }]

        retail_turnover = '1000'

        answer_store = AnswerStore([{
            'answer_id': 'total-retail-turnover-answer',
            'value': retail_turnover
        }])

        parser = PlaceholderParser(language='en',
                                   answer_store=answer_store)
        placeholders = parser.parse(placeholder_list)

        assert placeholders['total_turnover'] == '£1,000.00'

    @staticmethod
    def test_metadata_transform_placeholder():
        placeholder_list = [{
            'placeholder': 'start_date',
            'transforms': [
                {
                    'transform': 'format_date',
                    'arguments': {
                        'date_to_format': {
                            'source': 'metadata',
                            'identifier': 'ref_p_start_date'
                        },
                        'date_format': 'EEEE d MMMM YYYY'
                    }
                }
            ]
        }]

        parser = PlaceholderParser(language='en', metadata={
            'ref_p_start_date': '2019-02-11'
        })
        placeholders = parser.parse(placeholder_list)

        assert placeholders['start_date'] == 'Monday 11 February 2019'

    @staticmethod
    def test_multiple_answer_transform_placeholder():
        placeholder_list = [{
            'placeholder': 'persons_name',
            'transforms': [
                {
                    'transform': 'concatenate_list',
                    'arguments': {
                        'list_to_concatenate': {
                            'source': 'answers',
                            'identifier': ['first-name', 'last-name']
                        },
                        'delimiter': ' '
                    }
                }
            ]
        }]

        parser = PlaceholderParser(language='en', answer_store=AnswerStore([
            {
                'answer_id': 'first-name',
                'value': 'Joe'
            },
            {
                'answer_id': 'last-name',
                'value': 'Bloggs'
            }
        ]))

        placeholders = parser.parse(placeholder_list)

        assert placeholders['persons_name'] == 'Joe Bloggs'

    @staticmethod
    def test_multiple_metadata_transform_placeholder():
        placeholder_list = [{
            'placeholder': 'start_date',
            'transforms': [
                {
                    'transform': 'format_date',
                    'arguments': {
                        'date_to_format': {
                            'source': 'metadata',
                            'identifier': 'ref_p_start_date'
                        },
                        'date_format': 'YYYY-MM-dd'
                    }
                },
                {
                    'transform': 'format_date',
                    'arguments': {
                        'date_to_format': {
                            'source': 'previous_transform',
                        },
                        'date_format': 'dd/MM/YYYY'
                    }
                }
            ]
        }]

        parser = PlaceholderParser(language='en', metadata={
            'ref_p_start_date': '2019-02-11'
        })
        placeholders = parser.parse(placeholder_list)

        assert placeholders['start_date'] == '11/02/2019'

    @staticmethod
    def test_multiple_metadata_list_transform_placeholder():
        placeholder_list = [{
            'placeholder': 'dates',
            'transforms': [
                {
                    'transform': 'concatenate_list',
                    'arguments': {
                        'list_to_concatenate': {
                            'source': 'metadata',
                            'identifier': ['ref_p_start_date', 'ref_p_end_date']
                        },
                        'delimiter': ' '
                    }
                }
            ]
        }]

        parser = PlaceholderParser(language='en', metadata={
            'ref_p_start_date': '2019-02-11',
            'ref_p_end_date': '2019-10-11'
        })
        placeholders = parser.parse(placeholder_list)

        assert placeholders['dates'] == '2019-02-11 2019-10-11'

    @staticmethod
    def test_mixed_transform_placeholder():
        placeholder_list = [{
            'placeholder': 'age_in_years',
            'transforms': [
                {
                    'transform': 'calculate_years_difference',
                    'arguments': {
                        'first_date': {
                            'source': 'answers',
                            'identifier': 'date-of-birth-answer'
                        },
                        'second_date': {
                            'source': 'metadata',
                            'identifier': 'second-date'
                        }
                    }
                }
            ]
        }]

        parser = PlaceholderParser(language='en', answer_store=AnswerStore([
            {
                'answer_id': 'date-of-birth-answer',
                'value': '1999-01-01'
            }
        ]), metadata={
            'second-date': '2019-02-02'
        })
        placeholders = parser.parse(placeholder_list)

        assert placeholders['age_in_years'] == '20'

    @staticmethod
    def test_mixed_transform_placeholder_value():
        placeholder_list = [{
            'placeholder': 'age_in_years',
            'transforms': [
                {
                    'transform': 'calculate_years_difference',
                    'arguments': {
                        'first_date': {
                            'source': 'answers',
                            'identifier': 'date-of-birth-answer'
                        },
                        'second_date': {
                            'value': '2019-02-02'
                        }
                    }
                }
            ]
        }]

        parser = PlaceholderParser(language='en', answer_store=AnswerStore([
            {
                'answer_id': 'date-of-birth-answer',
                'value': '1999-01-01'
            }
        ]))
        placeholders = parser.parse(placeholder_list)

        assert placeholders['age_in_years'] == '20'

    @staticmethod
    def test_chain_transform_placeholder():
        placeholder_list = [{
            'placeholder': 'persons_name',
            'transforms': [
                {
                    'transform': 'concatenate_list',
                    'arguments': {
                        'list_to_concatenate': {
                            'source': 'answers',
                            'identifier': ['first-name', 'last-name']
                        },
                        'delimiter': ' '
                    }
                },
                {
                    'transform': 'format_possessive',
                    'arguments': {
                        'string_to_format': {
                            'source': 'previous_transform'
                        }
                    }
                }
            ]
        }]

        parser = PlaceholderParser(language='en', answer_store=AnswerStore([
            {
                'answer_id': 'first-name',
                'value': 'Joe'
            },
            {
                'answer_id': 'last-name',
                'value': 'Bloggs'
            }
        ]))

        placeholders = parser.parse(placeholder_list)

        assert placeholders['persons_name'] == 'Joe Bloggs’'
