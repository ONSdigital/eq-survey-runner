from unittest import TestCase

import mock
from mock import Mock

from app.templating.summary.summary_item import SummaryItem


class TestSummaryItem(TestCase):

    def test_create_summary_item(self):
        # Given
        question_schema = mock.MagicMock()
        question_schema.answers[0].type = 'positiveinteger'
        answer = Mock()
        answers = Mock()
        answers.__iter__ = Mock(return_value=iter([answer]))

        # When
        item = SummaryItem(question_schema, answers, 'GENERAL')

        # Then
        self.assertEquals(len(item.sub_items), 1)

    def test_create_date_range_summary_item(self):
        # Given
        question_schema = mock.MagicMock()
        question_schema.answers[0].type = 'date'
        from_date_answer = Mock()
        to_date_answer = Mock()
        answers = Mock()
        answers.__iter__ = Mock(return_value=iter([from_date_answer, to_date_answer]))

        # When
        item = SummaryItem(question_schema, answers, 'DATERANGE')

        # Then
        self.assertEquals(len(item.sub_items), 1, 'Only one sub answer should be created for both dates')

    def test_create_multiple_date_range_summary_item(self):
        # Given
        question_schema = mock.MagicMock()
        question_schema.answers[0].type = 'date'
        first_from_date_answer = Mock()
        first_to_date_answer = Mock()
        second_from_date_answer = Mock()
        second_to_date_answer = Mock()
        answers = Mock()
        answers.__iter__ = Mock(return_value=iter([first_from_date_answer, first_to_date_answer, second_from_date_answer,
                                                     second_to_date_answer]))

        # When
        item = SummaryItem(question_schema, answers, 'DATERANGE')

        # Then
        self.assertEquals(len(item.sub_items), 2, 'Only two sub answer should be created for both dates ranges')

    def test_create_multiple_sub_items(self):
        # Given
        schema = mock.MagicMock()
        schema.answers[0].type = 'positiveinteger'
        first_answer = Mock()
        second_answer = Mock()
        answers = Mock()
        answers.__iter__ = Mock(return_value=iter([first_answer, second_answer]))

        # When
        item = SummaryItem(schema, answers, 'GENERAL')

        # Then
        self.assertEquals(len(item.sub_items), 2)
