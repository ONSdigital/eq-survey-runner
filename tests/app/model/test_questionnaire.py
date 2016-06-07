from app.model.questionnaire import Questionnaire, QuestionnaireException
from app.model.group import Group
from app.model.block import Block
import unittest


class QuestionnaireModelTest(unittest.TestCase):
    def test_basics(self):
        questionnaire = Questionnaire()

        questionnaire.id = 'some-id'
        questionnaire.title = 'my questionnaire object'

        group1 = Group()
        group1.id = 'group-1'
        group2 = Group()
        group2.id = 'group-2'

        questionnaire.add_group(group1)
        questionnaire.add_group(group2)

        self.assertEquals(questionnaire.id, 'some-id')
        self.assertEquals(questionnaire.title, 'my questionnaire object')
        self.assertEquals(len(questionnaire.groups), 2)
        self.assertEquals(questionnaire.groups[0], group1)
        self.assertEquals(questionnaire.groups[1], group2)

        self.assertEquals(group1.container, questionnaire)
        self.assertEquals(group2.container, questionnaire)

    def test_get_item_by_id(self):
        questionnaire = Questionnaire()

        questionnaire.id = 'some-id'
        questionnaire.title = 'my questionnaire object'

        # The order that items is added is important otherwise,
        # items are ot registered on the questionnaire
        group1 = Group()
        group1.id = 'group-1'
        questionnaire.add_group(group1)

        block1 = Block()
        block1.id = 'block-1'
        group1.add_block(block1)

        group2 = Group()
        group2.id = 'group-2'
        questionnaire.add_group(group2)

        block2 = Block()
        block2.id = 'block-2'
        group2.add_block(block2)

        self.assertRaises(QuestionnaireException, questionnaire.get_item_by_id, 'group-1')
        self.assertRaises(QuestionnaireException, questionnaire.get_item_by_id, 'group-2')
        self.assertRaises(QuestionnaireException, questionnaire.get_item_by_id, 'block-1')
        self.assertRaises(QuestionnaireException, questionnaire.get_item_by_id, 'block-2')

        questionnaire.register(group1)
        questionnaire.register(group2)
        questionnaire.register(block1)
        questionnaire.register(block2)

        self.assertEquals(questionnaire.get_item_by_id('group-1'), group1)
        self.assertEquals(questionnaire.get_item_by_id('group-2'), group2)
        self.assertEquals(questionnaire.get_item_by_id('block-1'), block1)
        self.assertEquals(questionnaire.get_item_by_id('block-2'), block2)

    def test_register_duplicate(self):
        questionnaire = Questionnaire()

        questionnaire.id = 'some-id'
        questionnaire.title = 'my questionnaire object'

        group1 = Group()
        group1.id = 'group-1'
        questionnaire.add_group(group1)
        questionnaire.register(group1)

        group = questionnaire.get_item_by_id('group-1')
        self.assertEqual(group1, group)

        group2 = Group()
        group2.id = 'group-1'  # Duplicate id

        self.assertRaises(QuestionnaireException, questionnaire.register, group2)

    def test_equivalence(self):
        questionnaire1 = Questionnaire()

        questionnaire1.id = 'some-id'
        questionnaire1.title = 'my questionnaire object'

        # The order that items is added is important otherwise,
        # items are ot registered on the questionnaire
        group1_1 = Group()
        group1_1.id = 'group-1'
        questionnaire1.add_group(group1_1)

        block1_1 = Block()
        block1_1.id = 'block-1'
        group1_1.add_block(block1_1)

        group1_2 = Group()
        group1_2.id = 'group-2'
        questionnaire1.add_group(group1_2)

        block1_2 = Block()
        block1_2.id = 'block-2'
        group1_2.add_block(block1_2)

        questionnaire2 = Questionnaire()

        questionnaire2.id = 'some-id'
        questionnaire2.title = 'my questionnaire object'

        # The order that items is added is important otherwise,
        # items are ot registered on the questionnaire
        group2_1 = Group()
        group2_1.id = 'group-1'
        questionnaire2.add_group(group2_1)

        block2_1 = Block()
        block2_1.id = 'block-1'
        group2_1.add_block(block2_1)

        group2_2 = Group()
        group2_2.id = 'group-2'
        questionnaire2.add_group(group2_2)

        block2_2 = Block()
        block2_2.id = 'block-2'
        group2_2.add_block(block2_2)

        self.assertEquals(questionnaire1, questionnaire2)
