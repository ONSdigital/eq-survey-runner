from unittest.mock import patch
import pytest

from app.data_model.answer_store import Answer, AnswerStore
from app.data_model.completed_store import CompletedStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestPathFinder(
    AppContextTestCase
):  # pylint: disable=too-many-public-methods, too-many-lines
    def test_simple_path(self):
        schema = load_schema_from_params('test', 'textfield')
        completed_store = CompletedStore({'locations': [{'block_id': 'name-block'}]})
        path_finder = PathFinder(
            schema, AnswerStore(), metadata={}, completed_store=completed_store
        )

        section = schema.get_section_for_block_id('name-block')
        routing_path = path_finder.routing_path(section)

        assumed_routing_path = [
            Location(block_id='name-block'),
            Location(block_id='summary'),
        ]

        self.assertEqual(routing_path, assumed_routing_path)

    def test_introduction_in_path_when_in_schema(self):
        schema = load_schema_from_params('test', 'introduction')
        current_section = schema.get_section('introduction-section')

        path_finder = PathFinder(
            schema, AnswerStore(), metadata={}, completed_store=CompletedStore()
        )

        blocks = [b.block_id for b in path_finder.routing_path(current_section)]

        self.assertIn('introduction', blocks)

    def test_introduction_not_in_path_when_not_in_schema(self):
        schema = load_schema_from_params('test', 'checkbox')
        current_section = schema.get_section('default-section')
        path_finder = PathFinder(
            schema, AnswerStore(), metadata={}, completed_store=CompletedStore()
        )

        with patch('app.questionnaire.rules.evaluate_when_rules', return_value=False):
            blocks = [b.block_id for b in path_finder.routing_path(current_section)]

        self.assertNotIn('introduction', blocks)

    def test_routing_path_with_conditional_path(self):
        schema = load_schema_from_params('test', 'routing_number_equals')
        current_section = schema.get_section_for_block_id('number-question')
        expected_path = [
            Location(block_id='number-question'),
            Location(block_id='correct-answer'),
            Location(block_id='summary'),
        ]

        answer = Answer(answer_id='answer', value=123)
        answers = AnswerStore()
        answers.add_or_update(answer)

        completed_store = CompletedStore(
            {'locations': [{'block_id': 'number-question'}]}
        )

        path_finder = PathFinder(
            schema, answer_store=answers, metadata={}, completed_store=completed_store
        )

        routing_path = path_finder.routing_path(current_section)

        self.assertEqual(routing_path, expected_path)

    def test_routing_basic_and_conditional_path(self):
        # Given
        schema = load_schema_from_params('test', 'routing_number_equals')
        current_section = schema.get_section_for_block_id('number-question')
        expected_path = [
            Location('number-question'),
            Location('correct-answer'),
            Location('summary'),
        ]

        answer_1 = Answer(answer_id='answer', value=123)

        answers = AnswerStore()
        answers.add_or_update(answer_1)

        # When
        path_finder = PathFinder(
            schema, answer_store=answers, metadata={}, completed_store=CompletedStore()
        )
        routing_path = path_finder.routing_path(current_section)

        # Then
        self.assertEqual(routing_path, expected_path)

    def test_routing_path_with_complete_introduction(self):
        schema = load_schema_from_params('test', 'introduction')
        current_section = schema.get_section_for_block_id('introduction')
        completed_store = CompletedStore({'locations': [{'block_id': 'introduction'}]})

        expected_routing_path = [
            Location(block_id='introduction'),
            Location(block_id='general-business-information-completed'),
            Location(block_id='confirmation'),
        ]

        path_finder = PathFinder(schema, AnswerStore(), {}, completed_store)
        routing_path = path_finder.routing_path(current_section)

        self.assertEqual(routing_path, expected_routing_path)

    def test_routing_path_full_path(self):
        schema = load_schema_from_params('test', 'summary')
        current_section = schema.get_section_for_block_id('dessert-block')
        expected_path = [
            Location('radio'),
            Location('test-number-block'),
            Location('dessert-block'),
            Location('summary'),
        ]

        answers = AnswerStore()
        completed_store = CompletedStore(
            {
                'locations': [
                    {'block_id': 'radio'},
                    {'block_id': 'test-number-block'},
                    {'block_id': 'dessert-block'},
                ]
            }
        )
        path_finder = PathFinder(
            schema, answer_store=answers, metadata={}, completed_store=completed_store
        )
        routing_path = path_finder.routing_path(current_section)

        self.assertEqual(routing_path, expected_path)

    def test_routing_path_empty_routing_rules(self):
        schema = load_schema_from_params('test', 'checkbox')
        current_section = schema.get_section_for_block_id('mandatory-checkbox')
        expected_path = [
            Location('mandatory-checkbox'),
            Location('non-mandatory-checkbox'),
            Location('summary'),
        ]

        answer_1 = Answer(answer_id='mandatory-checkbox-answer', value='Cheese')
        answer_2 = Answer(answer_id='non-mandatory-checkbox-answer', value='deep pan')

        answers = AnswerStore()
        answers.add_or_update(answer_1)
        answers.add_or_update(answer_2)

        completed_store = CompletedStore(
            {'locations': [{'block_id': 'mandatory-checkbox'}]}
        )

        path_finder = PathFinder(
            schema, answer_store=answers, metadata={}, completed_store=completed_store
        )
        routing_path = path_finder.routing_path(current_section)

        self.assertEqual(routing_path, expected_path)

    def test_routing_path_with_conditional_value_not_in_metadata(self):
        schema = load_schema_from_params('test', 'metadata_routing')
        current_section = schema.get_section_for_block_id('block1')
        expected_path = [
            Location(block_id='block1'),
            Location(block_id='block2'),
            Location(block_id='block3'),
            Location(block_id='summary'),
        ]

        completed_store = CompletedStore({'locations': [{'block_id': 'block1'}]})
        metadata = {}

        path_finder = PathFinder(
            schema, AnswerStore(), metadata=metadata, completed_store=completed_store
        )
        routing_path = path_finder.routing_path(current_section)

        self.assertEqual(routing_path, expected_path)

    def test_routing_path_should_skip_block(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_block')
        current_section = schema.get_section_for_block_id('should-skip')
        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id='do-you-want-to-skip-answer', value='Yes')
        )
        completed_store = CompletedStore(
            {'locations': [{'block_id': 'do-you-want-to-skip'}]}
        )

        # When
        path_finder = PathFinder(
            schema,
            answer_store=answer_store,
            metadata={},
            completed_store=completed_store,
        )
        routing_path = path_finder.routing_path(current_section)

        # Then
        expected_routing_path = [
            Location(block_id='do-you-want-to-skip'),
            Location(block_id='a-non-skipped-block'),
            Location(block_id='summary'),
        ]

        with patch(
            'app.questionnaire.path_finder.evaluate_skip_conditions', return_value=True
        ):
            self.assertEqual(routing_path, expected_routing_path)

    def test_routing_path_should_skip_group(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')

        current_section = schema.get_section_for_block_id('do-you-want-to-skip')

        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id='do-you-want-to-skip-answer', value='Yes')
        )

        completed_store = CompletedStore(
            {'locations': [{'block_id': 'do-you-want-to-skip'}]}
        )

        # When
        path_finder = PathFinder(
            schema,
            answer_store=answer_store,
            metadata={},
            completed_store=completed_store,
        )
        routing_path = path_finder.routing_path(current_section)

        # Then
        expected_routing_path = [
            Location(block_id='do-you-want-to-skip'),
            Location(block_id='last-group-block'),
            Location(block_id='summary'),
        ]

        with patch(
            'app.questionnaire.path_finder.evaluate_skip_conditions', return_value=True
        ):
            self.assertEqual(routing_path, expected_routing_path)

    def test_routing_path_should_not_skip_group(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')

        current_section = schema.get_section_for_block_id('do-you-want-to-skip')

        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id='do-you-want-to-skip-answer', value='No')
        )

        completed_store = CompletedStore(
            {'locations': [{'block_id': 'do-you-want-to-skip'}]}
        )

        # When
        path_finder = PathFinder(
            schema,
            answer_store=answer_store,
            metadata={},
            completed_store=completed_store,
        )
        routing_path = path_finder.routing_path(current_section)

        # Then
        expected_routing_path = [
            Location(block_id='do-you-want-to-skip'),
            Location(block_id='should-skip'),
            Location(block_id='last-group-block'),
            Location(block_id='summary'),
        ]

        with patch(
            'app.questionnaire.path_finder.evaluate_skip_conditions', return_value=False
        ):
            self.assertEqual(routing_path, expected_routing_path)

    def test_get_routing_path_when_first_block_in_group_skipped(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id='do-you-want-to-skip-answer', value='Yes')
        )

        # When
        path_finder = PathFinder(
            schema,
            answer_store=answer_store,
            metadata={},
            completed_store=CompletedStore(),
        )

        # Then
        expected_route = [
            {
                'block_id': 'do-you-want-to-skip-block',
                'group_id': 'do-you-want-to-skip-group',
            },
            {'block_id': 'summary', 'group_id': 'should-skip-group'},
        ]
        current_section = schema.get_section_for_block_id('summary')
        pytest.xfail(
            reason='Known bug when skipping last group due to summary bundled into it'
        )

        self.assertEqual(path_finder.routing_path(current_section), expected_route)

    def test_build_path_with_group_routing(self):
        # Given i have answered the routing question
        schema = load_schema_from_params('test', 'routing_group')
        current_section = schema.get_section_for_block_id('group2-block')

        answer_store = AnswerStore()
        answer_store.add_or_update(
            Answer(answer_id='which-group-answer', value='group2')
        )

        # When i build the path
        path_finder = PathFinder(
            schema,
            answer_store=answer_store,
            metadata={},
            completed_store=CompletedStore(),
        )
        path = path_finder.routing_path(current_section)

        # Then it should route me straight to Group2 and not Group1
        self.assertNotIn(Location('group1-block'), path)
        self.assertIn(Location('group2-block'), path)

    def test_remove_answer_and_block_if_routing_backwards(self):
        schema = load_schema_from_params('test', 'confirmation_question')
        current_section = schema.get_section_for_block_id(
            'confirm-zero-employees-block'
        )
        # All blocks completed
        completed_store = CompletedStore(
            {
                'locations': [
                    {'block_id': 'number-of-employees-total-block'},
                    {'block_id': 'confirm-zero-employees-block'},
                ]
            }
        )

        answer_store = AnswerStore()
        number_of_employees_answer = Answer(
            answer_id='number-of-employees-total', value=0
        )
        confirm_zero_answer = Answer(
            answer_id='confirm-zero-employees-answer', value='No'
        )
        answer_store.add_or_update(number_of_employees_answer)
        answer_store.add_or_update(confirm_zero_answer)

        path_finder = PathFinder(
            schema, answer_store, metadata={}, completed_store=completed_store
        )

        self.assertEqual(len(path_finder.completed_store.locations), 2)
        self.assertEqual(len(path_finder.answer_store), 2)

        routing_path = path_finder.routing_path(current_section)

        expected_path = [
            Location(block_id='number-of-employees-total-block'),
            Location(block_id='confirm-zero-employees-block'),
            Location(block_id='number-of-employees-total-block'),
        ]
        self.assertEqual(routing_path, expected_path)

        self.assertEqual(
            path_finder.completed_store.locations, [completed_store.locations[0]]
        )
        self.assertEqual(len(path_finder.answer_store), 1)
