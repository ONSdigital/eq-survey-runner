import unittest

from app.schema_loader.schema_loader import load_schema_file
from app.helpers.schema_helper import SchemaHelper


class TestSchemaHelper(unittest.TestCase):

    def test_first_block_id(self):
        survey = load_schema_file("test_repeating_household.json")

        first_block_id = "household-composition"

        self.assertEqual(SchemaHelper.get_first_block_id(survey), first_block_id)

    def test_first_group_id(self):
        survey = load_schema_file("test_repeating_household.json")

        first_group_id = "multiple-questions-group"

        self.assertEqual(SchemaHelper.get_first_group_id(survey), first_group_id)

    def test_last_group_id(self):
        survey = load_schema_file("test_repeating_household.json")

        last_group_id = "repeating-group"

        self.assertEqual(last_group_id, SchemaHelper.get_last_group_id(survey))

    def test_get_blocks(self):
        survey = load_schema_file("test_repeating_household.json")
        blocks = [b for b in SchemaHelper.get_blocks(survey)]

        self.assertEqual(len(blocks), 3)

    def test_get_groups(self):
        survey = load_schema_file("test_repeating_household.json")
        groups = [group for group in SchemaHelper.get_groups(survey)]

        self.assertEqual(len(groups), 2)

    def test_get_group(self):
        survey = load_schema_file("test_repeating_household.json")
        group = SchemaHelper.get_group(survey, "repeating-group")

        self.assertEqual(group['title'], "Group 2")

    def test_get_block(self):
        survey = load_schema_file("test_repeating_household.json")
        block = SchemaHelper.get_block(survey, "repeating-block-1")

        self.assertEqual(block['title'], "Block 2")

    def test_get_repeat_rules(self):
        survey = load_schema_file("test_repeating_household.json")
        groups = [group for group in SchemaHelper.get_groups(survey)]
        rules = [rule for rule in SchemaHelper.get_repeat_rules(groups[1])]

        self.assertEqual(len(rules), 1)
