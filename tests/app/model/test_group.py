import unittest

from app.schema.block import Block
from app.schema.group import Group


class GroupModelTest(unittest.TestCase):
    def test_basics(self):
        group = Group()

        group.id = 'some-id'
        group.title = 'my group object'

        block1 = Block()
        block1.id = 'block-1'
        block2 = Block()
        block2.id = 'block-2'

        group.add_block(block1)
        group.add_block(block2)

        self.assertEqual(group.id, 'some-id')
        self.assertEqual(group.title, 'my group object')
        self.assertIsNone(group.container)
        self.assertEqual(len(group.blocks), 2)
        self.assertEqual(group.blocks[0], block1)
        self.assertEqual(group.blocks[1], block2)

        self.assertEqual(block1.container, group)
        self.assertEqual(block2.container, group)
