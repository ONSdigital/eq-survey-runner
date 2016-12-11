from unittest import TestCase

from mock import MagicMock

from app.questionnaire_state.state_answer import StateAnswer
from app.questionnaire_state.state_repeating_answer_question import RepeatingAnswerStateQuestion, extract_answer_instance_id
from app.schema.answer import Answer
from app.schema.widgets.text_widget import TextWidget


class TestRepeatingAnswerStateQuestion(TestCase):

    def test_update_state_initialise_repeating(self):

        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())
        question_state.schema_item.type = 'RepeatingAnswer'
        question_state.schema_item.answers = [Answer('answer_id')]
        question_state.schema_item.answers[0].widget = TextWidget('answer_id')

        answer_state = MagicMock()
        answer_state.id = 'answer_id'
        answer_state.answer_instance = 0

        question_state.answers.append(answer_state)
        question_state.update_state({
            'answer_id': 'answer_value',
            'answer_id_1': 'answer_value_1'
        })
        self.assertEqual(len(question_state.answers), 2)

    def test_update_state_multiple_answers_in_schema(self):

        question = RepeatingAnswerStateQuestion('question_id', MagicMock())
        question.schema_item.type = 'RepeatingAnswer'

        answer1 = Answer('answer_one')
        answer2 = Answer('answer_two')

        answer1.widget = TextWidget('answer_one')
        answer2.widget = TextWidget('answer_two')

        question.schema_item.answers = [answer1, answer2]

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_one_1': 'answer_one_value_1',
            'answer_two': 'answer_two_value',
        })

        self.assertEqual(len(question.children), 3)

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_two': 'answer_two_value',
            'answer_two_3': 'answer_two_value_3',
            'answer_two_2': 'answer_two_value_2',
        })

        self.assertEqual(len(question.children), 5)

    def test_update_state_non_repeating_multiple_answers(self):
        question = RepeatingAnswerStateQuestion('question_id', MagicMock())

        answer1 = MagicMock()
        answer1.schema_item.id = 'answer_one'

        answer2 = MagicMock()
        answer2.schema_item.id = 'answer_two'

        answer3 = MagicMock()
        answer3.schema_item.id = 'answer_three'

        question.answers.append(answer1)
        question.answers.append(answer2)
        question.answers.append(answer3)

        question.update_state({
            'answer_one': 'answer_one_value',
            'answer_two': 'answer_two_value',
            'answer_three': 'answer_three_value',
        })

        self.assertEqual(len(question.children), 3)

    def test_update_state_multiple_repeating_answers(self):

        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())
        question_state.schema_item.type = 'RepeatingAnswer'

        answers = []
        for x in range(3):
            answer = Answer('answer'+str(x))
            answer.widget = TextWidget('answer' + str(x))
            answers.append(answer)
        question_state.schema_item.answers = answers

        answer1 = StateAnswer('answer0', MagicMock())
        answer2 = StateAnswer('answer1', MagicMock())
        answer3 = StateAnswer('answer2', MagicMock())

        question_state.answers = [answer1, answer2, answer3]

        question_state.update_state({
            'answer0': 'answer_one_value',
            'answer0_1': 'answer_one_value_1',
            'answer1': 'answer_two_value',
            'answer1_1': 'answer_two_value_1',
            'answer1_2': 'answer_two_value_2',
            'answer2': 'answer_three_value',
        })

        self.assertEqual(len(question_state.answers), 6)

    def test_extract_answer_instance_id(self):
        answer_id, answer_index = extract_answer_instance_id('')
        self.assertEqual(answer_id, '')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = extract_answer_instance_id('abcdefg')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = extract_answer_instance_id('abcdefg_')
        self.assertEqual(answer_id, 'abcdefg_')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = extract_answer_instance_id('abcdefg_0')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = extract_answer_instance_id('abcdefg_1')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 1)

        answer_id, answer_index = extract_answer_instance_id('abcdefg_1_2')
        self.assertEqual(answer_id, 'abcdefg_1')
        self.assertEqual(answer_index, 2)

        answer_id, answer_index = extract_answer_instance_id('_1')
        self.assertEqual(answer_id, '_1')
        self.assertEqual(answer_index, 0)

        answer_id, answer_index = extract_answer_instance_id('1234_1')
        self.assertEqual(answer_id, '1234')
        self.assertEqual(answer_index, 1)

        answer_id, answer_index = extract_answer_instance_id('abcdefg_12345')
        self.assertEqual(answer_id, 'abcdefg')
        self.assertEqual(answer_index, 12345)

    def test_answers_grouped_by_instance_id_no_answers(self):
        # Given
        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())

        # When
        answers = question_state.answers_grouped_by_instance()

        # Then
        self.assertEqual(len(answers), 0)

    def test_answers_grouped_by_instance_id_one_answer_no_instances(self):
        # Given
        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())

        schema_answer = Answer('answer')
        schema_answer.widget = TextWidget('answer')
        question_state.schema_item.answers = [schema_answer]

        question_state.answers = []

        # When
        result = question_state.answers_grouped_by_instance()

        # Then
        self.assertEqual(len(result), 0)

    def test_answers_grouped_by_instance_id_one_answer_one_instance(self):
        # Given
        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())

        schema_answer = Answer('answer')
        schema_answer.widget = TextWidget('answer')
        question_state.schema_item.answers = [schema_answer]

        state_answer = MagicMock()
        state_answer.id = 'answer'
        state_answer.answer_instance = 0

        question_state.answers = [state_answer]

        # When
        result = question_state.answers_grouped_by_instance()

        # Then
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], state_answer)

    def test_answers_grouped_by_instance_id_one_answer_many_instances(self):
        # Given
        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())

        schema_answer = Answer('answer')
        schema_answer.widget = TextWidget('answer')
        question_state.schema_item.answers = [schema_answer]

        state_answer = MagicMock()
        state_answer.id = 'answer'
        state_answer.answer_instance = 0

        state_answer1 = MagicMock()
        state_answer1.id = 'answer'
        state_answer1.answer_instance = 1

        question_state.answers = [state_answer, state_answer1]

        # When
        result = question_state.answers_grouped_by_instance()

        # Then
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0], state_answer)
        self.assertEqual(len(result[1]), 1)
        self.assertEqual(result[1][0], state_answer1)

    def test_answers_grouped_by_instance_id_many_answers_one_instance(self):
        # Given
        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())

        first_name_schema = Answer('first-name')
        first_name_schema.widget = TextWidget('first-name')

        middle_name_schema = Answer('middle-names')
        middle_name_schema.widget = TextWidget('middle-names')

        last_name_schema = Answer('last-name')
        last_name_schema.widget = TextWidget('last-name')

        question_state.schema_item.answers = [
            first_name_schema,
            middle_name_schema,
            last_name_schema
        ]

        first_name = MagicMock()
        first_name.id = 'first-name'
        first_name.answer_instance = 0

        middle_name = MagicMock()
        middle_name.id = 'middle-names'
        middle_name.answer_instance = 0

        last_name = MagicMock()
        last_name.id = 'last-name'
        last_name.answer_instance = 0

        question_state.answers = [first_name, middle_name, last_name]

        # When
        result = question_state.answers_grouped_by_instance()

        # Then
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(result[0][0], first_name)
        self.assertEqual(result[0][1], middle_name)
        self.assertEqual(result[0][2], last_name)

    def test_answers_grouped_by_instance_id_many_answers_many_instance(self):
        # Given
        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())

        first_name_schema = Answer('first-name')
        first_name_schema.widget = TextWidget('first-name')

        middle_name_schema = Answer('middle-names')
        middle_name_schema.widget = TextWidget('middle-names')

        last_name_schema = Answer('last-name')
        last_name_schema.widget = TextWidget('last-name')

        question_state.schema_item.answers = [
            first_name_schema,
            middle_name_schema,
            last_name_schema
        ]

        first_name = MagicMock()
        first_name.id = 'first-name'
        first_name.answer_instance = 0

        middle_name = MagicMock()
        middle_name.id = 'middle-names'
        middle_name.answer_instance = 0

        last_name = MagicMock()
        last_name.id = 'last-name'
        last_name.answer_instance = 0

        first_name1 = MagicMock()
        first_name1.id = 'first-name'
        first_name1.answer_instance = 1

        middle_name1 = MagicMock()
        middle_name1.id = 'middle-names'
        middle_name1.answer_instance = 1

        last_name1 = MagicMock()
        last_name1.id = 'last-name'
        last_name1.answer_instance = 1

        first_name2 = MagicMock()
        first_name2.id = 'first-name'
        first_name2.answer_instance = 2

        middle_name2 = MagicMock()
        middle_name2.id = 'middle-names'
        middle_name2.answer_instance = 2

        last_name2 = MagicMock()
        last_name2.id = 'last-name'
        last_name2.answer_instance = 2

        question_state.answers = [
            first_name, middle_name, last_name,
            first_name1, middle_name1, last_name1,
            first_name2, middle_name2, last_name2,
        ]

        # When
        result = question_state.answers_grouped_by_instance()

        # Then
        self.assertEqual(len(result), 3)

        # Instance 0
        self.assertEqual(len(result[0]), 3)
        self.assertEqual(result[0][0], first_name)
        self.assertEqual(result[0][1], middle_name)
        self.assertEqual(result[0][2], last_name)

        # Instance 1
        self.assertEqual(len(result[1]), 3)
        self.assertEqual(result[1][0], first_name1)
        self.assertEqual(result[1][1], middle_name1)
        self.assertEqual(result[1][2], last_name1)

        # Instance 2
        self.assertEqual(len(result[2]), 3)
        self.assertEqual(result[2][0], first_name2)
        self.assertEqual(result[2][1], middle_name2)
        self.assertEqual(result[2][2], last_name2)

    def test_answers_grouped_by_instance_id_odd_number_of_instances(self):
        # Given
        question_state = RepeatingAnswerStateQuestion('question_id', MagicMock())

        first_name_schema = Answer('first-name')
        first_name_schema.widget = TextWidget('first-name')

        last_name_schema = Answer('last-name')
        last_name_schema.widget = TextWidget('last-name')

        question_state.schema_item.answers = [
            first_name_schema,
            last_name_schema
        ]

        first_name = MagicMock()
        first_name.id = 'first-name'
        first_name.answer_instance = 0

        last_name = MagicMock()
        last_name.id = 'last-name'
        last_name.answer_instance = 0

        first_name1 = MagicMock()
        first_name1.id = 'first-name'
        first_name1.answer_instance = 1

        question_state.answers = [
            first_name, last_name,
            first_name1
        ]

        # When
        result = question_state.answers_grouped_by_instance()

        # Then
        self.assertEqual(len(result), 2)

        # Instance 0
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(result[0][0], first_name)
        self.assertEqual(result[0][1], last_name)

        # Instance 1
        self.assertEqual(len(result[1]), 1)
        self.assertEqual(result[1][0], first_name1)
