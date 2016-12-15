import unittest

from app.questionnaire.navigator import Navigator
from app.schema_loader.schema_loader import load_schema_file
from app.data_model.answer_store import Answer, AnswerStore


class TestNavigator(unittest.TestCase):

    def test_next_block(self):
        survey = load_schema_file("1_0102.json")

        current_block_id = "7418732e-12fb-4270-8307-5682ac63bfae"
        next_block = {
            "block_id": "02ed26ad-4cfc-4e29-a946-630476228b2c",
            "group_id": "07f40cd2-0704-4804-9f32-19309089a51b",
            "group_instance": 0
        }

        navigator = Navigator(survey)
        self.assertEqual(navigator.get_next_location(current_block_id=current_block_id), next_block)

    def test_previous_block(self):
        survey = load_schema_file("1_0102.json")

        current_block_id = "02ed26ad-4cfc-4e29-a946-630476228b2c"

        previous_block = {
            "block_id": "7418732e-12fb-4270-8307-5682ac63bfae",
            "group_id": "07f40cd2-0704-4804-9f32-19309089a51b",
            "group_instance": 0
        }

        navigator = Navigator(survey)
        self.assertEqual(navigator.get_previous_location(current_block_id=current_block_id), previous_block)

    def test_introduction_in_path_when_in_schema(self):
        survey = load_schema_file("1_0102.json")

        navigator = Navigator(survey)

        blocks = [b['block_id'] for b in navigator.get_location_path()]

        self.assertIn('introduction', blocks)

    def test_introduction_not_in_path_when_not_in_schema(self):
        survey = load_schema_file("census_individual.json")

        navigator = Navigator(survey)

        blocks = [b['block_id'] for b in navigator.get_location_path()]

        self.assertNotIn('introduction', blocks)

    def test_next_with_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0"},
            {"block_id": "96682325-47ab-41e4-a56e-8315a19ffe2a"},
            {"block_id": "cd3b74d1-b687-4051-9634-a8f9ce10a27d"},
            {"block_id": "an3b74d1-b687-4051-9634-a8f9ce10ard"},
            {"block_id": "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"}
        ]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="96682325-47ab-41e4-a56e-8315a19ffe2a",
            answer_id="2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="No"
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        current_block_id = expected_path[1]["block_id"]
        expected_next_block = expected_path[2]

        navigator = Navigator(survey, answer_store=answers)
        actual_next_block = navigator.get_next_location(current_block_id=current_block_id)

        self.assertEqual(actual_next_block["block_id"], expected_next_block["block_id"])

        current_block_id = expected_path[2]["block_id"]
        expected_next_block = expected_path[3]

        actual_next_block = navigator.get_next_location(current_block_id=current_block_id)

        self.assertEqual(actual_next_block["block_id"], expected_next_block["block_id"])

    def test_routing_basic_path(self):
        survey = load_schema_file("1_0112.json")

        expected_path = [
            {"block_id": "980b148e-0856-4e50-9afe-67a4fa6ae13b"},
            {"block_id": "6c8a2f39-e0d8-406f-b463-2151225abea2"},
            {"block_id": "0c7c8876-6a63-4251-ac29-b821b3e9b1bc"},
            {"block_id": "a42b5752-1896-4f52-9d58-320085be92a7"},
            {"block_id": "0b29d3f7-5905-43d8-9921-5b353db68104"},
            {"block_id": "7e2d49eb-ffc7-4a61-a45d-eba336d1d0e6"},
        ]

        for v in expected_path:
            v['group_id'] = "f74d1147-673c-497a-9616-763829d944ac"
            v['group_instance'] = 0

        navigator = Navigator(survey)
        routing_path = navigator.get_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_routing_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0"},
            {"block_id": "96682325-47ab-41e4-a56e-8315a19ffe2a"},
            {"block_id": "cd3b74d1-b687-4051-9634-a8f9ce10a27d"},
            {"block_id": "an3b74d1-b687-4051-9634-a8f9ce10ard"},
            {"block_id": "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"}
        ]

        for v in expected_path:
            v['group_id'] = "14ba4707-321d-441d-8d21-b8367366e766"
            v['group_instance'] = 0

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="96682325-47ab-41e4-a56e-8315a19ffe2a",
            answer_id="2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="No",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)
        routing_path = navigator.get_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_routing_basic_and_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0"},
            {"block_id": "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b"},
            {"block_id": "26f2c4b3-28ac-4072-9f18-a6a6c6f660db"},
            {"block_id": "cd3b74d1-b687-4051-9634-a8f9ce10a27d"},
            {"block_id": "an3b74d1-b687-4051-9634-a8f9ce10ard"},
            {"block_id": "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"}
        ]

        for v in expected_path:
            v['group_id'] = "14ba4707-321d-441d-8d21-b8367366e766"
            v['group_instance'] = 0

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Dark Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
            answer_id="pel989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="Can I be a pain and have a goodies ship",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)
        routing_path = navigator.get_routing_path()

        self.assertEqual(routing_path, expected_path)

    def test_get_next_location_introduction(self):
        survey = load_schema_file("0_star_wars.json")

        navigator = Navigator(survey)

        next_location = navigator.get_next_location(current_block_id='introduction')

        self.assertEqual('f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0', next_location["block_id"])

    def test_get_next_location_summary(self):
        survey = load_schema_file("0_star_wars.json")

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="96682325-47ab-41e4-a56e-8315a19ffe2a",
            answer_id="2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="No",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)

        current_block_id = 'an3b74d1-b687-4051-9634-a8f9ce10ard'

        next_location = navigator.get_next_location(current_block_id=current_block_id)
        expected_next_location = {
            "block_id": '846f8514-fed2-4bd7-8fb2-4b5fcb1622b1',
            "group_id": "14ba4707-321d-441d-8d21-b8367366e766",
            "group_instance": 0
        }

        self.assertEqual(expected_next_location, next_location)

        current_block_id = '846f8514-fed2-4bd7-8fb2-4b5fcb1622b1'
        next_location = navigator.get_next_location(current_block_id=current_block_id)
        expected_next_location = {
            "block_id": 'summary',
            "group_id": "14ba4707-321d-441d-8d21-b8367366e766",
            "group_instance": 0
        }

        self.assertEqual(expected_next_location, next_location)

    def test_get_previous_location_introduction(self):
        survey = load_schema_file("0_star_wars.json")

        navigator = Navigator(survey)

        first_block_id = 'f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0'
        next_location = navigator.get_previous_location(current_block_id=first_block_id)

        self.assertEqual('introduction', next_location['block_id'])

    def test_previous_with_conditional_path(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0"},
            {"block_id": "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b"},
            {"block_id": "26f2c4b3-28ac-4072-9f18-a6a6c6f660db"},
            {"block_id": "cd3b74d1-b687-4051-9634-a8f9ce10a27d"},
            {"block_id": "an3b74d1-b687-4051-9634-a8f9ce10ard"},
            {"block_id": "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"}
        ]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Dark Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
            answer_id="pel989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="Can I be a pain and have a goodies ship",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        current_block_id = expected_path[3]["block_id"]
        expected_previous_block = expected_path[2]

        navigator = Navigator(survey, answer_store=answers)
        actual_previous_block = navigator.get_previous_location(current_block_id=current_block_id)

        self.assertEqual(actual_previous_block["block_id"], expected_previous_block['block_id'])

        current_block_id = expected_path[2]["block_id"]
        expected_previous_block = expected_path[1]

        actual_previous_block = navigator.get_previous_location(current_block_id=current_block_id)

        self.assertEqual(actual_previous_block["block_id"], expected_previous_block['block_id'])

    def test_previous_with_conditional_path_alternative(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0"},
            {"block_id": "96682325-47ab-41e4-a56e-8315a19ffe2a"},
            {"block_id": "cd3b74d1-b687-4051-9634-a8f9ce10a27d"},
            {"block_id": "an3b74d1-b687-4051-9634-a8f9ce10ard"},
            {"block_id": "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"}
        ]

        for v in expected_path:
            v['group_id'] = "14ba4707-321d-441d-8d21-b8367366e766"
            v['group_instance'] = 0

        current_block_id = expected_path[2]["block_id"]
        expected_previous_block = expected_path[1]

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="96682325-47ab-41e4-a56e-8315a19ffe2a",
            answer_id="2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
            value="No",
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(navigator.get_previous_location(current_block_id=current_block_id), expected_previous_block)

    def test_next_location_goto_summary(self):
        survey = load_schema_file("0_star_wars.json")

        expected_path = [
            {"block_id": 'introduction'},
            {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0"},
            {"block_id": "summary"}
        ]

        for v in expected_path:
            v['group_id'] = "14ba4707-321d-441d-8d21-b8367366e766"
            v['group_instance'] = 0

        answer = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            group_instance=0,
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="I prefer Star Trek",
        )
        answers = AnswerStore()
        answers.add(answer)
        navigator = Navigator(survey, answer_store=answers)

        current_block_id = expected_path[1]["block_id"]
        expected_next_location = expected_path[2]

        next_location = navigator.get_next_location(current_block_id=current_block_id)

        self.assertEqual(next_location, expected_next_location)

    def test_next_location_empty_routing_rules(self):
        survey = load_schema_file("test_checkbox.json")

        # Force some empty routing rules
        survey['groups'][0]['blocks'][0]['routing_rules'] = []

        expected_path = [
          {"block_id": "introduction"},
          {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0"},
          {"block_id": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc1"},
          {"block_id": "summary"}
        ]

        for v in expected_path:
            v['group_id'] = "14ba4707-321d-441d-8d21-b8367366e761"
            v['group_instance'] = 0

        answer_1 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Cheese",
        )
        answer_2 = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc1",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23",
            value="deep pan",
        )
        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)

        current_block_id = expected_path[1]["block_id"]
        expected_next_location = expected_path[2]

        next_location = navigator.get_next_location(current_block_id=current_block_id)

        self.assertEqual(next_location, expected_next_location)

    def test_interstitial_post_blocks(self):
        survey = load_schema_file("0_star_wars.json")

        answer = Answer(
            group_id="14ba4707-321d-441d-8d21-b8367366e766",
            block_id="f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
            answer_id="ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
            value="Light Side"
        )
        answers = AnswerStore()
        answers.add(answer)

        navigator = Navigator(survey, answer_store=answers)

        self.assertFalse({
            'block_id': 'summary',
            "group_id": "14ba4707-321d-441d-8d21-b8367366e766",
            "group_instance": 0
        } in navigator.get_location_path())

    def test_repeating_groups(self):
        survey = load_schema_file("test_repeating_household.json")

        # Default is to count answers, so switch to using value
        survey['groups'][-1]['routing_rules'][0]['repeat']['type'] = 'answer_value'

        expected_path = [
            {
                "block_id": "household-composition",
                "group_id": "multiple-questions-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 1
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 1
            }
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="2"
        )
        answers = AnswerStore()
        answers.add(answer)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_path, navigator.get_routing_path())

    def test_should_not_show_block_for_zero_repeats(self):
        survey = load_schema_file("test_repeating_household.json")

        # Default is to count answers, so switch to using value
        survey['groups'][-1]['routing_rules'][0]['repeat']['type'] = 'answer_value'

        expected_path = [
            {
                "block_id": "household-composition",
                "group_id": "multiple-questions-group",
                'group_instance': 0
            }
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="0"
        )
        answers = AnswerStore()
        answers.add(answer)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_path, navigator.get_routing_path())

    def test_repeating_groups_no_of_answers(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            {
                "block_id": "household-composition",
                "group_id": "multiple-questions-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 1
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 1
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 2
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 2
            }
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie"
        )

        answer_3 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=2,
            answer_id="first-name",
            block_id="household-composition",
            value="Gregg"
        )

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)
        answers.add(answer_3)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_path, navigator.get_routing_path())

    def test_repeating_groups_no_of_answers_minus_one(self):
        survey = load_schema_file("test_repeating_household.json")

        # Default is to count answers, so switch to using value
        survey['groups'][-1]['routing_rules'][0]['repeat']['type'] = 'answer_count_minus_one'
        expected_path = [
            {
                "block_id": "household-composition",
                "group_id": "multiple-questions-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 0
            }
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie"
        )

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_path, navigator.get_routing_path())

    def test_repeating_groups_previous_location_introduction(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            {
                'block_id': 'introduction',
                'group_id': 'multiple-questions-group',
                'group_instance': 0
            },
            {
                "block_id": "household-composition",
                "group_id": "multiple-questions-group",
                'group_instance': 0
            }
        ]

        navigator = Navigator(survey)

        self.assertEqual(navigator.get_previous_location(current_block_id='household-composition'), expected_path[0])

    def test_repeating_groups_previous_location(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            {
                "block_id": "household-composition",
                "group_id": "multiple-questions-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 1
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 1
            }
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie Bloggs"
        )

        current_block_id = expected_path[4]["block_id"]
        current_group_id = expected_path[4]["group_id"]
        current_iteration = expected_path[4]["group_instance"]

        expected_previous_location = expected_path[3]

        answers = AnswerStore()

        answers.add(answer)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_previous_location, navigator.get_previous_location(current_group_id=current_group_id,
                                                                                     current_block_id=current_block_id,
                                                                                     current_iteration=current_iteration))

    def test_repeating_groups_next_location(self):
        survey = load_schema_file("test_repeating_household.json")

        expected_path = [
            {
                "block_id": "household-composition",
                "group_id": "multiple-questions-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 0
            },
            {
                "block_id": "repeating-block-1",
                "group_id": "repeating-group",
                'group_instance': 1
            },
            {
                "block_id": "repeating-block-2",
                "group_id": "repeating-group",
                'group_instance': 1
            }
        ]

        answer = Answer(
            group_id="multiple-questions-group",
            answer_instance=0,
            answer_id="first-name",
            block_id="household-composition",
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            answer_instance=1,
            answer_id="first-name",
            block_id="household-composition",
            value="Sophie Bloggs"
        )

        current_group_id = expected_path[-1]["group_id"]
        current_block_id = expected_path[-1]["block_id"]
        current_iteration = expected_path[-1]["group_instance"]

        answers = AnswerStore()
        answers.add(answer)
        answers.add(answer_2)

        navigator = Navigator(survey, answer_store=answers)

        summary_block = {
            "group_id": "repeating-group",
            "block_id": 'summary',
            "group_instance": 0
        }
        self.assertEqual(summary_block, navigator.get_next_location(current_group_id=current_group_id,
                                                                    current_block_id=current_block_id,
                                                                    current_iteration=current_iteration))

    def test_repeating_groups_conditional_location_path(self):
        survey = load_schema_file("test_repeating_and_conditional_routing.json")

        expected_path = [
            {
                'group_instance': 0,
                'group_id': 'repeat-value-group',
                'block_id': 'introduction'
            },
            {
                "block_id": "no-of-repeats",
                "group_id": "repeat-value-group",
                'group_instance': 0
            },
            {
                "block_id": "repeated-block",
                "group_id": "repeated-group",
                'group_instance': 0
            },
            {
                "block_id": "age-block",
                "group_id": "repeated-group",
                'group_instance': 0
            },
            {
                'block_id': 'shoe-size-block',
                'group_id': 'repeated-group',
                'group_instance': 0
            },
            {
                "block_id": "repeated-block",
                "group_id": "repeated-group",
                'group_instance': 1
            },
            {
                "block_id": "shoe-size-block",
                "group_id": "repeated-group",
                'group_instance': 1
            },
            {
                'block_id': 'summary',
                'group_id': 'repeated-group',
                'group_instance': 0
            },
            {
                'block_id': 'thank-you',
                'group_id': 'repeated-group',
                'group_instance': 0
            }
        ]

        answer_1 = Answer(
            group_id="repeat-value-group",
            block_id="no-of-repeats",
            answer_id="no-of-repeats-answer",
            value="2"
        )

        answer_2 = Answer(
            group_id="repeated-group",
            group_instance=0,
            block_id="repeated-block",
            answer_id="conditional-answer",
            value="Age and Shoe Size"
        )

        answer_3 = Answer(
            group_id="repeated-group",
            group_instance=1,
            block_id="repeated-block",
            answer_id="conditional-answer",
            value="Shoe Size Only"
        )

        answers = AnswerStore()
        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_path, navigator.get_location_path())

    def test_next_with_conditional_path_based_on_metadata(self):
        survey = load_schema_file("test_metadata_routing.json")

        expected_path = [
            {
                "block_id": "block1",
                "group_id": "group1",
                'group_instance': 0
            },
            {
                "block_id": "block3",
                "group_id": "group1",
                'group_instance': 0
            }
        ]

        current_group_id = expected_path[0]["group_id"]
        current_block_id = expected_path[0]["block_id"]
        current_iteration = expected_path[0]["group_instance"]

        expected_next_block_id = expected_path[1]

        metadata = {
            "variant_flags": {
                "flag_1": "true"
            }
        }

        navigator = Navigator(survey, metadata=metadata)

        self.assertEqual(expected_next_block_id, navigator.get_next_location(current_group_id=current_group_id,
                                                                             current_block_id=current_block_id,
                                                                             current_iteration=current_iteration))

    def test_next_with_conditional_path_when_value_not_in_metadata(self):
        survey = load_schema_file("test_metadata_routing.json")

        expected_path = [
            {
                "block_id": "block1",
                "group_id": "group1",
                'group_instance': 0
            },
            {
                "block_id": "block2",
                "group_id": "group1",
                'group_instance': 0
            }
        ]

        current_group_id = expected_path[0]["group_id"]
        current_block_id = expected_path[0]["block_id"]
        current_iteration = expected_path[0]["group_instance"]

        expected_next_block_id = expected_path[1]

        metadata = {
            "variant_flags": {
            }
        }

        navigator = Navigator(survey, metadata=metadata)

        self.assertEqual(expected_next_block_id, navigator.get_next_location(current_group_id=current_group_id,
                                                                             current_block_id=current_block_id,
                                                                             current_iteration=current_iteration))

    def test_routing_backwards_loops_to_previous_block(self):
        survey = load_schema_file("test_household_question.json")

        expected_path = [{
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'introduction'
        }, {
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'household-composition'
        }, {
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'household-summary'
        }, {
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'household-composition'
        }]

        current_group_id = expected_path[2]["group_id"]
        current_block_id = expected_path[2]["block_id"]
        current_iteration = expected_path[2]["group_instance"]

        expected_next_location = expected_path[3]

        answers = AnswerStore()

        answer_1 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=0,
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=1,
            value="Sophie Bloggs"
        )

        answer_3 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-summary",
            answer_id="household-composition-add-another",
            answer_instance=0,
            value="No"
        )

        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_next_location, navigator.get_next_location(current_group_id=current_group_id,
                                                                             current_block_id=current_block_id,
                                                                             current_iteration=current_iteration))

    def test_routing_backwards_continues_to_summary_when_complete(self):
        survey = load_schema_file("test_household_question.json")

        expected_path = [{
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'introduction'
        }, {
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'household-composition'
        }, {
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'household-summary'
        }, {
            'group_instance': 0,
            'group_id': 'multiple-questions-group',
            'block_id': 'summary'
        }]

        current_group_id = expected_path[2]["group_id"]
        current_block_id = expected_path[2]["block_id"]
        current_iteration = expected_path[2]["group_instance"]

        expected_next_location = expected_path[3]

        answers = AnswerStore()

        answer_1 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=0,
            value="Joe Bloggs"
        )

        answer_2 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-composition",
            answer_id="household-full-name",
            answer_instance=1,
            value="Sophie Bloggs"
        )

        answer_3 = Answer(
            group_id="multiple-questions-group",
            group_instance=0,
            block_id="household-summary",
            answer_id="household-composition-add-another",
            answer_instance=0,
            value="Yes"
        )

        answers.add(answer_1)
        answers.add(answer_2)
        answers.add(answer_3)

        navigator = Navigator(survey, answer_store=answers)

        self.assertEqual(expected_next_location, navigator.get_next_location(current_group_id=current_group_id,
                                                                             current_block_id=current_block_id,
                                                                             current_iteration=current_iteration))

    def test_navigation_no_blocks_completed(self):
        survey = load_schema_file("test_navigation.json")
        navigator = Navigator(survey)

        completed_blocks = []

        user_navigation = [
            {
                'link_name': 'Property Details',
                'highlight': True,
                'group_id': 'property-details',
                'instance': 0,
                'repeating': False,
                'completed': False,
                'block_id': 'insurance-type'
            },
            {
                'link_name': 'Household Details',
                'highlight': False, 'group_id':
                'multiple-questions-group',
                'instance': 0,
                'repeating': False,
                'completed': False,
                'block_id': 'household-composition'
            },
            {
                'link_name': 'Extra Cover',
                'highlight': False,
                'group_id': 'extra-cover',
                'instance': 0,
                'repeating': False,
                'completed': False,
                'block_id': 'extra-cover-block'
            },
            {
                'link_name': 'Payment Details',
                'highlight': False,
                'group_id': 'payment-details',
                'instance': 0,
                'repeating': False,
                'completed': False,
                'block_id': 'credit-card'
            }
        ]

        self.assertEqual(navigator.get_front_end_navigation(completed_blocks, 'property-details', 0), user_navigation)

    def test_non_repeating_block_completed(self):
        survey = load_schema_file("test_navigation.json")
        navigator = Navigator(survey)
        completed_blocks = [
            {
                'group_instance': 0,
                'block_id': 'introduction',
                'group_id': 'property-details'
            },
            {
                'group_instance': 0,
                'block_id': 'insurance-type',
                'group_id': 'property-details'
            },
            {
                'group_instance': 0,
                'block_id': 'insurance-address',
                'group_id': 'property-details'
            },
            {
                'group_instance': 0,
                'block_id': 'property-interstitial',
                'group_id': 'property-details'
            }
        ]

        user_navigation = [
            {
                'completed': True,
                'link_name': 'Property Details',
                'block_id': 'insurance-type',
                'group_id': 'property-details',
                'highlight': True,
                'instance': 0,
                'repeating': False
             },
            {
                'completed': False,
                'link_name': 'Household Details',
                'block_id': 'household-composition',
                'group_id': 'multiple-questions-group',
                'highlight': False, 'instance': 0,
                'repeating': False
            },
            {
                'completed': False,
                'link_name': 'Extra Cover',
                'block_id': 'extra-cover-block',
                'group_id': 'extra-cover',
                'highlight': False,
                'instance': 0,
                'repeating': False
            },
            {
                'completed': False,
                'link_name': 'Payment Details',
                'block_id': 'credit-card',
                'group_id': 'payment-details',
                'highlight': False,
                'instance': 0,
                'repeating': False
            }
        ]
        self.assertEqual(navigator.get_front_end_navigation(completed_blocks, 'property-details', 0), user_navigation)

    def test_navigation_repeating_household_and_hidden_household_groups_completed(self):
        survey = load_schema_file("test_navigation.json")
        navigator = Navigator(survey)
        navigator.answer_store.answers = [
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'household-full-name',
                'value': 'Jim',
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'group_instance': 0,
                'answer_instance': 1,
                'answer_id': 'household-full-name',
                'value': 'Ben',
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 0,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-age',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 1,
                'answer_instance': 0,
                'answer_id': 'what-is-your-shoe-size',
                'value': None,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
            }
        ]
        completed_blocks = [
            {
                'group_instance': 0,
                'group_id': 'property-details',
                'block_id': 'introduction'
            },
            {
                'group_instance': 0,
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'group_instance': 0,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 0,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
            },
            {
                'group_instance': 1,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'group_instance': 1,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-2'
            }
        ]
        user_navigation = [
            {
                'link_name': 'Property Details',
                'repeating': False,
                'instance': 0,
                'completed': False,
                'highlight': True,
                'group_id': 'property-details',
                'block_id': 'insurance-type'
            },
            {
                'link_name': 'Household Details',
                'repeating': False,
                'instance': 0,
                'completed': True,
                'highlight': False,
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            },
            {
                'link_name': 'Jim',
                'repeating': True,
                'instance': 0,
                'completed': True,
                'highlight': False,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'link_name': 'Ben',
                'repeating': True,
                'instance': 1,
                'completed': True,
                'highlight': False,
                'group_id': 'repeating-group',
                'block_id': 'repeating-block-1'
            },
            {
                'link_name': 'Extra Cover',
                'repeating': False,
                'instance': 0,
                'completed': False,
                'highlight': False,
                'group_id': 'extra-cover',
                'block_id': 'extra-cover-block'
            },
            {
                'link_name': 'Payment Details',
                'repeating': False,
                'instance': 0,
                'completed': False,
                'highlight': False,
                'group_id': 'payment-details',
                'block_id': 'credit-card'
            }
        ]

        self.assertEqual(navigator.get_front_end_navigation(completed_blocks, 'property-details', 0), user_navigation)

    def test_navigation_repeating_group_extra_answered_not_completed(self):
        survey = load_schema_file("test_navigation.json")
        navigator = Navigator(survey)

        navigator.answer_store.answers = [
            {
                'answer_instance': 0,
                'group_id': 'multiple-questions-group',
                'answer_id': 'household-full-name',
                'block_id': 'household-composition',
                'group_instance': 0,
                'value': 'Person1'
            },
            {
                'answer_instance': 1,
                'group_id': 'multiple-questions-group',
                'answer_id': 'household-full-name',
                'block_id': 'household-composition',
                'group_instance': 0,
                'value': 'Person2'
            },
            {
                'answer_instance': 1,
                'group_id': 'extra-cover',
                'answer_id': 'extra-cover-answer',
                'block_id': 'extra-cover-block',
                'group_instance': 0,
                'value': 2
            }
        ]

        completed_blocks = [
            {
                'block_id': 'introduction',
                'group_instance': 0,
                'group_id': 'property-details'
            },
            {
                'block_id': 'insurance-type',
                'group_instance': 0,
                'group_id': 'property-details'
            },
            {
                'block_id': 'cd6a5727-8cab-4737-aa4e-d666d98b3f92',
                'group_instance': 0,
                'group_id': 'property-details'
            },
            {
                'block_id': 'personal-interstitial',
                'group_instance': 0,
                'group_id': 'property-details'
            },
            {
                'block_id': 'extra-cover-block',
                'group_instance': 0,
                'group_id': 'extra-cover'
            },
            {
                'block_id': 'ea651fa7-6b9d-4b6f-ba72-79133f312039',
                'group_instance': 0,
                'group_id': 'extra-cover'
            }
        ]

        user_navigation = [
            {
                'completed': False,
                'group_id': 'property-details',
                'highlight': True,
                'block_id': 'insurance-type',
                'repeating': False,
                'instance': 0,
                'link_name': 'Property Details'
            },
            {
                'completed': False,
                'group_id': 'multiple-questions-group',
                'highlight': False,
                'block_id': 'household-composition',
                'repeating': False,
                'instance': 0,
                'link_name': 'Household Details'
            },
            {
                'completed': False,
                'group_id': 'repeating-group',
                'highlight': False,
                'block_id': 'repeating-block-1',
                'repeating': True,
                'instance': 0,
                'link_name': 'Person1'
            },
            {
                'completed': False,
                'group_id': 'repeating-group',
                'highlight': False,
                'block_id': 'repeating-block-1',
                'repeating': True,
                'instance': 1,
                'link_name': 'Person2'
            },
            {
                'completed': False,
                'group_id': 'extra-cover',
                'highlight': False,
                'block_id': 'extra-cover-block',
                'repeating': False,
                'instance': 0,
                'link_name': 'Extra Cover'
            },
            {
                'completed': False,
                'group_id': 'payment-details',
                'highlight': False,
                'block_id': 'credit-card',
                'repeating': False,
                'instance': 0,
                'link_name': 'Payment Details'
            },
            {
                'completed': False,
                'group_id': 'extra-cover-items-group',
                'highlight': False,
                'block_id': 'extra-cover-items',
                'repeating': False,
                'instance': 0,
                'link_name': 'Extra Cover Items'
            }
        ]

        self.assertEqual(navigator.get_front_end_navigation(completed_blocks, 'property-details', 0), user_navigation)

    def test_navigation_repeating_group_extra_answered_completed(self):
        survey = load_schema_file("test_navigation.json")
        navigator = Navigator(survey)

        navigator.answer_store.answers = [
            {
                'value': 2,
                'group_instance': 0,
                'block_id': 'extra-cover-block',
                'group_id': 'extra-cover',
                'answer_instance': 0,
                'answer_id': 'extra-cover-answer'
            },
            {
                'value': '2',
                'group_instance': 0,
                'block_id': 'extra-cover-items',
                'group_id': 'extra-cover-items-group',
                'answer_instance': 0,
                'answer_id': 'extra-cover-items-answer'
            },
            {
                'value': '2',
                'group_instance': 1,
                'block_id': 'extra-cover-items',
                'group_id': 'extra-cover-items-group',
                'answer_id': 'extra-cover-items-answer',
                'answer_instance': 0
            }
        ]

        completed_blocks = [
            {
                'block_id': 'introduction',
                'group_id': 'property-details',
                'group_instance': 0
            },
            {
                'block_id': 'extra-cover-block',
                'group_instance': 0,
                'group_id': 'extra-cover'
            },
            {
                'group_id': 'extra-cover',
                'group_instance': 0,
                'block_id': 'extra-cover-interstitial'
            },
            {
                'block_id': 'extra-cover-items',
                'group_instance': 0,
                'group_id': 'extra-cover-items-group'
            },
            {
                'group_id': 'extra-cover-items-group',
                'group_instance': 1,
                'block_id': 'extra-cover-items'
            }
        ]
        user_navigation = [
            {
                'group_id': 'property-details',
                'repeating': False,
                'highlight': True,
                'link_name': 'Property Details',
                'instance': 0,
                'block_id': 'insurance-type',
                'completed': False
            },
            {
                'group_id': 'multiple-questions-group',
                'repeating': False,
                'highlight': False,
                'link_name': 'Household Details',
                'instance': 0,
                'block_id': 'household-composition',
                'completed': False
            },
            {
                'group_id': 'extra-cover',
                'repeating': False,
                'highlight': False,
                'link_name': 'Extra Cover',
                'instance': 0,
                'block_id': 'extra-cover-block',
                'completed': True
            },
            {
                'group_id': 'payment-details',
                'repeating': False,
                'highlight': False,
                'link_name': 'Payment Details',
                'instance': 0,
                'block_id': 'credit-card',
                'completed': False
            },
            {
                'group_id': 'extra-cover-items-group',
                'repeating': False,
                'highlight': False,
                'link_name': 'Extra Cover Items',
                'instance': 0,
                'block_id': 'extra-cover-items',
                'completed': True
            }
        ]

        self.assertEqual(navigator.get_front_end_navigation(completed_blocks, 'property-details', 0), user_navigation)

    def test_navigation_repeating_group_link_name_format(self):
        survey = load_schema_file("test_repeating_household.json")
        navigator = Navigator(survey)

        navigator.answer_store.answers = [
            {
                'block_id': 'household-composition',
                'answer_instance': 0,
                'answer_id': 'first-name',
                'group_id': 'multiple-questions-group',
                'group_instance': 0,
                'value': 'Joe'
            },
            {
                'block_id': 'household-composition',
                'answer_instance': 0,
                'answer_id': 'middle-names',
                'group_id': 'multiple-questions-group',
                'group_instance': 0,
                'value': None
            },
            {
                'block_id': 'household-composition',
                'answer_instance': 0,
                'answer_id': 'last-name',
                'group_id': 'multiple-questions-group',
                'group_instance': 0,
                'value': 'Bloggs'
            },
            {
                'block_id': 'household-composition',
                'answer_instance': 1,
                'answer_id': 'first-name',
                'group_id': 'multiple-questions-group',
                'group_instance': 0,
                'value': 'Jim'
            },
            {
                'block_id': 'household-composition',
                'answer_instance': 1,
                'answer_id': 'last-name',
                'group_id': 'multiple-questions-group',
                'group_instance': 0,
                'value': None
            },
            {
                'block_id': 'household-composition',
                'answer_instance': 1,
                'answer_id': 'middle-names',
                'group_id': 'multiple-questions-group',
                'group_instance': 0,
                'value': None
            }
        ]

        completed_blocks = [
            {
                'group_instance': 0,
                'group_id': 'multiple-questions-group',
                'block_id': 'introduction'
            },
            {
                'group_instance': 0,
                'group_id': 'multiple-questions-group',
                'block_id': 'household-composition'
            }
        ]

        user_navigation = [
            {
                'repeating': False,
                'link_name': '',
                'instance': 0,
                'block_id': 'household-composition',
                'completed': True,
                'highlight': False,
                'group_id': 'multiple-questions-group'
            },
            {
                'repeating': True,
                'link_name': 'Joe Bloggs',
                'instance': 0,
                'block_id': 'repeating-block-1',
                'completed': False,
                'highlight': False,
                'group_id': 'repeating-group'
            },
            {
                'repeating': True,
                'link_name': 'Jim',
                'instance': 1,
                'block_id': 'repeating-block-1',
                'completed': False,
                'highlight': False,
                'group_id': 'repeating-group'
            }
        ]

        self.assertEqual(navigator.get_front_end_navigation(completed_blocks, 'property-details', 0), user_navigation)

    def test_block_index_for_location_with_invalid_location(self):
        blocks = [
            {
                "group_id": 'first-valid-group-id',
                "group_instance": 0,
                "block": {"id": 'first-valid-block-id'}
            },
            {
                "group_id": 'second-valid-group-id',
                "group_instance": 0,
                "block": {"id": 'second-valid-block-id'}
            }
        ]

        invalid_group_location = {
            'group_instance': 0,
            'group_id': 'this-group-id-doesnt-exist-in-the-list-of-blocks',
            'block_id': 'first-valid-block-id'
        }

        with self.assertRaises(StopIteration):
            Navigator._block_index_for_location(blocks, invalid_group_location)

        invalid_block_location = {
            'group_instance': 0,
            'group_id': 'second-valid-group-id',
            'block_id': 'this-block-id-doesnt-exist-in-the-list-of-blocks'
        }

        with self.assertRaises(StopIteration):
            Navigator._block_index_for_location(blocks, invalid_block_location)
