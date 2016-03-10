from app.model.block import Block
from app.model.section import Section
import unittest


class BlockModelTest(unittest.TestCase):
    def test_basics(self):
        block = Block()

        block.id = 'some-id'
        block.title = 'my block object'

        section1 = Section()
        section2 = Section()

        block.add_section(section1)
        block.add_section(section2)

        self.assertEquals(block.id, 'some-id')
        self.assertEquals(block.title, 'my block object')
        self.assertIsNone(block.container)
        self.assertEquals(len(block.sections), 2)
        self.assertEquals(block.sections[0], section1)
        self.assertEquals(block.sections[1], section2)

        self.assertEquals(section1.container, block)
        self.assertEquals(section2.container, block)
