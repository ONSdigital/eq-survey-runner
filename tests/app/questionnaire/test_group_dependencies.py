import unittest
from app.questionnaire.group_dependencies import GroupDependencies
from app.questionnaire.group_dependencies import get_group_dependencies
from app.questionnaire.questionnaire_schema import QuestionnaireSchema


class TestGroupDependencies(unittest.TestCase):
    def test_adding_of_dependencies(self):
        sut = GroupDependencies()

        sut.add('dependent_id', 'dependency_driver_id', 'group')
        sut.add('dependent_id2', 'dependency_driver_id2', 'group')
        sut.add('dependent_id3', 'dependency_driver_id3', 'block')

        self.assertEqual(len(sut), 3)
        self.assertEqual(sut['dependent_id2'], ['dependency_driver_id2'])
        self.assertEqual(sut['group_drivers'], ['dependency_driver_id', 'dependency_driver_id2'])
        self.assertEqual(sut['block_drivers'], ['dependency_driver_id3'])

    def test_duplicate_dependencies_do_not_duplicate(self):
        sut = GroupDependencies()

        sut.add('dependent_id', 'dependency_driver_id', 'group')
        sut.add('dependent_id', 'dependency_driver_id', 'group')
        sut.add('dependent_id2', 'dependency_driver_id2', 'block')
        sut.add('dependent_id2', 'dependency_driver_id2', 'block')

        self.assertEqual(sut['dependent_id'], ['dependency_driver_id'])
        self.assertEqual(sut['dependent_id2'], ['dependency_driver_id2'])
        self.assertEqual(sut['group_drivers'], ['dependency_driver_id'])
        self.assertEqual(sut['block_drivers'], ['dependency_driver_id2'])

    def test_multiple_adds_are_added_to_correct_group(self):
        sut = GroupDependencies()

        sut.add('dependent_id1', 'dependency_driver_id1', 'group')
        sut.add('dependent_id2', 'dependency_driver_id2.1', 'group')
        sut.add('dependent_id2', 'dependency_driver_id2.2', 'group')
        sut.add('dependent_id3', 'dependency_driver_id3.1', 'block')
        sut.add('dependent_id3', 'dependency_driver_id3.2', 'block')
        sut.add('dependent_id3', 'dependency_driver_id3.3', 'block')

        self.assertEqual(sut['dependent_id1'], ['dependency_driver_id1'])
        self.assertEqual(sut['dependent_id2'], ['dependency_driver_id2.1', 'dependency_driver_id2.2'])
        self.assertEqual(sut['dependent_id3'],
                         ['dependency_driver_id3.1', 'dependency_driver_id3.2', 'dependency_driver_id3.3'])
        self.assertEqual(sut['group_drivers'],
                         ['dependency_driver_id1', 'dependency_driver_id2.1', 'dependency_driver_id2.2'])
        self.assertEqual(sut['block_drivers'],
                         ['dependency_driver_id3.1', 'dependency_driver_id3.2', 'dependency_driver_id3.3'])

    def test_dependencies_can_be_added_with_update_without_duplicates(self):
        sut_a = GroupDependencies()
        sut_a.add('dependent_id1', 'dependency_driver_id1', 'group')
        sut_a.add('dependent_id2', 'dependency_driver_id2.1', 'group')
        sut_a.add('dependent_id2', 'dependency_driver_id2.2', 'group')
        sut_a.add('dependent_id3', 'dependency_driver_id3.1', 'block')

        sut_b = GroupDependencies()
        sut_a.add('dependent_id2', 'dependency_driver_id2.1', 'group')
        sut_b.add('dependent_id3', 'dependency_driver_id3.1', 'block')
        sut_b.add('dependent_id3', 'dependency_driver_id3.2', 'block')
        sut_b.add('dependent_id3', 'dependency_driver_id3.3', 'block')

        sut_a.update(sut_b)

        self.assertEqual(sut_a['dependent_id1'], ['dependency_driver_id1'])
        self.assertEqual(sut_a['dependent_id2'], ['dependency_driver_id2.1', 'dependency_driver_id2.2'])
        self.assertEqual(sut_a['dependent_id3'],
                         ['dependency_driver_id3.1', 'dependency_driver_id3.2', 'dependency_driver_id3.3'])
        self.assertEqual(sut_a['group_drivers'],
                         ['dependency_driver_id1', 'dependency_driver_id2.1', 'dependency_driver_id2.2'])
        self.assertEqual(sut_a['block_drivers'],
                         ['dependency_driver_id3.1', 'dependency_driver_id3.2', 'dependency_driver_id3.3'])


class TestGetDependencies(unittest.TestCase):

    def test_repeat_with_group_ids_added_to_dependencies(self):
        survey_json = {
            'sections': [{
                'id': 'default-section',
                'groups': [
                    {
                        'id': 'dependent-group',
                        'routing_rules': [{
                            'repeat': {
                                'type': 'group',
                                'group_ids': [
                                    'primary-group',
                                    'repeating-group'
                                ]
                            }
                        }],
                        'blocks': [{
                            'type': 'Question',
                            'id': 'dependent-block',
                            'questions': [{
                                'id': 'dependent-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'dependent-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        dependencies = get_group_dependencies(schema)

        self.assertEqual(len(dependencies), 1)
        self.assertEqual(dependencies['dependent-group'], ['primary-group', 'repeating-group'])
        self.assertEqual(dependencies['group_drivers'], ['primary-group', 'repeating-group'])
        self.assertEqual(dependencies['block_drivers'], [])

    def test_repeat_with_answer_count_added_to_dependencies(self):
        survey_json = {
            'sections': [{
                'id': 'default-section',
                'groups': [
                    {
                        'id': 'driving-group',
                        'blocks': [{
                            'type': 'Question',
                            'id': 'driving-block',
                            'questions': [{
                                'id': 'driving-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'driving-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    },
                    {
                        'id': 'dependent-group',
                        'routing_rules': [{
                            'repeat': {
                                'type': 'answer_count',
                                'answer_id': 'driving-answer'
                            }
                        }],
                        'blocks': [{
                            'type': 'Question',
                            'id': 'dependent-block',
                            'questions': [{
                                'id': 'dependent-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'dependent-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        dependencies = get_group_dependencies(schema)

        self.assertEqual(len(dependencies), 1)
        self.assertEqual(dependencies['dependent-group'], ['driving-block'])
        self.assertEqual(dependencies['group_drivers'], [])
        self.assertEqual(dependencies['block_drivers'], ['driving-block'])

    def test_repeat_with_answer_count_minus_one_added_to_dependencies(self):
        survey_json = {
            'sections': [{
                'id': 'default-section',
                'groups': [
                    {
                        'id': 'driving-group',
                        'blocks': [{
                            'type': 'Question',
                            'id': 'driving-block',
                            'questions': [{
                                'id': 'driving-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'driving-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    },
                    {
                        'id': 'dependent-group',
                        'routing_rules': [{
                            'repeat': {
                                'type': 'answer_count_minus_one',
                                'answer_id': 'driving-answer'
                            }
                        }],
                        'blocks': [{
                            'type': 'Question',
                            'id': 'dependent-block',
                            'questions': [{
                                'id': 'dependent-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'dependent-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        dependencies = get_group_dependencies(schema)

        self.assertEqual(len(dependencies), 1)
        self.assertEqual(dependencies['dependent-group'], ['driving-block'])
        self.assertEqual(dependencies['group_drivers'], [])
        self.assertEqual(dependencies['block_drivers'], ['driving-block'])

    def test_repeat_with_relationship_block_not_added_to_dependencies(self):
        survey_json = {
            'sections': [{
                'id': 'default-section',
                'groups': [
                    {
                        'id': 'driving-group',
                        'blocks': [{
                            'type': 'Question',
                            'id': 'driving-block',
                            'questions': [{
                                'id': 'driving-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'driving-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    },
                    {
                        'id': 'dependent-group',
                        'routing_rules': [{
                            'repeat': {
                                'type': 'answer_count',
                                'answer_id': 'driving-answer'
                            }
                        }],
                        'blocks': [{
                            'type': 'Question',
                            'id': 'dependent-block',
                            'questions': [{
                                'id': 'dependent-question',
                                'type': 'Relationship',
                                'answers': [{
                                    'id': 'dependent-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        dependencies = get_group_dependencies(schema)

        self.assertEqual(len(dependencies), 0)
        self.assertEqual(dependencies['group_drivers'], [])
        self.assertEqual(dependencies['block_drivers'], [])

    def test_repeat_with_answer_value_not_added_to_dependencies(self):
        survey_json = {
            'sections': [{
                'id': 'default-section',
                'groups': [
                    {
                        'id': 'driving-group',
                        'blocks': [{
                            'type': 'Question',
                            'id': 'driving-block',
                            'questions': [{
                                'id': 'driving-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'driving-answer',
                                    'type': 'Number'
                                }]
                            }]
                        }]
                    },
                    {
                        'id': 'dependent-group',
                        'routing_rules': [{
                            'repeat': {
                                'type': 'answer_value',
                                'answer_id': 'driving-answer'
                            }
                        }],
                        'blocks': [{
                            'type': 'Question',
                            'id': 'dependent-block',
                            'questions': [{
                                'id': 'dependent-question',
                                'type': 'General',
                                'answers': [{
                                    'id': 'dependent-answer',
                                    'type': 'TextField'
                                }]
                            }]
                        }]
                    }]
            }]
        }

        schema = QuestionnaireSchema(survey_json)
        dependencies = get_group_dependencies(schema)

        self.assertEqual(len(dependencies), 0)
        self.assertEqual(dependencies['group_drivers'], [])
        self.assertEqual(dependencies['block_drivers'], [])
