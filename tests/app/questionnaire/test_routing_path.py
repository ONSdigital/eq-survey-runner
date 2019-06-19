from unittest import TestCase
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.location import Location


class TestRouter(TestCase):
    def setUp(self):
        self.locations = [
            Location('block-a'),
            Location('block-b'),
            Location('block-c'),
            Location('block-b'),
            Location('block-c'),
        ]
        self.routing_path = RoutingPath(self.locations)
        super().setUp()

    def test_eq_to_routing_path(self):
        self.assertEqual(self.routing_path, self.routing_path)

    def test_eq_to_list(self):
        self.assertEqual(self.locations, self.routing_path)

    def test_len(self):
        self.assertEqual(len(self.locations), len(self.routing_path))

    def test_reversed(self):
        self.assertEqual(
            list(reversed(self.locations)), list(reversed(self.routing_path))
        )

    def test_contains_true(self):
        self.assertIn(self.locations[0], self.routing_path)
        self.assertNotIn(Location('block-z'), self.routing_path)

    def test_iter(self):
        self.assertEqual(self.locations[0], next(iter(self.routing_path)))

    def test_getitem(self):
        self.assertEqual(self.locations[0], self.routing_path[0])
