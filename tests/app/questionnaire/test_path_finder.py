import pytest

from app.data_model.answer_store import Answer, AnswerStore
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.utilities.schema import load_schema_from_params
from tests.app.app_context_test_case import AppContextTestCase


class TestPathFinder(AppContextTestCase):  # pylint: disable=too-many-public-methods, too-many-lines

    def test_next_block(self):
        schema = load_schema_from_params('test', '0102')

        current_location = Location(
            block_id='total-retail-turnover',
            group_id='rsi',
            group_instance=0
        )

        next_location = Location(
            block_id='internet-sales',
            group_id='rsi',
            group_instance=0
        )

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        self.assertEqual(path_finder.get_next_location(current_location=current_location), next_location)

    def test_previous_block(self):
        schema = load_schema_from_params('test', '0102')

        current_location = Location(
            block_id='internet-sales',
            group_id='rsi',
            group_instance=0
        )

        previous_location = Location(
            block_id='total-retail-turnover',
            group_id='rsi',
            group_instance=0
        )

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        self.assertEqual(path_finder.get_previous_location(current_location=current_location), previous_location)

    def test_introduction_in_path_when_in_schema(self):
        schema = load_schema_from_params('test', '0102')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])

        blocks = [b.block_id for b in path_finder.get_full_routing_path()]

        self.assertIn('introduction', blocks)

    def test_introduction_not_in_path_when_not_in_schema(self):
        schema = load_schema_from_params('census', 'individual')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])

        blocks = [b.block_id for b in path_finder.get_full_routing_path()]

        self.assertNotIn('introduction', blocks)

    def test_next_with_conditional_path(self):
        schema = load_schema_from_params('0', 'star_wars')

        expected_path = [
            Location('star-wars', 0, 'choose-your-side-block'),
            Location('star-wars', 0, 'light-side-pick-character-ship'),
            Location('star-wars', 0, 'star-wars-trivia'),
            Location('star-wars', 0, 'star-wars-trivia-part-2'),
            Location('star-wars', 0, 'star-wars-trivia-part-3'),
        ]

        answer_1 = Answer(
            answer_id='choose-your-side-answer',
            value='Light Side'
        )

        answer_2 = Answer(
            answer_id='light-side-pick-ship-answer',
            value='No'
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        current_location = expected_path[1]
        expected_next_location = expected_path[2]

        completed_blocks = [
            expected_path[0],
            expected_path[1]
        ]

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=completed_blocks)
        actual_next_block = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(actual_next_block, expected_next_location)

        current_location = expected_path[2]
        expected_next_location = expected_path[3]

        path_finder.completed_blocks = [
            expected_path[0],
            expected_path[1],
            expected_path[2]
        ]

        actual_next_block = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(actual_next_block, expected_next_location)

    def test_routing_basic_path(self):
        schema = load_schema_from_params('test', '0112')

        expected_path = [
            Location('rsi', 0, 'introduction'),
            Location('rsi', 0, 'reporting-period'),
            Location('rsi', 0, 'total-retail-turnover'),
            Location('rsi', 0, 'internet-sales'),
            Location('rsi', 0, 'changes-in-retail-turnover'),
            Location('rsi', 0, 'number-of-employees'),
            Location('rsi', 0, 'changes-in-employees'),
            Location('rsi', 0, 'summary')
        ]

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        routing_path = path_finder.get_full_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_routing_basic_and_conditional_path(self):
        schema = load_schema_from_params('0', 'star_wars')

        expected_path = [
            Location('star-wars', 0, 'introduction'),
            Location('star-wars', 0, 'choose-your-side-block'),
            Location('star-wars', 0, 'dark-side-pick-character-ship'),
            Location('star-wars', 0, 'light-side-ship-type'),
            Location('star-wars', 0, 'star-wars-trivia'),
            Location('star-wars', 0, 'star-wars-trivia-part-2'),
            Location('star-wars', 0, 'star-wars-trivia-part-3'),
            Location('star-wars', 0, 'summary'),
        ]

        answer_1 = Answer(
            answer_id='choose-your-side-answer',
            value='Dark Side'
        )
        answer_2 = Answer(
            answer_id='dark-side-pick-ship-answer',
            value='Can I be a pain and have a goodies ship',
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])
        routing_path = path_finder.get_full_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_get_next_location_introduction(self):
        schema = load_schema_from_params('0', 'star_wars')

        introduction = Location('star-wars', 0, 'introduction')

        path_finder = PathFinder(schema, AnswerStore(), {}, [introduction])

        next_location = path_finder.get_next_location(current_location=introduction)

        self.assertEqual('choose-your-side-block', next_location.block_id)

    def test_get_next_location_summary(self):
        schema = load_schema_from_params('0', 'star_wars')

        answer_1 = Answer(
            answer_id='choose-your-side-answer',
            value='Light Side'
        )
        answer_2 = Answer(
            answer_id='light-side-pick-ship-answer',
            value='No',
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        current_location = Location('star-wars', 0, 'star-wars-trivia-part-2')

        next_location = path_finder.get_next_location(current_location=current_location)

        expected_next_location = Location('star-wars', 0, 'star-wars-trivia-part-3')

        self.assertEqual(expected_next_location, next_location)

        current_location = expected_next_location

        next_location = path_finder.get_next_location(current_location=current_location)

        expected_next_location = Location('star-wars', 0, 'summary')

        self.assertEqual(expected_next_location, next_location)

    def test_get_previous_location_introduction(self):
        schema = load_schema_from_params('0', 'star_wars')

        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])

        first_location = Location('star-wars', 0, 'choose-your-side-block')

        previous_location = path_finder.get_previous_location(current_location=first_location)

        self.assertEqual('introduction', previous_location.block_id)

    def test_previous_with_conditional_path(self):
        schema = load_schema_from_params('0', 'star_wars')

        expected_path = [
            Location('star-wars', 0, 'choose-your-side-block'),
            Location('star-wars', 0, 'dark-side-pick-character-ship'),
            Location('star-wars', 0, 'light-side-ship-type'),
            Location('star-wars', 0, 'star-wars-trivia'),
            Location('star-wars', 0, 'star-wars-trivia-part-2'),
            Location('star-wars', 0, 'star-wars-trivia-part-3'),
        ]

        answer_1 = Answer(
            answer_id='choose-your-side-answer',
            value='Dark Side'
        )
        answer_2 = Answer(
            answer_id='dark-side-pick-ship-answer',
            value='Can I be a pain and have a goodies ship',
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        current_location = expected_path[3]
        expected_previous_location = expected_path[2]

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])
        actual_previous_block = path_finder.get_previous_location(current_location=current_location)

        self.assertEqual(actual_previous_block, expected_previous_location)

        current_location = expected_path[2]
        expected_previous_location = expected_path[1]

        actual_previous_block = path_finder.get_previous_location(current_location=current_location)

        self.assertEqual(actual_previous_block, expected_previous_location)

    def test_previous_with_conditional_path_alternative(self):
        schema = load_schema_from_params('0', 'star_wars')

        expected_path = [
            Location('star-wars', 0, 'choose-your-side-block'),
            Location('star-wars', 0, 'light-side-pick-character-ship'),
            Location('star-wars', 0, 'star-wars-trivia'),
            Location('star-wars', 0, 'star-wars-trivia-part-2'),
            Location('star-wars', 0, 'star-wars-trivia-part-3'),
        ]

        current_location = expected_path[2]
        expected_previous_location = expected_path[1]

        answer_1 = Answer(
            answer_id='choose-your-side-answer',
            value='Light Side'
        )
        answer_2 = Answer(
            answer_id='light-side-pick-ship-answer',
            value='No',
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(path_finder.get_previous_location(current_location=current_location),
                         expected_previous_location)

    def test_next_location_goto_summary(self):
        schema = load_schema_from_params('0', 'star_wars')

        expected_path = [
            Location('star-wars', 0, 'introduction'),
            Location('star-wars', 0, 'choose-your-side-block'),
            Location('star-wars', 0, 'summary'),
        ]

        answer = Answer(
            group_instance=0,
            answer_id='choose-your-side-answer',
            value='I prefer Star Trek',
        )
        answers = AnswerStore()
        answers.add(answer)
        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        current_location = expected_path[1]
        expected_next_location = expected_path[2]

        next_location = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(next_location, expected_next_location)

    def test_next_location_empty_routing_rules(self):
        schema = load_schema_from_params('test', 'checkbox')

        expected_path = [
            Location('checkboxes', 0, 'introduction'),
            Location('checkboxes', 0, 'mandatory-checkbox'),
            Location('checkboxes', 0, 'non-mandatory-checkbox'),
            Location('checkboxes', 0, 'summary')
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
        answers.add(answer_1)
        answers.add(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        current_location = expected_path[1]
        expected_next_location = expected_path[2]

        next_location = path_finder.get_next_location(current_location=current_location)

        self.assertEqual(next_location, expected_next_location)

    def test_interstitial_post_blocks(self):
        schema = load_schema_from_params('0', 'star_wars')

        answer = Answer(
            answer_id='choose-your-side-answer',
            value='Light Side'
        )

        answers = AnswerStore()
        answers.add(answer)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertFalse(Location('star-wars', 0, 'summary') in path_finder.get_full_routing_path())

    def test_repeating_groups(self):
        schema = load_schema_from_params('test', 'repeating_household')

        # Default is to count answers, so switch to using value
        schema.json['sections'][-2]['groups'][0]['routing_rules'][0]['repeat']['type'] = 'answer_value'

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2'),
            Location('summary-group', 0, 'summary'),
        ]

        answer = Answer(
            group_instance=0,
            answer_id='first-name',
            value='2'
        )
        answers = AnswerStore()
        answers.add(answer)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(expected_path, path_finder.get_full_routing_path())

    def test_should_not_show_block_for_zero_repeats(self):
        schema = load_schema_from_params('test', 'repeating_household')

        # Default is to count answers, so switch to using value
        schema.json['sections'][-2]['groups'][0]['routing_rules'][0]['repeat']['type'] = 'answer_value'

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('summary-group', 0, 'summary')
        ]

        answer = Answer(
            group_instance=0,
            answer_id='first-name',
            value='0'
        )
        answers = AnswerStore()
        answers.add(answer)
        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])
        self.assertEqual(expected_path, path_finder.get_full_routing_path())

    def test_repeating_groups_no_of_answers(self):
        schema = load_schema_from_params('test', 'repeating_household')

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2'),
            Location('repeating-group', 2, 'repeating-block-1'),
            Location('repeating-group', 2, 'repeating-block-2'),
            Location('summary-group', 0, 'summary'),
        ]

        answer = Answer(
            group_instance=0,
            answer_instance=0,
            answer_id='first-name',
            value='Joe Bloggs'
        )

        answer_2 = Answer(
            group_instance=0,
            answer_instance=1,
            answer_id='first-name',
            value='Sophie Bloggs'
        )

        answer_3 = Answer(
            group_instance=0,
            answer_instance=2,
            answer_id='first-name',
            value='Gregg Bloggs'
        )

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(expected_path, path_finder.get_full_routing_path())

    def test_repeating_groups_no_of_answers_minus_one(self):
        schema = load_schema_from_params('test', 'repeating_household')

        # Default is to count answers, so switch to using value
        schema.json['sections'][-2]['groups'][0]['routing_rules'][0]['repeat']['type'] = 'answer_count_minus_one'

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('summary-group', 0, 'summary'),
        ]

        answer = Answer(
            group_instance=0,
            answer_instance=0,
            answer_id='first-name',
            value='Joe Bloggs'
        )

        answer_2 = Answer(
            group_instance=0,
            answer_instance=1,
            answer_id='first-name',
            value='Sophie Bloggs'
        )

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(expected_path, path_finder.get_full_routing_path())

    def test_repeating_groups_previous_location_first_instance(self):
        schema = load_schema_from_params('census', 'household')

        expected_path = [
            Location('who-lives-here', 0, 'overnight-visitors'),
            Location('who-lives-here-relationship', 0, 'household-relationships'),
        ]
        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        self.assertEqual(path_finder.get_previous_location(current_location=expected_path[1]), expected_path[0])

    def test_repeating_groups_previous_location_second_instance(self):
        schema = load_schema_from_params('census', 'household')

        expected_path = [
            Location('who-lives-here-relationship', 0, 'household-relationships'),
            Location('who-lives-here-relationship', 1, 'household-relationships'),
        ]
        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        self.assertEqual(path_finder.get_previous_location(current_location=expected_path[1]), expected_path[0])

    def test_repeating_groups_previous_location(self):
        schema = load_schema_from_params('test', 'repeating_household')

        expected_path = [
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2'),
        ]

        answer = Answer(
            answer_instance=0,
            answer_id='first-name',
            value='Joe Bloggs'
        )

        answer_2 = Answer(
            answer_instance=1,
            answer_id='first-name',
            value='Sophie Bloggs'
        )

        current_location = expected_path[4]

        expected_previous_location = expected_path[3]

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(expected_previous_location,
                         path_finder.get_previous_location(current_location=current_location))

    def test_repeating_groups_next_location(self):
        schema = load_schema_from_params('test', 'repeating_household')

        expected_path = [
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('repeating-group', 0, 'repeating-block-1'),
            Location('repeating-group', 0, 'repeating-block-2'),
            Location('repeating-group', 1, 'repeating-block-1'),
            Location('repeating-group', 1, 'repeating-block-2')
        ]

        answer = Answer(
            answer_instance=0,
            answer_id='first-name',
            value='Joe Bloggs'
        )

        answer_2 = Answer(
            answer_instance=1,
            answer_id='first-name',
            value='Sophie Bloggs'
        )

        current_location = expected_path[-1]

        answers = AnswerStore()
        answers.add(answer)
        answers.add(answer_2)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        summary_location = Location('summary-group', 0, 'summary')

        self.assertEqual(summary_location, path_finder.get_next_location(current_location=current_location))

    def test_repeating_groups_conditional_location_path(self):
        schema = load_schema_from_params('test', 'repeating_and_conditional_routing')

        expected_path = [
            Location('repeat-value-group', 0, 'introduction'),
            Location('repeat-value-group', 0, 'no-of-repeats'),
            Location('repeated-group', 0, 'repeated-block'),
            Location('repeated-group', 0, 'age-block'),
            Location('repeated-group', 0, 'shoe-size-block'),
            Location('repeated-group', 1, 'repeated-block'),
            Location('repeated-group', 1, 'shoe-size-block'),
            Location('summary-group', 0, 'summary')
        ]

        answer_1 = Answer(
            answer_id='no-of-repeats-answer',
            value='2'
        )

        answer_2 = Answer(
            group_instance=0,
            answer_id='conditional-answer',
            value='Age and Shoe Size'
        )

        answer_3 = Answer(
            group_instance=1,
            answer_id='conditional-answer',
            value='Shoe Size Only'
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(expected_path, path_finder.get_full_routing_path())

    def test_excessive_repeating_groups_conditional_location_path(self):
        schema = load_schema_from_params('test', 'repeating_and_conditional_routing')

        answers = AnswerStore()

        answers.add(Answer(
            answer_id='no-of-repeats-answer',
            value='10000'
        ))

        for i in range(50):
            answers.add(Answer(
                group_instance=i,
                answer_id='conditional-answer',
                value='Shoe Size Only'
            ))

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual('summary', path_finder.get_full_routing_path().pop().block_id)

    def test_next_with_conditional_path_based_on_metadata(self):
        schema = load_schema_from_params('test', 'metadata_routing')

        expected_path = [
            Location('group1', 0, 'block1'),
            Location('group1', 0, 'block3'),
        ]

        current_location = expected_path[0]

        expected_next_location = expected_path[1]

        metadata = {
            'variant_flags': {
                'flag_1': True
            }
        }

        path_finder = PathFinder(schema, AnswerStore(), metadata=metadata, completed_blocks=[])

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_next_with_conditional_path_when_value_not_in_metadata(self):
        schema = load_schema_from_params('test', 'metadata_routing')

        expected_path = [
            Location('group1', 0, 'block1'),
            Location('group1', 0, 'block2'),
        ]

        current_location = expected_path[0]

        expected_next_location = expected_path[1]

        metadata = {
            'variant_flags': {
            }
        }

        path_finder = PathFinder(schema, AnswerStore(), metadata=metadata, completed_blocks=[])

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_routing_backwards_loops_to_previous_block(self):
        schema = load_schema_from_params('test', 'household_question')

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('multiple-questions-group', 0, 'household-summary'),
            Location('multiple-questions-group', 0, 'household-composition'),
        ]

        current_location = expected_path[2]

        expected_next_location = expected_path[3]

        answers = AnswerStore()

        answer_1 = Answer(
            group_instance=0,
            answer_id='household-full-name',
            answer_instance=0,
            value='Joe Bloggs'
        )

        answer_2 = Answer(
            group_instance=0,
            answer_id='household-full-name',
            answer_instance=1,
            value='Sophie Bloggs'
        )

        answer_3 = Answer(
            group_instance=0,
            answer_id='household-composition-add-another',
            answer_instance=0,
            value='No'
        )

        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_routing_backwards_continues_to_summary_when_complete(self):
        schema = load_schema_from_params('test', 'household_question')

        expected_path = [
            Location('multiple-questions-group', 0, 'introduction'),
            Location('multiple-questions-group', 0, 'household-composition'),
            Location('multiple-questions-group', 0, 'household-summary'),
            Location('multiple-questions-group', 0, 'summary'),
        ]

        current_location = expected_path[2]

        expected_next_location = expected_path[3]

        answers = AnswerStore()

        answer_1 = Answer(
            group_instance=0,
            answer_id='household-full-name',
            answer_instance=0,
            value='Joe Bloggs'
        )

        answer_2 = Answer(
            group_instance=0,
            answer_id='household-full-name',
            answer_instance=1,
            value='Sophie Bloggs'
        )

        answer_3 = Answer(
            group_instance=0,
            answer_id='household-composition-add-another',
            answer_instance=0,
            value='Yes'
        )

        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        path_finder = PathFinder(schema, answer_store=answers, metadata={}, completed_blocks=[])

        self.assertEqual(expected_next_location, path_finder.get_next_location(current_location=current_location))

    def test_get_next_location_should_skip_block(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_block')
        current_location = Location('do-you-want-to-skip-group', 0, 'do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='do-you-want-to-skip-answer',
                                value='Yes'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_next_location = Location('summary-group', 0, 'summary')

        self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_next_location)

    def test_get_next_location_should_skip_group(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        current_location = Location('do-you-want-to-skip-group', 0, 'do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='do-you-want-to-skip-answer',
                                value='Yes'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_next_location = Location('last-group', 0, 'last-group-block')

        self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_next_location)

    def test_get_next_location_should_not_skip_group(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        current_location = Location('do-you-want-to-skip-group', 0, 'do-you-want-to-skip')
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='do-you-want-to-skip-answer',
                                value='No'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_location = Location('should-skip-group', 0, 'should-skip')

        self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_location)

    def test_get_next_location_should_not_skip_when_no_answers(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        current_location = Location('do-you-want-to-skip-group', 0, 'do-you-want-to-skip')
        answer_store = AnswerStore()

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_location = Location('should-skip-group', 0, 'should-skip')

        self.assertEqual(path_finder.get_next_location(current_location=current_location), expected_location)

    def test_get_routing_path_when_first_block_in_group_skipped(self):
        # Given
        schema = load_schema_from_params('test', 'skip_condition_group')
        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='do-you-want-to-skip-answer',
                                value='Yes'))

        # When
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        # Then
        expected_route = [
            {
                'block_id': 'do-you-want-to-skip-block',
                'group_id': 'do-you-want-to-skip-group',
                'group_instance': 0
            },
            {
                'block_id': 'summary',
                'group_id': 'should-skip-group',
                'group_instance': 0
            }
        ]

        pytest.xfail(reason='Known bug when skipping last group due to summary bundled into it')
        self.assertEqual(path_finder.get_routing_path('should-skip-group'), expected_route)

    def test_given_no_completed_blocks_when_get_latest_location_then_go_to_first_block(self):
        # Given no completed blocks
        schema = load_schema_from_params('test', 'repeating_household')
        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        completed_block = []

        # When go latest location
        latest_location = path_finder.get_latest_location(completed_block)

        # Then go to the first block
        self.assertEqual(Location('multiple-questions-group', 0, 'introduction'), latest_location)

    def test_given_some_completed_blocks_when_get_latest_location_then_go_to_next_uncompleted_block(self):
        # Given no completed blocks
        schema = load_schema_from_params('test', 'repeating_household')
        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        completed_block = [Location('multiple-questions-group', 0, 'introduction')]

        # When go latest location
        latest_location = path_finder.get_latest_location(completed_block)

        # Then go to the first block
        self.assertEqual(Location('multiple-questions-group', 0, 'household-composition'), latest_location)

    def test_given_completed_all_the_blocks_when_get_latest_location_then_go_to_last_block(self):
        # Given no completed blocks
        schema = load_schema_from_params('test', 'textarea')
        path_finder = PathFinder(schema, AnswerStore(), metadata={}, completed_blocks=[])
        completed_block = [Location('textarea-group', 0, 'textarea-block'),
                           Location('textarea-group', 0, 'textarea-summary')]

        # When go latest location
        latest_location = path_finder.get_latest_location(completed_block)

        # Then go to the first block
        self.assertEqual(Location('textarea-group', 0, 'textarea-summary'), latest_location)

    def test_build_path_with_group_routing(self):
        # Given i have answered the routing question
        schema = load_schema_from_params('test', 'routing_group')

        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='which-group-answer',
                                value='group2'))

        # When i build the path
        path_finder = PathFinder(schema, answer_store=answer_store, metadata={}, completed_blocks=[])

        path = path_finder.build_path()

        # Then it should route me straight to Group2 and not Group1
        self.assertNotIn(Location('group1', 0, 'group1-block'), path)
        self.assertIn(Location('group2', 0, 'group2-block'), path)

    def test_return_to_summary_if_complete(self):
        schema = load_schema_from_params('test', 'summary')

        # All blocks completed
        completed_blocks = [
            Location('summary-group', 0, 'radio'),
            Location('summary-group', 0, 'test-number-block'),
            Location('dessert-group', 0, 'dessert-block')
        ]

        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='radio-answer', value='Bacon'))
        answer_store.add(Answer(answer_id='test-currency', value='123'))
        answer_store.add(Answer(answer_id='dessert', value='Cake'))

        summary_location = Location('dessert-group', 0, 'summary')

        path_finder = PathFinder(schema, answer_store, metadata={}, completed_blocks=completed_blocks)

        self.assertEqual(path_finder.get_next_location(current_location=completed_blocks[0]), summary_location)

    def test_return_to_section_summary_if_section_complete(self):
        schema = load_schema_from_params('test', 'section_summary')

        # All blocks completed
        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('address-length', 0, 'address-duration')
        ]

        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='insurance-type-answer', value='Contents'))
        answer_store.add(Answer(answer_id='insurance-address-answer', value='123 Test Road'))
        answer_store.add(Answer(answer_id='address-duration-answer', value='No'))

        summary_location = Location('address-length', 0, 'property-details-summary')

        path_finder = PathFinder(schema, answer_store, metadata={}, completed_blocks=completed_blocks)

        self.assertEqual(path_finder.get_next_location(current_location=completed_blocks[0]), summary_location)

    def test_go_to_next_section_after_section_summary(self):
        schema = load_schema_from_params('test', 'section_summary')

        # All blocks completed
        completed_blocks = [
            Location('property-details', 0, 'insurance-type'),
            Location('property-details', 0, 'insurance-address'),
            Location('address-length', 0, 'address-duration'),
            Location('address-length', 0, 'property-details-summary')
        ]

        answer_store = AnswerStore()
        answer_store.add(Answer(answer_id='insurance-type-answer', value='Both'))
        answer_store.add(Answer(answer_id='insurance-address-answer', value='123 Test Road'))
        answer_store.add(Answer(answer_id='address-duration-answer', value='No'))

        second_section_location = Location('house-details', 0, 'house-type')

        path_finder = PathFinder(schema, answer_store, metadata={}, completed_blocks=completed_blocks)

        self.assertEqual(path_finder.get_next_location(current_location=completed_blocks[3]), second_section_location)
