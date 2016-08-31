from tests.integration.routing.routing_test_case import RoutingTestCase
from tests.integration.create_token import create_token
from werkzeug.datastructures import MultiDict
import random


answer_codes = {
    "CHOOSE_A_SIDE": "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
    "CHOOSE_A_HERO": "91631df0-4356-4e9f-a9d9-ce8b08d26eb3",
    "PICK_A_GOOD_SHIP": "2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
    "PICK_A_BADDIE": "653e6407-43d6-4dfc-8b11-a673a73d602d",
    "PICK_A_BAD_SHIP": "pel989b8-5185-4ba6-b73f-c126e3a06ba7",
    "HOW_MANY_SHIPS": "50dd83c9-8de6-4c3b-be24-e85dd290b855",
    "CHOOSE_A_GOOD_SHIP": "a2c2649a-85ff-4a26-ba3c-e1880f7c807b",
    "CHOOSE_A_BAD_SHIP": "a5d5ca1a-cf58-4626-be35-dce81297688b_1",
    "HOW_MANY_CRAWLERS": "8fe76762-d07f-4a1f-a315-0b0385940f8c",
    "CRAWLER_DESCRIPTION_1": "56b6f367-e84b-43fa-a5e2-19193f223fa0_1",
    "CRAWLER_DESCRIPTION_2": "56b6f367-e84b-43fa-a5e2-19193f223fa0_2",
    "WHICH_SPECIES": "cccfe681-9969-4175-8ac3-98184ab58423",
    "CHEWIES_AGE": "6cf5c72a-c1bf-4d0c-af6c-d0f07bc5b65b",
    "DEATH_STAR_COST": "92e49d93-cbdc-4bcb-adb2-0e0af6c9a07c",
    "LIGHTSABRE_TEMP": "pre49d93-cbdc-4bcb-adb2-0e0af6c9a07c",
    "TIE_FIGTHER_ANIMAL": "a5dc09e8-36f2-4bf4-97be-c9e6ca8cbe0d",
    "WRONG_QUOTE": "7587eb9b-f24e-4dc0-ac94-66118b896c10",
    "GREEN_LIGHTSABRE": "9587eb9b-f24e-4dc0-ac94-66117b896c10",
    "CRAWLER_APPEARANCE": "5587eb9b-f24e-4dc0-ac94-66117b896c10",
    "EMPIRE_RELEASE_START_DAY": "6fd644b0-798e-4a58-a393-a438b32fe637-day",
    "EMPIRE_RELEASE_START_MONTH": "6fd644b0-798e-4a58-a393-a438b32fe637-month",
    "EMPIRE_RELEASE_START_YEAR": "6fd644b0-798e-4a58-a393-a438b32fe637-year",
    "EMPIRE_RELEASE_END_DAY": "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-day",
    "EMPIRE_RELEASE_END_MONTH": "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-month",
    "EMPIRE_RELEASE_END_YEAR": "06a6a4b7-6ce4-4687-879d-3443cd8e2ff0-year",
    "TOTAL_EWOKS": "5rr015b1-f87c-4740-9fd4-f01f707ef558",
    "WHAT_ELSE_STOLEN": "c8d9d66e-6c0a-439e-8ef9-e0d7038be009",
    "NO_CHEWIE_MEDAL": "215015b1-f87c-4740-9fd4-f01f707ef558",
    "CONFIRM_CHEWIES_AGE": "7587qe9b-f24e-4dc0-ac94-66118b896c10",
    "EPISODES_1_TO_3": "77e20f0e-cabb-4eac-8cb0-ac6e66f0e95f",
    "BINKS_HOME_PLANET": "fcf636ff-7b3d-47b6-aaff-9a4b00aa888b",
    "FAVOURITE_FILM": "4a085fe5-6830-4ef6-96e6-2ea2b3caf0c1"
}

# Create the inverse
answer_names = {v: k for k, v in answer_codes.items()}

blocks = {
    "CHOOSE_A_SIDE": "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
    "CHOOSE_A_HERO": "96682325-47ab-41e4-a56e-8315a19ffe2a",
    "CHOOSE_A_BADDIE": "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
    "HOW_MANY_SHIPS": "5ff0d900-530d-4266-8bed-c3d1f11b8d8c",
    "CHOOSE_A_GOOD_SHIP": "26f2c4b3-28ac-4072-9f18-a6a6c6f660db",
    "CHOOSE_A_BAD_SHIP": "fab02f02-6ce4-4f22-b61f-0c7880009f08_1",
    "HOW_MANY_CRAWLERS": "66cd681c-c3cb-4e32-8d51-b98337a6b524",
    "DESCRIBE_CRAWLER": "73ca315e-cab0-4b19-a79b-f850884db9e5_1",
    "PAGE_ONE_QUESTIONS": "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
    "PAGE_TWO_QUESTIONS": "an3b74d1-b687-4051-9634-a8f9ce10ard",
    "PAGE_THREE_QUESTIONS": "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
}


class TestRouting(RoutingTestCase):
    def setUp(self):
        super().setUp()
        self.stack = []
        self.answers = self.get_answers()
        self.rules = self.get_all_routing_rules()


    def test_routing(self):
        self.login(create_token('star_wars', '0'))
        self.assertUrlEndsWith('introduction')
        self.click_button('Get Started')
        self.assertUrlEndsWith(blocks['CHOOSE_A_SIDE'])

        # while current url not ends with summary
            # get rules for current URL
            # pick first rule and add remaining rules to stack
            # fill in the form using the rule
            # click submit
            # check the current url matches that specified by the url


        while len(self.rules) > 0:
            while not self._current_url.endswith('summary'):
                rule = self.get_rule(self._current_location)

                self._fill_form(rule)

                # Store the location
                self.stack.append({
                    'location': self._current_location,
                    'form_data': MultiDict(self._form_data)
                })

                self.click_button('Save & Continue')

                if rule:
                    self.assertUrlEndsWith(rule[2])

            # We are now on the summary screen
            self._check_summary_screen()

            self.rewind_and_route()

    def _check_summary_screen(self):
        self.assertUrlEndsWith('summary')

        submitted = self.get_submitted_answers()
        cleaned = MultiDict()
        items = self.get_summary_items()

        import pdb
        pdb.set_trace()

        # group the dates
        for code, value in submitted.items():
            if code.endswith('-day'):
                item_id = code[:-4]
                self.assertIn(item_id + '-month', submitted.keys())
                self.assertIn(item_id + '-year', submitted.keys())

                cleaned.add(item_id, str(value) + '/' + submitted[item_id + '-month'] + '/' + submitted[item_id + '-year'])

            elif code.endswith('-month') or code.endswith('-year'):
                pass  # ignore them, they are handled above
            else:
                cleaned.add(code, value)

        # check the items
        for code, value in cleaned.items():
            self.assertIn(code, items.keys())
            # self.assertRegexpMatches(items[code], value)

    def get_submitted_answers(self):
        submitted = MultiDict()
        for page in self.stack:
            submitted.update(page['form_data'])
        return submitted

    def rewind_and_route(self):
        if len(self.stack) > 0:
            previous = self.stack.pop()
            if self.has_rules(previous['location']):
                self.go_to_location(previous['location'])
            else:
                self.rewind_and_route()

    def _fill_form(self, rule):
        fields = self.get_input_fields()
        skip_field = None
        if isinstance(rule, tuple):
            if len(rule) == 3:
                condition = rule[1]
                if isinstance(condition, tuple) and len(condition) == 3:
                    if condition[1] == 'equals':
                        skip_field = condition[0]
                        self._form_data.add(condition[0], condition[2])
                        self.remove_answer(condition[0], condition[2])
                    elif condition[1] == 'not equals':
                        skip_field = condition[0]
                        self._form_data.add(condition[0], self.choose_other_answer(condition[0], condition[2]))

        for code, answer in fields.items():
            if code != skip_field:
                self._form_data.add(code, self.choose_next_answer(code))

    def generate_random_int(self, lowest, highest, exclude):
        number = random.randrange(lowest, highest)
        if number == exclude:
            return self.generate_random_int(lowest, highest, exclude)
        return number

    def choose_other_answer(self, code, value):
        answer_name = answer_names[code]
        possible_answers = self.answers[answer_name]

        if isinstance(possible_answers, list):
            for possible in possible_answers:
                if possible != value:
                    return possible
            return possible_answers[0]
        else:
            return self.generate_random_int(1, 20, value)

    def choose_next_answer(self, answer_code):
        answer_name = answer_names[answer_code]
        possible_answers = self.answers[answer_name]

        if isinstance(possible_answers, list):
            if len(possible_answers) > 1:
                answer = possible_answers.pop(0)  # Take the first
            else:
                answer = possible_answers[0]
            return answer
        else:
            return possible_answers

    def remove_answer(self, answer_code, answer_value):
        answer_name = answer_names[answer_code]
        if answer_value in self.answers[answer_name] and len(self.answers[answer_name]) > 1:
            self.answers[answer_name].remove(answer_value)

    def get_rule(self, item_id):
        for rule in self.rules:
            if rule[0] == item_id:
                self.rules.remove(rule)
                return rule
        return None

    def has_rules(self, item_id):
        for rule in self.rules:
            if rule[0] == item_id:
                return True
        return False
