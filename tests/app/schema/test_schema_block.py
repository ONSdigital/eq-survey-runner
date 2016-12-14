import unittest

from app.schema.block import Block
from app.schema.group import Group
from app.schema.questionnaire import Questionnaire


class TestSchemaBlock(unittest.TestCase):

    def test_should_return_true_if_first_in_schema(self):
        # Given
        questionnaire = Questionnaire()
        group = Group()
        block = Block('first-block')

        questionnaire.add_group(group)
        group.add_block(block)

        # When
        result = block.first_in_schema()

        # Then
        self.assertTrue(result)

    def test_should_return_false_if_not_first_block_in_group(self):
        # Given
        questionnaire = Questionnaire()
        group = Group()
        first = Block('first-block')
        second = Block('second-block')

        questionnaire.add_group(group)
        group.add_block(first)
        group.add_block(second)

        # When
        result = second.first_in_schema()

        # Then
        self.assertFalse(result)

    def test_should_return_false_if_not_first_group_in_questionnaire(self):
        # Given
        questionnaire = Questionnaire()
        first_group = Group()
        second_group = Group()
        block = Block('block-id')

        questionnaire.add_group(first_group)
        questionnaire.add_group(second_group)
        second_group.add_block(block)

        # When
        result = block.first_in_schema()

        # Then
        self.assertFalse(result)

    def test_should_return_true_if_first_block_when_multiple_groups_in_questionnaire(self):
        # Given
        questionnaire = Questionnaire()

        first_group = Group()
        second_group = Group()

        first_block = Block('first')
        second_block = Block('second')
        third_block = Block('third')
        fourth_block = Block('fourth')

        questionnaire.add_group(first_group)
        questionnaire.add_group(second_group)

        first_group.add_block(first_block)
        first_group.add_block(second_block)

        second_group.add_block(third_block)
        second_group.add_block(fourth_block)

        # Then
        self.assertTrue(first_block.first_in_schema())
        self.assertFalse(second_block.first_in_schema())
        self.assertFalse(third_block.first_in_schema())
        self.assertFalse(fourth_block.first_in_schema())
