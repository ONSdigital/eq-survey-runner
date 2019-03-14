from unittest.mock import patch
import pytest

from app.data_model.answer_store import Answer, AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestPathFinder(AppContextTestCase):  # pylint: disable=too-many-public-methods, too-many-lines

    def test_next_block(self):
        schema = load_schema_from_params('test', 'textfield')

        current_location = Location(block_id='name-block')
        next_location = Location(block_id='summary')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        self.assertEqual(path_finder.get_next_location(current_location=current_location), next_location)

    def test_previous_block(self):
        schema = load_schema_from_params('test', 'textfield')

        current_location = Location(block_id='summary')
        previous_location = Location(block_id='name-block')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        self.assertEqual(path_finder.get_previous_location(current_location=current_location), previous_location)

    def test_introduction_in_path_when_in_schema(self):
        schema = load_schema_from_params('test', 'introduction')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])

        blocks = [b.block_id for b in path_finder.get_full_routing_path()]

        self.assertIn('introduction', blocks)

    def test_introduction_not_in_path_when_not_in_schema(self):
        schema = load_schema_from_params('test', 'checkbox')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])

        with patch('app.questionnaire.rules.evaluate_when_rules', return_value=False):
            blocks = [b.block_id for b in path_finder.get_full_routing_path()]

        self.assertNotIn('introduction', blocks)

    def test_next_with_conditional_path(self):
        schema = load_schema_from_params('test', 'routing_number_equals')

        expected_path = [
            Location('number-question'),
            Location('correct-answer'),
        ]

        answer_1 = Answer(
            answer_id='answer',
            value=123
        )

        answers = AnswerStore()
        answers.add_or_update(answer_1)

        current_location = expected_path[0]
        expected_next_location = expected_path[1]

        completed_blocks = [
            expected_path[0],
        ]

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=completed_blocks)

        actual_next_block = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(actual_next_block, expected_next_location)

    def test_routing_basic_and_conditional_path(self):
        # Given
        schema = load_schema_from_params('test', 'routing_number_equals')

        expected_path = [
            Location('number-question'),
            Location('correct-answer'),
            Location('summary'),
        ]

        answer_1 = Answer(
            answer_id='answer',
            value=123
        )

        answers = AnswerStore()
        answers.add_or_update(answer_1)

        # When
        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])
        routing_path = path_finder.get_full_routing_path()

        # Then
        self.assertEqual(routing_path, expected_path)

    def test_get_next_location_introduction(self):
        schema = load_schema_from_params('test', 'introduction')

        introduction = Location('introduction')

        path_finder = PathFinder(schema, AnswerStore(), {}, [introduction])

        next_location = path_finder.get_next_location(current_location=introduction)

        self.assertEqual('general-business-information-completed', next_location.block_id)

    def test_get_next_location_summary(self):
        schema = load_schema_from_params('test', 'summary')

        answers = AnswerStore()

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        current_location = Location('dessert-block')

        next_location = path_finder.get_next_location(current_location=current_location)

        expected_next_location = Location('summary')

        self.assertEqual(expected_next_location, next_location)

    def test_get_previous_location_introduction(self):
        schema = load_schema_from_params('test', 'introduction')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])

        first_location = Location('general-business-information-completed')

        previous_location = path_finder.get_previous_location(current_location=first_location)

        self.assertEqual('introduction', previous_location.block_id)

    def test_previous_with_conditional_path(self):
        schema = load_schema_from_params('test', 'routing_number_equals')

        expected_path = [
            Location('number-question'),
            Location('correct-answer'),
        ]

        answer_1 = Answer(
            answer_id='answer',
            value=123
        )

        answers = AnswerStore()
        answers.add_or_update(answer_1)

        current_location = expected_path[1]
        expected_previous_location = expected_path[0]

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])
        actual_previous_block = path_finder.get_previous_location(current_location=current_location)

        self.assertEqual(actual_previous_block, expected_previous_location)

    def test_previous_with_conditional_path_alternative(self):
        schema = load_schema_from_params('test', 'routing_number_equals')

        expected_path = [
            Location('number-question'),
            Location('incorrect-answer'),
        ]

        answer_1 = Answer(
            answer_id='answer',
            value=456
        )

        current_location = expected_path[1]
        expected_previous_location = expected_path[0]

        answers = AnswerStore()
        answers.add_or_update(answer_1)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(path_finder.get_previous_location(current_location=current_location),
                         expected_previous_location)

    def test_next_location_goto_summary(self):
        schema = load_schema_from_params('test', 'summary')

        expected_path = [
            Location('radio'),
            Location('test-number-block'),
            Location('dessert-block'),
            Location('summary'),
        ]

        answers = AnswerStore()
        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        current_location = expected_path[2]
        expected_next_location = expected_path[3]

        next_location = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(next_location, expected_next_location)

    def test_next_location_empty_routing_rules(self):
        schema = load_schema_from_params('test', 'checkbox')

        expected_path = [
            Location('mandatory-checkbox'),
            Location('non-mandatory-checkbox'),
            Location('summary')
        ]

        answer_1 = Answer(
            answer_id='mandatory-checkbox-answer',
            value='Cheese',
        )
        answer_2 = Answer(
            answer_id='non-mandatory-checkbox-answer',
            value='deep pan',
        )

        answers = AnswerStore()
        answers.add_or_update(answer_1)
        answers.add_or_update(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        current_location = expected_path[0]
        expected_next_location = expected_path[1]

        next_location = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(next_location, expected_next_location)

    def test_next_with_conditional_path_when_value_not_in_metadata(self):
        schema = load_schema_from_params('test', 'metadata_routing')

        expected_path = [
            Location('block1'),
            Location('block2'),
        ]

        current_location = expected_path[0]

        expected_next_location = expected_path[1]

        metadata = {}

        path_finder = PathFinder(schema, AnswerStore(), metadata=metadata, completed_blocks=[])

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_get_next_location_should_skip_block(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_block')
        current_location = Location('do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add_or_update(Answer(answer_id='do-you-want-to-skip-answer',
                                          value='Yes'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_next_location = Location('a-non-skipped-block')

        with patch('app.questionnaire.path_finder.evaluate_skip_conditions', return_value=True):
            self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_next_location)

    def test_get_next_location_should_skip_group(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        current_location = Location('do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add_or_update(Answer(answer_id='do-you-want-to-skip-answer',
                                          value='Yes'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_next_location = Location('last-group-block')

        with patch('app.questionnaire.path_finder.evaluate_skip_conditions', return_value=True):
            self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_next_location)

    def test_get_next_location_should_not_skip_group(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        current_location = Location('do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add_or_update(Answer(answer_id='do-you-want-to-skip-answer',
                                          value='No'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_location = Location('should-skip')

        with patch('app.questionnaire.path_finder.evaluate_skip_conditions', return_value=False):
            self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_location)

    def test_get_routing_path_when_first_block_in_group_skipped(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        answer_store = AnswerStore()
        answer_store.add_or_update(Answer(answer_id='do-you-want-to-skip-answer',
                                          value='Yes'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_route = [
            {
                'block_id': 'do-you-want-to-skip-block',
                'group_id': 'do-you-want-to-skip-group',
            },
            {
                'block_id': 'summary',
                'group_id': 'should-skip-group',
            }
        ]

        pytest.xfail(reason='Known bug when skipping last group due to summary bundled into it')
        self.assertEqual(path_finder.get_full_routing_path(), expected_route)

    def test_build_path_with_group_routing(self):
        # Given i have answered the routing question
        schema = load_schema_from_params('test', 'routing_group')

        answer_store = AnswerStore()
        answer_store.add_or_update(Answer(answer_id='which-group-answer',
                                          value='group2'))

        # When i build the path
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])
        path = path_finder.build_path()

        # Then it should route me straight to Group2 and not Group1
        self.assertNotIn(Location('group1-block'), path)
        self.assertIn(Location('group2-block'), path)

    def test_return_to_summary_if_complete(self):
        schema = load_schema_from_params('test', 'summary')

        # All blocks completed
        completed_blocks = [
            Location('radio'),
            Location('test-number-block'),
            Location('dessert-block')
        ]

        answer_store = AnswerStore()
        answer_store.add_or_update(Answer(answer_id='radio-answer', value='Bacon'))
        answer_store.add_or_update(Answer(answer_id='test-currency', value='123'))
        answer_store.add_or_update(Answer(answer_id='dessert', value='Cake'))

        summary_location = Location('summary')

        path_finder = PathFinder(schema, answer_store, metadata={}, completed_blocks=completed_blocks)

        self.assertEqual(path_finder.get_next_location(current_location=completed_blocks[0]), summary_location)

    def test_remove_answer_and_block_if_routing_backwards(self):
        schema = load_schema_from_params('test', 'confirmation_question')

        # All blocks completed
        completed_blocks = [
            Location('number-of-employees-total-block'),
            Location('confirm-zero-employees-block')
        ]

        answer_store = AnswerStore()
        number_of_employees_answer = Answer(answer_id='number-of-employees-total', value=0)
        confirm_zero_answer = Answer(answer_id='confirm-zero-employees-answer', value='No')
        answer_store.add_or_update(number_of_employees_answer)
        answer_store.add_or_update(confirm_zero_answer)

        path_finder = PathFinder(schema, answer_store, metadata={}, completed_blocks=completed_blocks)
        self.assertEqual(len(path_finder.completed_blocks), 2)
        self.assertEqual(len(path_finder.answer_store), 2)

        self.assertEqual(path_finder.get_next_location(current_location=completed_blocks[1]), completed_blocks[0])

        self.assertEqual(path_finder.completed_blocks, [completed_blocks[0]])
        self.assertEqual(len(path_finder.answer_store), 1)
