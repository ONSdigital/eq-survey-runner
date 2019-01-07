import unittest
from unittest import mock
from unittest.mock import call

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

        self.location = Location('group_foo', 0, 'block_bar')
        self.schema = MagicMock(spec=QuestionnaireSchema)
        self.answer_store = MagicMock(spec=AnswerStore)
        self.questionnaire_store = MagicMock(
            spec=QuestionnaireStore,
            completed_blocks=[],
            answer_store=self.answer_store
        )
        self.answer_store_updater = AnswerStoreUpdater(self.location, self.schema, self.questionnaire_store)
        self.schema.location_requires_group_instance.return_value = False

    def test_save_answers_with_answer_data(self):
        self.location.block_id = 'household-composition'
        self.schema.get_group_dependencies.return_value = None
        self.schema.get_answer_ids_for_block.return_value = ['first-name', 'middle-names', 'last-name']

        answers = [
            Answer(
                group_instance=0,
                group_instance_id='group-0',
                answer_id='first-name',
                answer_instance=0,
                value='Joe'
            ), Answer(
                group_instance=0,
                group_instance_id='group-0',
                answer_id='middle-names',
                answer_instance=0,
                value=''
            ), Answer(
                group_instance=0,
                group_instance_id='group-0',
                answer_id='last-name',
                answer_instance=0,
                value='Bloggs'
            ), Answer(
                group_instance=0,
                group_instance_id='group-1',
                answer_id='first-name',
                answer_instance=1,
                value='Bob'
            ), Answer(
                group_instance=0,
                group_instance_id='group-1',
                answer_id='middle-names',
                answer_instance=1,
                value=''
            ), Answer(
                group_instance=0,
                group_instance_id='group-1',
                answer_id='last-name',
                answer_instance=1,
                value='Seymour'
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
        self.schema.get_group_dependencies.return_value = None

        form = MagicMock(spec=QuestionnaireForm, data={answer_id: answer_value})

        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert self.answer_store.add_or_update.call_count == 1

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'group_instance': 0,
            'group_instance_id': None,
            'answer_id': answer_id,
            'answer_instance': 0,
            'value': answer_value
        }

    def test_save_answers_stores_specific_group(self):
        answer_id = 'answer'
        answer_value = '1000'

        self.location.group_instance = 1
        self.schema.get_answer_ids_for_block.return_value = [answer_id]
        self.schema.get_group_dependencies.return_value = None

        form = MagicMock(spec=QuestionnaireForm, data={answer_id: answer_value})

        self.answer_store_updater.save_answers(form)

        assert self.questionnaire_store.completed_blocks == [self.location]
        assert self.answer_store.add_or_update.call_count == 1

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'group_instance': self.location.group_instance,
            'group_instance_id': None,
            'answer_id': answer_id,
            'answer_instance': 0,
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
            'group_instance': 0,
            'group_instance_id': None,
            'answer_id': answer_id,
            'answer_instance': 0,
            'value': default_value
        }

    def test_remove_empty_household_members_from_answer_store(self):
        empty_household_answers = [
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': ''
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': ''
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': ''
            },
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            }
        ]

        self.schema.get_answer_ids_for_block.return_value = ['first-name', 'middle-names', 'last-name']
        self.answer_store.filter.return_value = iter(empty_household_answers)

        self.answer_store_updater.remove_empty_household_members()

        remove_answer_calls = [call(answer_ids=['first-name', 'middle-names', 'last-name'], answer_instance=0),
                               call(answer_ids=['first-name', 'middle-names', 'last-name'], answer_instance=1)]

        # both instances of the answer should be removed
        assert remove_answer_calls in self.answer_store.remove.call_args_list
        assert self.answer_store.remove.call_count == 2

    def test_remove_empty_household_members_values_entered_are_stored(self):
        household_answers = [
            # Answered
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': 'Joe'
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': ''
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': 'Bloggs'
            },

            # Unanswered
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            }
        ]

        self.schema.get_answer_ids_for_block.return_value = ['first-name', 'middle-names', 'last-name']
        self.answer_store.filter.return_value = iter(household_answers)

        self.answer_store_updater.remove_empty_household_members()

        # only the second instance of the answer should be removed
        assert self.answer_store.remove.call_count == 1

        remove_answer_calls = [call(answer_ids=['first-name', 'middle-names', 'last-name'], answer_instance=1)]
        assert remove_answer_calls in self.answer_store.remove.call_args_list

    def test_remove_empty_household_members_partial_answers_are_stored(self):
        self.location.block_id = 'household-composition'
        self.schema.get_group_dependencies.return_value = None

        household_answers = [
            # Answered
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': 'Joe'
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': 'J'
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': 'Bloggs'
            },

            # Partially answered
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': ''
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 1,
                'value': 'Last name only'
            },
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 2,
                'value': 'First name only'
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 2,
                'value': ''
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 2,
                'value': ''
            }
        ]
        self.answer_store.filter.return_value = iter(household_answers)
        self.schema.get_answer_ids_for_block.return_value = ['first-name', 'middle-names', 'last-name']

        self.answer_store_updater.remove_empty_household_members()

        # no answers should be removed
        assert self.answer_store.remove.called is False

    def test_remove_empty_household_members_middle_name_only_not_stored(self):
        household_answer = [
            {
                'answer_id': 'first-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': ''
            },
            {
                'answer_id': 'middle-names',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': 'should not be saved'
            },
            {
                'answer_id': 'last-name',
                'group_instance_id': None,
                'group_instance': 0,
                'answer_instance': 0,
                'value': ''
            }
        ]

        self.schema.get_answer_ids_for_block.return_value = ['first-name', 'middle-names', 'last-name']
        self.answer_store.filter.return_value = iter(household_answer)

        self.answer_store_updater.remove_empty_household_members()

        # partial answer should be removed
        assert self.answer_store.remove.call_count == 1

        remove_answer_calls = [call(answer_ids=['first-name', 'middle-names', 'last-name'], answer_instance=0)]
        assert remove_answer_calls in self.answer_store.remove.call_args_list

    def test_save_answers_removes_completed_block_for_dependencies(self):
        parent_id, dependent_answer_id = 'parent_answer', 'dependent_answer'
        self.location = parent_location = Location('group', 0, 'min-block')
        dependent_location = Location('group', 0, 'dependent-block')

        self.questionnaire_store.completed_blocks = [parent_location, dependent_location]
        self.schema.get_answer_ids_for_block.return_value = [parent_id]
        self.schema.answer_dependencies = {parent_id: [dependent_answer_id]}
        self.schema.get_block.return_value = {'id': dependent_location.block_id, 'parent_id': dependent_location.group_id}

        # rotate the hash every time get_hash() is called to simulate the stored answer changing
        self.answer_store.get_hash.side_effect = ['first_hash', 'second_hash']

        form = MagicMock(spec=QuestionnaireForm, data={parent_id: '10'})

        self.schema.get_group_dependencies.return_value = None

        self.answer_store_updater.save_answers(form)

        assert self.answer_store.add_or_update.call_count == 1
        assert self.answer_store.remove.called is False

        self.questionnaire_store.remove_completed_blocks.assert_called_with(location=dependent_location)

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'group_instance': 0,
            'group_instance_id': None,
            'answer_id': parent_id,
            'answer_instance': 0,
            'value': '10'
        }

    def test_save_answers_removes_completed_block_for_dependencies_repeating_on_non_repeating_answer(self):
        """
        Tests that all dependent completed blocks are removed across all repeating groups when
        parent answer is not in a repeating group
        """
        parent_id, dependent_answer_id = 'parent_answer', 'dependent_answer'
        self.location = parent_location = Location('group', 0, 'min-block')
        dependent_location = Location('group', 0, 'dependent-block')

        self.questionnaire_store.completed_blocks = [parent_location, dependent_location]
        self.schema.get_answer_ids_for_block.return_value = [parent_id]
        self.schema.answer_dependencies = {parent_id: [dependent_answer_id]}
        self.schema.get_block.return_value = {'id': dependent_location.block_id, 'parent_id': dependent_location.group_id}

        # the dependent answer is in a repeating group, the parent is not
        self.schema.answer_is_in_repeating_group = lambda _answer_id: _answer_id == dependent_answer_id

        # rotate the hash every time get_hash() is called to simulate the stored answer changing
        self.answer_store.get_hash.side_effect = ['first_hash', 'second_hash']

        form = MagicMock(spec=QuestionnaireForm, data={parent_id: '10'})

        self.answer_store_updater.save_answers(form)

        self.questionnaire_store.remove_completed_blocks.assert_called_with(
            group_id=dependent_location.group_id,
            block_id=dependent_location.block_id
        )

        assert self.answer_store.add_or_update.call_count == 1
        assert self.answer_store.remove.called is False

        created_answer = self.answer_store.add_or_update.call_args[0][0]
        assert created_answer.__dict__ == {
            'group_instance': 0,
            'group_instance_id': None,
            'answer_id': parent_id,
            'answer_instance': 0,
            'value': '10'
        }
