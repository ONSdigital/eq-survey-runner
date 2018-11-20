from unittest import TestCase
from app.questionnaire.routing_path import RoutingPath
from app.questionnaire.location import Location


class TestRouter(TestCase):
    def setUp(self):
        self.blocks = [
            Location('group-a', 0, 'block-a'),
            Location('group-b', 0, 'block-b'),
            Location('group-b', 0, 'block-c'),
            Location('group-b', 1, 'block-b'),
            Location('group-b', 1, 'block-c')
        ]
        self.routing_path = RoutingPath(self.blocks)
        super().setUp()

    def test_eq_to_routing_path(self):
        self.assertEqual(self.routing_path, self.routing_path)

    def test_eq_to_list(self):
        self.assertEqual(self.blocks, self.routing_path)

    def test_len(self):
        self.assertEqual(len(self.blocks), len(self.routing_path))

    def test_reversed(self):
        self.assertEqual(
            list(reversed(self.blocks)),
            list(reversed(self.routing_path))
        )

    def test_contains_true(self):
        self.assertIn(self.blocks[0], self.routing_path)
        self.assertNotIn(Location('group-z', 0, 'block-z'), self.routing_path)

    def test_iter(self):
        self.assertEqual(self.blocks[0], next(iter(self.routing_path)))

    def test_getitem(self):
        self.assertEqual(self.blocks[0], self.routing_path[0])
