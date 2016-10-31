import unittest

from app.questionnaire.navigator import Navigator
from app.schema_loader.schema_loader import load_schema_file


class TestNavigator(unittest.TestCase):

    def test_first_block(self):
        survey = load_schema_file("1_0102.json")

        first_block_id = "5bce8d8f-0af8-4d35-b77d-744e6179b406"

        navigator = Navigator(survey)
        self.assertEqual(navigator.get_first_block_id(), first_block_id)

    def test_previous_block(self):
        survey = load_schema_file("1_0102.json")

        current_block_id = "02ed26ad-4cfc-4e29-a946-630476228b2c"
        previous_block_id = "7418732e-12fb-4270-8307-5682ac63bfae"

        navigator = Navigator(survey)
        self.assertEqual(navigator.get_previous_location(current_location_id=current_block_id), previous_block_id)

    def test_next_with_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            "96682325-47ab-41e4-a56e-8315a19ffe2a",
            "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
            "an3b74d1-b687-4051-9634-a8f9ce10ard",
            "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
        ]

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "No"
        }

        current_block_id = expected_path[1]
        expected_next_block_id = expected_path[2]

        navigator = Navigator(survey)
        actual_next_block_id = navigator.get_next_location(answers, current_block_id)

        self.assertEqual(actual_next_block_id, expected_next_block_id)

        current_block_id = expected_path[2]
        expected_next_block_id = expected_path[3]
        actual_next_block_id = navigator.get_next_location(answers, current_block_id)

        self.assertEqual(actual_next_block_id, expected_next_block_id)

    def test_previous_with_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
            "26f2c4b3-28ac-4072-9f18-a6a6c6f660db",
            "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
            "an3b74d1-b687-4051-9634-a8f9ce10ard",
            "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
        ]

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Dark Side",
            "pel989b8-5185-4ba6-b73f-c126e3a06ba7": "Can I be a pain and have a goodies ship"
        }

        current_block_id = expected_path[3]
        expected_previous_block_id = expected_path[2]

        navigator = Navigator(survey)
        actual_previous_block_id = navigator.get_previous_location(answers, current_block_id)

        self.assertEqual(actual_previous_block_id, expected_previous_block_id)

        current_block_id = expected_path[2]
        expected_previous_block_id = expected_path[1]

        actual_previous_block_id = navigator.get_previous_location(answers, current_block_id)

        self.assertEqual(actual_previous_block_id, expected_previous_block_id)

    def test_next_block(self):
        survey = load_schema_file("1_0102.json")

        current_block_id = "7418732e-12fb-4270-8307-5682ac63bfae"
        next_block_id = "02ed26ad-4cfc-4e29-a946-630476228b2c"

        navigator = Navigator(survey)
        self.assertEqual(navigator.get_next_location(current_location_id=current_block_id), next_block_id)

    def test_routing_basic_path(self):
        survey = load_schema_file("1_0112.json")
        expected_path = [
            "980b148e-0856-4e50-9afe-67a4fa6ae13b",
            "6c8a2f39-e0d8-406f-b463-2151225abea2",
            "0c7c8876-6a63-4251-ac29-b821b3e9b1bc",
            "a42b5752-1896-4f52-9d58-320085be92a7",
            "0b29d3f7-5905-43d8-9921-5b353db68104",
            "7e2d49eb-ffc7-4a61-a45d-eba336d1d0e6",
        ]

        navigator = Navigator(survey)
        routing_path = navigator.get_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_routing_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            "96682325-47ab-41e4-a56e-8315a19ffe2a",
            "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
            "an3b74d1-b687-4051-9634-a8f9ce10ard",
            "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
        ]

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "No"
        }

        navigator = Navigator(survey)
        routing_path = navigator.get_routing_path(answers)

        self.assertEqual(routing_path, expected_path)

    def test_routing_basic_and_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
            "26f2c4b3-28ac-4072-9f18-a6a6c6f660db",
            "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
            "an3b74d1-b687-4051-9634-a8f9ce10ard",
            "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
        ]

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Dark Side",
            "pel989b8-5185-4ba6-b73f-c126e3a06ba7": "Can I be a pain and have a goodies ship"
        }

        navigator = Navigator(survey)
        routing_path = navigator.get_routing_path(answers)

        self.assertEqual(routing_path, expected_path)

    def test_previous_with_conditional_routing(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            "96682325-47ab-41e4-a56e-8315a19ffe2a",
            "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
            "an3b74d1-b687-4051-9634-a8f9ce10ard",
            "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
        ]

        current_block_id = expected_path[2]
        expected_previous_block_id = expected_path[1]

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "No"
        }

        navigator = Navigator(survey)

        self.assertEqual(navigator.get_previous_location(answers, current_block_id), expected_previous_block_id)

    def test_get_next_location_introduction(self):
        survey = load_schema_file("0_star_wars.json")

        navigator = Navigator(survey)

        next_location = navigator.get_next_location(current_location_id='introduction')

        self.assertEqual('f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0', next_location)

    def test_get_next_location_summary(self):
        survey = load_schema_file("0_star_wars.json")

        navigator = Navigator(survey)

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "No"
        }

        current_location_id = 'an3b74d1-b687-4051-9634-a8f9ce10ard'
        next_location_id = navigator.get_next_location(answers, current_location_id)
        expected_next_location_id = '846f8514-fed2-4bd7-8fb2-4b5fcb1622b1'

        self.assertEqual(expected_next_location_id, next_location_id)

        current_location_id = '846f8514-fed2-4bd7-8fb2-4b5fcb1622b1'
        next_location_id = navigator.get_next_location(answers, current_location_id)
        expected_next_location_id = 'summary'

        self.assertEqual(expected_next_location_id, next_location_id)

    def test_get_previous_location(self):
        survey = load_schema_file("0_star_wars.json")

        navigator = Navigator(survey)

        next_location = navigator.get_previous_location(current_location_id='f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0')

        self.assertEqual('introduction', next_location)

    def test_get_previous_location_conditional(self):
        survey = load_schema_file("0_star_wars.json")
        navigator = Navigator(survey)

        expected_path = [
            "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            "96682325-47ab-41e4-a56e-8315a19ffe2a",
            "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
            "an3b74d1-b687-4051-9634-a8f9ce10ard",
            "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
        ]

        current_location_id = expected_path[2]
        expected_previous_location_id = expected_path[1]

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side",
            "2e0989b8-5185-4ba6-b73f-c126e3a06ba7": "No"
        }

        self.assertEqual(navigator.get_previous_location(answers, current_location_id), expected_previous_location_id)

        current_location_id = expected_path[0]
        expected_previous_location_id = 'introduction'

        self.assertEqual(navigator.get_previous_location(answers, current_location_id), expected_previous_location_id)

    def test_next_location_goto_summary(self):
        survey = load_schema_file("0_star_wars.json")
        navigator = Navigator(survey)

        expected_path = [
            'introduction',
            'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0',
            'summary'
        ]

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "I prefer Star Trek"
        }

        current_location_id = expected_path[1]
        expected_next_location_id = expected_path[2]

        next_location_id = navigator.get_next_location(answers, current_location_id)

        self.assertEqual(next_location_id, expected_next_location_id)

    def test_next_location_empty_routing_rules(self):
        survey = load_schema_file("test_checkbox.json")
        navigator = Navigator(survey)

        # Force some empty routing rules
        navigator.blocks[0]['routing_rules'] = []

        expected_path = [
          'introduction',
          'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0',
          'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc1',
          'summary'
        ]

        answers = {
          "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Cheese",
          "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23": "deep pan",
        }

        current_location_id = expected_path[1]
        expected_next_location_id = expected_path[2]

        next_location_id = navigator.get_next_location(answers, current_location_id)

        self.assertEqual(next_location_id, expected_next_location_id)

    def test_interstitial_post_blocks(self):
        survey = load_schema_file("0_star_wars.json")
        navigator = Navigator(survey)

        answers = {
            "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c": "Light Side"
        }

        self.assertFalse('summary' in navigator.get_location_path(answers))
