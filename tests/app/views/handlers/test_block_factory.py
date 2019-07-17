from unittest import TestCase

from mock import Mock

from app.views.handlers.block_factory import get_block_handler
from app.questionnaire.location import InvalidLocationException, Location


class TestBlockFactory(TestCase):
    def test_get_handler_invalid_block(self):
        schema = Mock()
        schema.get_block = Mock(return_value=None)
        with self.assertRaises(InvalidLocationException):
            location = Location(block_id='block-id')
            get_block_handler(schema, location, None, None)

    def test_get_handler_invalid_block_type(self):
        schema = Mock()
        schema.get_block = Mock(return_value={'type': 'MadeUpType'})
        with self.assertRaises(ValueError):
            location = Location(block_id='block-id')
            get_block_handler(schema, location, None, None)
