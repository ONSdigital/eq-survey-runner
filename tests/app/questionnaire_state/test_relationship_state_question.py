from unittest import TestCase

from mock import patch, Mock

from app.questionnaire_state.relationship_state_question import RelationshipStateQuestion
from app.schema.answer import Answer
from app.schema.question import Question
from app.schema.widgets.text_widget import TextWidget


def create_answer(group_instance=0):
    answer = Answer('whos-related')
    answer.widget = TextWidget('whos-related')
    answer_state = answer.construct_state()
    answer_state.group_instance = group_instance
    return answer_state


class TestRelationshipStateQuestion(TestCase):

    household_answers = [
        {
            "answer_id": "first-name",
            "answer_instance": 0,
            "value": "John"
        },
        {
            "answer_id": "first-name",
            "answer_instance": 1,
            "value": "Jane"
        },
        {
            "answer_id": "first-name",
            "answer_instance": 2,
            "value": "Joe"
        }
    ]

    last_names = [
        {
            "answer_id": "last-name",
            "answer_instance": 0,
            "value": "Doe"
        },
        {
            "answer_id": "last-name",
            "answer_instance": 1,
            "value": "Doe"
        },
        {
            "answer_id": "last-name",
            "answer_instance": 2,
            "value": "Bloggs"
        }
    ]

    def test_should_create_relationship_answers_other_household_members(self):
        # Given
        answer_state = create_answer()
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock(return_value=self.household_answers)
            # When
            relationship_state_question.update_state({})

        # Then
        self.assertEqual(len(relationship_state_question.answers), 2)

    def test_relationship_questions_should_reduce_after_each_relationship_answer(self):
        # Given
        answer_state = create_answer(group_instance=1)
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock(return_value=self.household_answers)
            # When
            relationship_state_question.update_state({})

        # Then
        self.assertEqual(len(relationship_state_question.children), 1)

    def test_should_not_have_answer_for_last_person(self):
        # Given
        answer_state = create_answer(group_instance=2)
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock(return_value=self.household_answers)
            # When
            relationship_state_question.update_state({})

        # Then
        self.assertEqual(len(relationship_state_question.children), 0)

    def test_should_set_all_relationship_answers(self):
        # Given
        answer_state = create_answer()
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock(return_value=self.household_answers)
            # When
            relationship_state_question.update_state({'whos-related': 'Brother',
                                                      'whos-related_1': 'Sister'})

        # Then
        self.assertEqual(len(relationship_state_question.children), 2)
        self.assertEqual(relationship_state_question.children[0].schema_item.widget.id, 'whos-related')
        self.assertEqual(relationship_state_question.children[0].value, 'Brother')
        self.assertEqual(relationship_state_question.children[1].schema_item.widget.id, 'whos-related_1')
        self.assertEqual(relationship_state_question.children[1].value, 'Sister')

    def test_should_set_current_person_on_widget(self):
        # Given
        answer_state = create_answer(group_instance=1)
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock()
            get_answer_store().filter.side_effect = [self.household_answers, self.last_names]
            # When
            relationship_state_question.update_state({})

        # Then
        self.assertEqual(relationship_state_question.children[0].schema_item.widget.current_person, 'Jane Doe')

    def test_should_set_other_person_on_widget(self):
        # Given
        answer_state = create_answer(group_instance=1)
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock()
            get_answer_store().filter.side_effect = [self.household_answers, self.last_names]
            # When
            relationship_state_question.update_state({})

        # Then
        self.assertEqual(relationship_state_question.children[0].schema_item.widget.other_person, 'Joe Bloggs')

    def test_should_display_first_name_if_no_surname_provided(self):
        # Given
        answer_state = create_answer(group_instance=0)
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        first_names = [
            {
                "answer_id": "first-name",
                "answer_instance": 0,
                "value": "John"
            },
            {
                "answer_id": "first-name",
                "answer_instance": 1,
                "value": None
            },
            {
                "answer_id": "first-name",
                "answer_instance": 2,
                "value": 'Joe'
            }
        ]

        last_names = [
            {
                "answer_id": "last-name",
                "answer_instance": 0,
                "value": None
            },
            {
                "answer_id": "last-name",
                "answer_instance": 1,
                "value": 'Doe'
            },
            {
                "answer_id": "last-name",
                "answer_instance": 2,
                "value": 'Bloggs'
            }
        ]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock()
            get_answer_store().filter.side_effect = [first_names, last_names]
            # When
            relationship_state_question.update_state({})

        # Then
        self.assertEqual(relationship_state_question.children[0].schema_item.widget.current_person, 'John')

    def test_should_display_surname_if_no_first_name_provided(self):
        # Given
        answer_state = create_answer(group_instance=0)
        question_schema = Question()
        question_schema.answers = [answer_state.schema_item]
        relationship_state_question = RelationshipStateQuestion('relationship', question_schema)
        relationship_state_question.answers = [answer_state]

        first_names = [
            {
                "answer_id": "first-name",
                "answer_instance": 0,
                "value": "John"
            },
            {
                "answer_id": "first-name",
                "answer_instance": 1,
                "value": None
            },
            {
                "answer_id": "first-name",
                "answer_instance": 2,
                "value": 'Joe'
            }
        ]

        last_names = [
            {
                "answer_id": "last-name",
                "answer_instance": 0,
                "value": None
            },
            {
                "answer_id": "last-name",
                "answer_instance": 1,
                "value": 'Doe'
            },
            {
                "answer_id": "last-name",
                "answer_instance": 2,
                "value": 'Bloggs'
            }
        ]

        with patch('app.questionnaire_state.relationship_state_question.get_answer_store') as get_answer_store:
            get_answer_store().filter = Mock()
            get_answer_store().filter.side_effect = [first_names, last_names]
            # When
            relationship_state_question.update_state({})

        # Then
            self.assertEqual(relationship_state_question.children[0].schema_item.widget.other_person, 'Doe')
