from app.data_model.answer_store import Answer, AnswerStore
from app.helpers.schema_helpers import get_group_instance_id
from app.questionnaire.location import Location
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from tests.app.app_context_test_case import AppContextTestCase


class TestFormHelper(AppContextTestCase):

    def test_get_group_instance_id(self):
        questionnaire = {
            'sections': [{
                'id': 'section1',
                'groups': [
                    {
                        'id': 'group1',
                        'blocks': [
                            {
                                'id': 'block1',
                                'questions': [{
                                    'id': 'question1',
                                    'type': 'Question',
                                    'answers': [
                                        {
                                            'id': 'answer1',
                                            'type': 'TextArea'
                                        }
                                    ]
                                }]
                            }
                        ]
                    },
                    {
                        'id': 'group2',
                        'blocks': [
                            {
                                'id': 'block2',
                                'questions': [{
                                    'id': 'question2',
                                    'type': 'Question',
                                    'answers': [
                                        {
                                            'id': 'answer2',
                                            'type': 'TextArea'
                                        }
                                    ]
                                }]
                            }
                        ],
                        'routing_rules': [{
                            'repeat': {
                                'type': 'group',
                                'group_ids': ['group1']
                            }
                        }]
                    }
                ]
            }]
        }
        schema = QuestionnaireSchema(questionnaire)

        answer_1 = Answer(
            answer_id='answer1',
            group_instance_id='group1-aaa',
            group_instance=0,
            value=25,
        )
        answer_2 = Answer(
            answer_id='answer1',
            group_instance_id='group1-bbb',
            group_instance=1,
            value=65,
        )

        store = AnswerStore(None)
        store.add(answer_1)
        store.add(answer_2)

        location = Location('group2', 0, 'block2')
        self.assertEqual(get_group_instance_id(schema, store, location), 'group1-aaa')

        location = Location('group2', 1, 'block2')
        self.assertEqual(get_group_instance_id(schema, store, location), 'group1-bbb')
