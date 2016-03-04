from app.questionnaire.questionnaire_manager import QuestionnaireManager

import unittest


class QuestionnaireManagerTest(unittest.TestCase):

    def test_process_incoming_response(self):
        schema = {}
        questionnaire_manager = QuestionnaireManager(schema)
        questionnaire_manager.process_incoming_response(1)
        self.assertIsNotNone(questionnaire_manager.get_rendering_context())

    def test_get_rendering_context(self):
        '''
        check that the get rendering context returns nothing
        '''
        schema = {}
        questionnaire_manager = QuestionnaireManager(schema)
        self.assertIsNone(questionnaire_manager.get_rendering_context())


if __name__ == '__main__':
    unittest.main()
