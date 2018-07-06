from mock import MagicMock
from mock import patch
from app.data_model.answer_store import Answer, AnswerStore
from app.templating.summary.block import Block
from tests.app.app_context_test_case import AppContextTestCase


def build_block_schema(question_schema):
    block_schema = {
        'id': 'block_id',
        'title': 'A section title',
        'number': '1',
        'questions': question_schema
    }
    return block_schema


def build_question_schema(_id, answer_schemas):
    return {'id': _id, 'answers': answer_schemas, 'skipped': False, 'title': 'title', 'type': 'GENERAL'}


class TestSection(AppContextTestCase):

    def test_create_block(self):
        # Given

        answer_schema = MagicMock()
        question_schema = build_question_schema('question_id', [answer_schema])
        block_schema = build_block_schema([question_schema])
        answer_store = MagicMock()
        metadata = MagicMock()

        # When
        block = Block(block_schema, 'group_id', answer_store, metadata)

        # Then
        self.assertEqual(block.id, 'block_id')
        self.assertEqual(block.title, 'A section title')
        self.assertEqual(block.number, '1')
        self.assertEqual(len(block.questions), 1)

    def test_create_section_with_multiple_questions(self):
        # Given
        first_answer_schema = MagicMock()
        second_answer_schema = MagicMock()
        first_question_schema = build_question_schema('question_1', [first_answer_schema])
        second_question_schema = build_question_schema('question_2', [second_answer_schema])
        block_schema = build_block_schema([first_question_schema, second_question_schema])
        answer_store = MagicMock()
        metadata = MagicMock()

        # When
        block = Block(block_schema, 'group_id', answer_store, metadata)

        # Then
        self.assertEqual(len(block.questions), 2)

    def test_question_should_be_skipped(self):
        # Given
        answer = Answer(
            answer_id='answer_1',
            value='skip me',
        )
        answer_store = AnswerStore()
        answer_store.add(answer)
        metadata = MagicMock()
        answer_schema = {'id': 'answer_1', 'title': '', 'type': '', 'label': ''}
        skip_conditions = [{'when': [{'id': 'answer_1', 'condition': 'equals', 'value': 'skip me'}]}]
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema],
                           'skip_conditions': skip_conditions}

        with patch('app.questionnaire.rules._answer_is_in_repeating_group', return_value=False):
            second_question_schema = build_question_schema('question_2', [MagicMock()])
            block_schema = build_block_schema([question_schema, second_question_schema])

            # When
            block = Block(block_schema, 'group_id', answer_store, metadata)

            # Then
            self.assertTrue(len(block.questions) == 1)

    def test_question_with_no_answers_should_not_be_skipped(self):
        # Given
        answer_store = AnswerStore()
        metadata = MagicMock()
        answer_schema = {'id': 'answer_1', 'title': '', 'type': '', 'label': ''}
        skip_conditions = [{'when': [{'id': 'answer_1', 'condition': 'equals', 'value': 'skip me'}]}]
        question_schema = {'id': 'question_id', 'title': 'question_title', 'type': 'GENERAL', 'answers': [answer_schema],
                           'skip_conditions': skip_conditions}
        second_question_schema = build_question_schema('question_2', [MagicMock()])

        with patch('app.questionnaire.rules._answer_is_in_repeating_group', return_value=False):
            block_schema = build_block_schema([question_schema, second_question_schema])

            # When
            block = Block(block_schema, 'group_id', answer_store, metadata)

            # Then
            self.assertTrue(len(block.questions) == 2)
