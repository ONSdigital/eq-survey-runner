import unittest

from mock import MagicMock

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.data_model.questionnaire_store import QuestionnaireStore
from app.forms.questionnaire_form import QuestionnaireForm
from app.questionnaire.questionnaire_store_updater import QuestionnaireStoreUpdater
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


class TestAnswerStoreUpdater(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.location = Location('block_bar')
        self.schema = MagicMock(spec=QuestionnaireSchema)
        self.answer_store = MagicMock(spec=AnswerStore)
        self.list_store = MagicMock(spec=ListStore)
        self.questionnaire_store = MagicMock(
            spec=QuestionnaireStore,
            completed_blocks=[],
            answer_store=self.answer_store,
            list_store=self.list_store
        )
        self.metadata = MagicMock()
        self.answer_store_updater = None
        self.current_question = None

    def test_save_answers_with_form_data(self):
        answer_id = 'answer'
        answer_value = '1000'

        self.schema.get_answer_ids_for_question.return_value = [answer_id]

        form = MagicMock(spec=QuestionnaireForm, data={answer_id: answer_value})

        self.current_question = self.schema.get_block(self.location.block_id)['question']
        self.answer_store_updater = QuestionnaireStoreUpdater(self.location, self.schema, self.questionnaire_store, self.current_question)
        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert self.answer_store.add_or_update.call_count == 1

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'answer_id': answer_id,
            'list_item_id': None,
            'value': answer_value
        }

    def test_save_answers_data_with_default_value(self):
        answer_id = 'answer'
        default_value = 0

        self.schema.get_answer_ids_for_question.return_value = [answer_id]
        self.schema.get_answers.return_value = [{'default': default_value}]

        # No answer given so will use schema defined default
        form_data = {
            answer_id: None
        }

        form = MagicMock(spec=QuestionnaireForm, data=form_data)

        self.current_question = {
            'answers': [{
                'id': 'answer',
                'default': default_value
            }]
        }
        self.answer_store_updater = QuestionnaireStoreUpdater(self.location, self.schema, self.questionnaire_store, self.current_question)
        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert self.answer_store.add_or_update.call_count == 1

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'answer_id': answer_id,
            'list_item_id': None,
            'value': default_value
        }

    def test_empty_answers(self):
        string_answer_id = 'string-answer'
        checkbox_answer_id = 'checkbox-answer'
        radio_answer_id = 'radio-answer'

        self.schema.get_answer_ids_for_question.return_value = [
            string_answer_id,
            checkbox_answer_id,
            radio_answer_id
        ]

        form_data = {
            string_answer_id: '',
            checkbox_answer_id: [],
            radio_answer_id: None
        }

        form = MagicMock(spec=QuestionnaireForm, data=form_data)

        self.current_question = {
            'answers': [
                {
                    'id': 'string-answer',
                },
                {
                    'id': 'checkbox-answer',
                },
                {
                    'id': 'radio-answer',
                }
            ]
        }
        self.answer_store_updater = QuestionnaireStoreUpdater(self.location, self.schema, self.questionnaire_store, self.current_question)
        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert self.answer_store.add_or_update.call_count == 0

    def test_remove_all_answers_with_list_item_id(self):
        answer_store = AnswerStore(existing_answers=[
            {
                'answer_id': 'test1',
                'value': 1,
                'list_item_id': 'abcdef'
            },
            {
                'answer_id': 'test2',
                'value': 2,
                'list_item_id': 'abcdef'
            },
            {
                'answer_id': 'test3',
                'value': 3,
                'list_item_id': 'uvwxyz'
            }
        ])

        questionnaire_store = MagicMock(
            spec=QuestionnaireStore,
            completed_blocks=[],
            answer_store=answer_store,
            list_store=MagicMock(spec=ListStore)
        )

        self.answer_store_updater = QuestionnaireStoreUpdater(self.location, self.schema, questionnaire_store, self.current_question)
        self.answer_store_updater.remove_all_answers_with_list_item_id('abc', 'abcdef')

        assert len(answer_store) == 1
        assert answer_store.get_answer('test3', 'uvwxyz')
