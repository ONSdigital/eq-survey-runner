from unittest import TestCase

from mock import Mock

from app.views.handlers.block_factory import get_block_handler
from app.questionnaire.location import InvalidLocationException, Location


class TestBlockFactory(TestCase):
    def test_get_handler_invalid_block(self):
        schema = Mock()
        schema.get_block = Mock(return_value=None)
        with self.assertRaises(InvalidLocationException):
            get_block_handler(
                schema=schema,
                block_id='invalid-block-id',
                list_item_id=None,
                questionnaire_store=None,
                language=None,
            )

    def test_get_handler_invalid_block_type(self):
        schema = Mock()
        schema.get_block = Mock(return_value={'id': 'some-block', 'type': 'MadeUpType'})
        schema.is_block_in_repeating_section = Mock(return_value=False)

        with self.assertRaises(ValueError):
            get_block_handler(
                schema=schema,
                block_id='some-block',
                list_item_id=None,
                questionnaire_store=None,
                language=None,
            )

    def test_get_handler_invalid_location_missing_list_name_for_repeat(self):
        schema = Mock()
        schema.get_block = Mock(return_value={'id': 'some-block', 'type': 'Question'})
        schema.is_block_in_repeating_section = Mock(return_value=True)

        with self.assertRaises(InvalidLocationException):
            get_block_handler(
                schema=schema,
                block_id='some-block',
                list_item_id=None,
                questionnaire_store=None,
                language=None,
            )

    def test_get_handler_invalid_location_missing_list_item_id_for_repeat(self):
        schema = Mock()
        schema.get_block = Mock(return_value={'id': 'some-block', 'type': 'Question'})
        schema.is_block_in_repeating_section = Mock(return_value=True)

        with self.assertRaises(InvalidLocationException):
            get_block_handler(
                schema=schema,
                block_id='some-block',
                list_item_id=None,
                list_name='people',
                questionnaire_store=None,
                language=None,
            )
