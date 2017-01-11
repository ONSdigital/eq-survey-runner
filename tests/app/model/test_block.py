import unittest

from app.schema.block import Block
from app.schema.section import Section


class BlockModelTest(unittest.TestCase):
    def test_basics(self):
        block = Block()

        block.id = 'some-id'
        block.title = 'my block object'

        section1 = Section()
        section1.id = 'section-1'
        section2 = Section()
        section2.id = 'section-2'

        block.add_section(section1)
        block.add_section(section2)

        self.assertEqual(block.id, 'some-id')
        self.assertEqual(block.title, 'my block object')
        self.assertIsNone(block.container)
        self.assertEqual(len(block.sections), 2)
        self.assertEqual(block.sections[0], section1)
        self.assertEqual(block.sections[1], section2)

        self.assertEqual(section1.container, block)
        self.assertEqual(section2.container, block)
