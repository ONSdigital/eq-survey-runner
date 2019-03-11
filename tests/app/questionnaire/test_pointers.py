import unittest

from app.questionnaire.placeholder_renderer import find_pointers_containing


class TestPointers(unittest.TestCase):

    @staticmethod
    def test_find_pointers_containing_root():
        schema = {
            'test': ''
        }

        pointers = [p for p in find_pointers_containing(schema, 'test')]

        assert pointers == []

    @staticmethod
    def test_find_pointers_containing_element():
        schema = {
            'this': 'is',
            'a': {
                'test': 'schema'
            }
        }

        pointers = find_pointers_containing(schema, 'test')

        assert '/a' in pointers

    @staticmethod
    def test_find_pointers_containing_list():
        schema = {
            'this': 'is',
            'a': {
                'test': [{
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }, {
                    'item': {}
                }]
            }
        }

        pointers = find_pointers_containing(schema, 'item')

        assert '/a/test/0' in pointers
        assert '/a/test/1' in pointers
        assert '/a/test/2' in pointers
        assert '/a/test/3' in pointers
        assert '/a/test/4' in pointers
