from unittest import TestCase

from app.schema.questionnaire import Questionnaire


class TestSchemaQuestionnaire(TestCase):

    def test_get_item_by_id_answer_without_instance_id(self):

        items_by_id = {
            'item1': 'Item 1'
        }

        questionnaire = Questionnaire()
        questionnaire.items_by_id = items_by_id

        item_id = questionnaire.get_item_by_id('item1')
        self.assertEqual(item_id, 'Item 1')
