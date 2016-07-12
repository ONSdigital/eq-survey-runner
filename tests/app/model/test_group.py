from app.schema.group import Group
from app.schema.block import Block
import unittest


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

        self.assertEquals(group.id, 'some-id')
        self.assertEquals(group.title, 'my group object')
        self.assertIsNone(group.container)
        self.assertEquals(len(group.blocks), 2)
        self.assertEquals(group.blocks[0], block1)
        self.assertEquals(group.blocks[1], block2)

        self.assertEquals(block1.container, group)
        self.assertEquals(block2.container, group)
