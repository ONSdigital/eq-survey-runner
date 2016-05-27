from app.model.group import Group
from app.model.block import Block
import unittest
import json


class GroupModelTest(unittest.TestCase):
    def test_basics(self):
        group = Group()

        group.id = 'some-id'
        group.title = 'my group object'

        block1 = Block()
        block2 = Block()

        group.add_block(block1)
        group.add_block(block2)

        self.assertEquals(group.id, 'some-id')
        self.assertEquals(group.title, 'my group object')
        self.assertIsNone(group.container)
        self.assertEquals(len(group.blocks), 2)
        self.assertEquals(group.blocks[0], block1)
        self.assertEquals(group.blocks[1], block2)

        self.assertEquals(block1.container, group)
        self.assertEquals(block2.container, group)

    def test_to_json(self):
        group = Group()

        group.id = 'some-id'
        group.title = 'my group object'

        block1 = Block()
        block2 = Block()

        group.add_block(block1)
        group.add_block(block2)

        json_str = json.dumps(group.to_json())
        json_obj = json.loads(json_str)

        self.assertEquals(json_obj['id'], 'some-id')
        self.assertEquals(json_obj['title'], 'my group object')
        self.assertEquals(len(json_obj['blocks']), 2)
