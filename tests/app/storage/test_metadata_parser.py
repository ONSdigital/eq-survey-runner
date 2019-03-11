from unittest import TestCase
from datetime import datetime

import pytest

from app.storage.metadata_parser import boolean_parser, uuid_4_parser, iso_8601_date_parser


class TestMetaDataValidators(TestCase):

    def simple_mapping_assertion(self, method, value, expected, exc_type=Exception):
        """Given a method which should be called, assert that expected is
           returned. A special case is when expected=='err', expect an error
           to be raised."""
        if expected == 'err':
            with pytest.raises(exc_type):
                method(value)
        else:
            self.assertEqual(method(value), expected)

    def test_boolean_validator(self):
        """ Asserts that only boolean True/False are accepted"""
        variations = (
            ('False', 'err'),
            ('True', 'err'),
            (0, 'err'),
            (1, 'err'),
            (True, True),
            (False, False),
            ({}, 'err'),
            (tuple(), 'err'),
        )
        for (claim_value, expected) in variations:
            self.simple_mapping_assertion(boolean_parser, claim_value, expected, TypeError)

    def test_uuid_4_parser(self):
        """ Asserts that only boolean True/False are accepted"""
        variations = (
            ('False', 'err'),
            (0, 'err'),
            (1, 'err'),
            (True, 'err'),
            (False, 'err'),
            ({}, 'err'),
            (tuple(), 'err'),
            ('3e0a497f-ee63-4b12-b0b9-234eca1850fa', '3e0a497f-ee63-4b12-b0b9-234eca1850fa'),
            ('8b8d701d-1f76-430a-895f-53c9030f7ca2', '8b8d701d-1f76-430a-895f-53c9030f7ca2'),
        )
        for (claim_value, expected) in variations:
            self.simple_mapping_assertion(uuid_4_parser, claim_value, expected)

    def test_iso_8601_date_parser(self):
        """ Asserts that only boolean True/False are accepted"""
        variations = (
            ('False', 'err'),
            (0, 'err'),
            (1, 'err'),
            (True, 'err'),
            (False, 'err'),
            ({}, 'err'),
            (tuple(), 'err'),
            ('3e0a497f-ee63-4b12-b0b9-234eca1850fa', 'err'),
            ('1970-01-15', datetime(1970, 1, 15)),
            ('1998-09-21', datetime(1998, 9, 21)),
        )
        for (claim_value, expected) in variations:
            self.simple_mapping_assertion(iso_8601_date_parser, claim_value, expected)
