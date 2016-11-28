from unittest import TestCase

from app.schema.skip_condition import SkipCondition
from app.schema.when import When


class TestSkipCondition(TestCase):
    def test_as_dict(self):
        skip = SkipCondition()
        skip.when = When()

        copy = skip.as_dict()

        self.assertIsNot(copy, skip.__dict__)
        self.assertIsNot(copy['when'], skip.when.__dict__)
        self.assertEqual(copy['when'], skip.when.__dict__)

    def test_as_dict_no_when(self):
        skip = SkipCondition()

        copy = skip.as_dict()

        self.assertIsNot(copy, skip.__dict__)
        self.assertEqual(copy, skip.__dict__)
