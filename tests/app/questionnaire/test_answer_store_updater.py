# import unittest
# from mock import patch, MagicMock
# from app.data_model.answer_store import Answer, AnswerStore
# from app.data_model.questionnaire_store import QuestionnaireStore
# from app.questionnaire.answer_store_updater import AnswerStoreUpdater
# from app.questionnaire.location import Location
# from app.questionnaire.questionnaire_schema import QuestionnaireSchema
#
#
# class TestAnswerStoreUpdater(unittest.TestCase):
#     def setUp(self):
#         super().setUp()
#
#         self.location = Location('group_foo', 0, 'block_bar')
#         self.schema = MagicMock(spec=QuestionnaireSchema)
#         self.answer_store = MagicMock(spec=AnswerStore)
#         self.questionnaire_store = MagicMock(
#             spec=QuestionnaireStore,
#             completed_blocks=[],
#             answer_store=self.answer_store
#         )
#         self.answer_store_updater = AnswerStoreUpdater(self.location, self.schema, self.questionnaire_store)
#
#     def test_save_form_with_answer_data(self):
#         self.location.block_id = 'household-composition'
#
#         answers = [
#             Answer(
#                 group_instance=0,
#                 answer_id='first-name',
#                 answer_instance=0,
#                 value='Joe'
#             ), Answer(
#                 group_instance=0,
#                 answer_id='middle-names',
#                 answer_instance=0,
#                 value=''
#             ), Answer(
#                 group_instance=0,
#                 answer_id='last-name',
#                 answer_instance=0,
#                 value='Bloggs'
#             ), Answer(
#                 group_instance=0,
#                 answer_id='first-name',
#                 answer_instance=1,
#                 value='Bob'
#             ), Answer(
#                 group_instance=0,
#                 answer_id='middle-names',
#                 answer_instance=1,
#                 value=''
#             ), Answer(
#                 group_instance=0,
#                 answer_id='last-name',
#                 answer_instance=1,
#                 value='Seymour'
#             )
#         ]
#
#         form = MagicMock()
#         form.serialise.return_value = answers
#
#         self.schema.get_answer_ids_for_block.return_value = [
#             'first-name',
#             'middle-names',
#             'last-name'
#         ]
#
#         self.answer_store_updater.save_form(form)
#
#         self.assertEqual(self.questionnaire_store.completed_blocks, [self.location])
#
#         self.assertEqual(len(answers), self.answer_store.add_or_update.call_count)
#
#         # answers should be passed straight through as Answer objects
#         answer_calls = map(mock.call, answers)
#         self.answer_store.add_or_update.assert_has_calls(answer_calls, any_order=True)
#
#     def test_save_form_with_form_data(self):
#         answer_id = 'answer'
#         answer_value = '1000'
#         self.schema.get_answer_ids_for_block.return_value = [answer_id]
#         self.schema.block_has_question_type.return_value = False
#         self.schema.get_group_dependencies.return_value = None
#         self.schema.location_requires_group_instance.return_value = None
#
#         form = MagicMock(data={answer_id: answer_value})
#
#         self.answer_store_updater.save_form(form)
#
#         self.assertEqual(self.questionnaire_store.completed_blocks, [self.location])
#
#         self.assertEqual(1, self.answer_store.add_or_update.call_count)
#         created_answer = self.answer_store.add_or_update.call_args[0][0]
#         self.assertEqual(created_answer.__dict__, {
#             'group_instance': 0,
#             'group_instance_id': None,
#             'answer_id': answer_id,
#             'answer_instance': 0,
#             'value': answer_value
#         })
#
#     @patch('app.questionnaire.answer_store_updater.get_group_instance_id', MagicMock(return_value='df24f3e5-7da9-4a91-8c7a-8798caae2f95'))
#     def test_save_form_stores_specific_group(self):
#         answer_id = 'answer'
#         answer_value = '1000'
#         self.location.group_instance = 1
#         self.schema.get_answer_ids_for_block.return_value = [answer_id]
#         self.schema.block_has_question_type.return_value = False
#         self.schema.get_group_dependencies.return_value = None
#
#         form = MagicMock(data={answer_id: answer_value})
#
#         # @patch('')
#         self.answer_store_updater.save_form(form)
#
#         self.assertEqual(self.questionnaire_store.completed_blocks, [self.location])
#
#         self.assertEqual(1, self.answer_store.add_or_update.call_count)
#         created_answer = self.answer_store.add_or_update.call_args[0][0]
#         self.assertEqual(created_answer.__dict__, {
#             'group_instance': self.location.group_instance,
#             'group_instance_id': 'df24f3e5-7da9-4a91-8c7a-8798caae2f95',
#             'answer_id': answer_id,
#             'answer_instance': 0,
#             'value': answer_value
#         })
#
#     def test_save_form_data_with_default_value(self):
#         answer_id = 'answer'
#         default_value = 0
#         self.schema.get_answer_ids_for_block.return_value = [answer_id]
#         self.schema.get_answer.return_value = {'default': default_value}
#         self.schema.block_has_question_type.return_value = False
#         self.schema.location_requires_group_instance.return_value = False
#
#         # No answer given so will use schema defined default
#         form_data = {
#             answer_id: None
#         }
#         form = MagicMock(data=form_data)
#
#         self.answer_store_updater.save_form(form)
#
#         self.assertEqual(self.questionnaire_store.completed_blocks, [self.location])
#
#         self.assertEqual(1, self.answer_store.add_or_update.call_count)
#         created_answer = self.answer_store.add_or_update.call_args[0][0]
#         self.assertEqual(created_answer.__dict__, {
#             'group_instance': 0,
#             'group_instance_id': None,
#             'answer_id': answer_id,
#             'answer_instance': 0,
#             'value': default_value
#         })
#
#
# class TestAnswerStoreUpdaterDependencies(unittest.TestCase):
#     def setUp(self):
#         super().setUp()
#
#         self.schema = MagicMock(
#             spec=QuestionnaireSchema,
#             get_answer=MagicMock(),
#             get_question=MagicMock(),
#             get_block=MagicMock(),
#             get_group=MagicMock(),
#         )
#         self.answer_store = MagicMock(spec=AnswerStore)
#         self.questionnaire_store = MagicMock(
#             spec=QuestionnaireStore,
#             completed_blocks=[],
#             answer_store=self.answer_store,
#         )
#
#     def test_save_form_removes_completed_block_for_dependencies(self):
#         parent_id, dependent_answer_id = 'parent_answer', 'dependent_answer'
#         parent_location = Location('group', 0, 'min-block')
#         dependent_location = Location('group', 0, 'dependent-block')
#
#         self.questionnaire_store.completed_blocks = [parent_location, dependent_location]
#         self.schema.block_has_question_type.return_value = False
#         self.schema.get_answer_ids_for_block.return_value = [parent_id]
#         self.schema._answer_dependencies = {parent_id: [dependent_answer_id]}
#         self.schema.get_block.return_value = {'id': dependent_location.block_id, 'parent_id': dependent_location.group_id}
#
#         # rotate the hash every time get_hash() is called to simulate the stored answer changing
#         self.answer_store.get_hash.side_effect = ['first_hash', 'second_hash']
#
#         form = MagicMock(data={parent_id: '10'})
#
#         answer_store_updater = AnswerStoreUpdater(parent_location, self.schema, self.questionnaire_store)
#         answer_store_updater.save_form(form)
#
#         self.questionnaire_store.remove_completed_blocks.assert_called_with(location=dependent_location)
#
#         self.assertEqual(1, self.answer_store.add_or_update.call_count)
#         created_answer = self.answer_store.add_or_update.call_args[0][0]
#         self.assertEqual(created_answer.__dict__, {
#             'group_instance': 0,
#             'answer_id': parent_id,
#             'answer_instance': 0,
#             'value': '10'
#         })
#
#         self.assertFalse(self.answer_store.remove.called)
#
#     def test_save_form_removes_completed_block_for_dependencies_repeating(self):
#         """
#         Tests that all dependent completed blocks are removed across all repeating groups when
#         parent answer is not in a repeating group
#         """
#         parent_id, dependent_answer_id = 'parent_answer', 'dependent_answer'
#         parent_location = Location('group', 0, 'min-block')
#         dependent_location = Location('group', 0, 'dependent-block')
#
#         self.questionnaire_store.completed_blocks = [parent_location, dependent_location]
#
#         self.schema.get_answer_ids_for_block.return_value = [parent_id]
#         self.schema.dependencies = {parent_id: [dependent_answer_id]}
#         self.schema.get_block.return_value = {'id': dependent_location.block_id, 'parent_id': dependent_location.group_id}
#
#         # the dependent answer is in a repeating group, the parent is not
#         self.schema.answer_is_in_repeating_group = lambda _answer_id: _answer_id == dependent_answer_id
#
#         # rotate the hash every time get_hash() is called to simulate the stored answer changing
#         self.answer_store.get_hash.side_effect = ['first_hash', 'second_hash']
#
#         form = MagicMock(data={parent_id: '10'})
#
#         answer_store_updater = AnswerStoreUpdater(parent_location, self.schema, self.questionnaire_store)
#         answer_store_updater.save_form(form)
#
#         self.questionnaire_store.remove_completed_blocks.assert_called_with(
#             group_id=dependent_location.group_id,
#             block_id=dependent_location.block_id
#         )
#
#         self.assertEqual(1, self.answer_store.add_or_update.call_count)
#         created_answer = self.answer_store.add_or_update.call_args[0][0]
#         self.assertEqual(created_answer.__dict__, {
#             'group_instance': 0,
#             'answer_id': parent_id,
#             'answer_instance': 0,
#             'value': '10'
#         })
#
#         self.assertFalse(self.answer_store.remove.called)
