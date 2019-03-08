import unittest
from unittest import mock

from mock import MagicMock

from app.data_model.answer_store import Answer, AnswerStore
from app.data_model.questionnaire_store import QuestionnaireStore
from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire.answer_store_updater import AnswerStoreUpdater
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


class TestAnswerStoreUpdater(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.location = Location('block_bar')
        self.schema = MagicMock(spec=QuestionnaireSchema)
        self.answer_store = MagicMock(spec=AnswerStore)
        self.questionnaire_store = MagicMock(
            spec=QuestionnaireStore,
            completed_blocks=[],
            answer_store=self.answer_store
        )
        self.answer_store_updater = AnswerStoreUpdater(self.location, self.schema, self.questionnaire_store)

    def test_save_answers_with_answer_data(self):
        self.location.block_id = 'household-composition'
        self.schema.get_answer_ids_for_block.return_value = ['first-name', 'middle-names', 'last-name']

        answers = [
            Answer(
                answer_id='first-name',
                value='Joe'
            ), Answer(
                answer_id='middle-names',
                value=''
            ), Answer(
                answer_id='last-name',
                value='Bloggs'
            )
        ]

        form = MagicMock()
        form.serialise.return_value = answers

        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert len(answers) == self.answer_store.add_or_update.call_count

        # answers should be passed straight through as Answer objects
        answer_calls = list(map(mock.call, answers))
        assert answer_calls in self.answer_store.add_or_update.call_args_list

    def test_save_answers_with_form_data(self):
        answer_id = 'answer'
        answer_value = '1000'

        self.schema.get_answer_ids_for_block.return_value = [answer_id]

        form = MagicMock(spec=QuestionnaireForm, data={answer_id: answer_value})

        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert self.answer_store.add_or_update.call_count == 1

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'answer_id': answer_id,
            'value': answer_value
        }

    def test_save_answers_data_with_default_value(self):
        answer_id = 'answer'
        default_value = 0

        self.schema.get_answer_ids_for_block.return_value = [answer_id]
        self.schema.get_answer.return_value = {'default': default_value}

        # No answer given so will use schema defined default
        form_data = {
            answer_id: None
        }

        form = MagicMock(spec=QuestionnaireForm, data=form_data)

        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert self.answer_store.add_or_update.call_count == 1

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'answer_id': answer_id,
            'value': default_value
        }
