from tests.integration.integration_test_case import IntegrationTestCase
from tests.integration.create_token import create_token
import re
from werkzeug.datastructures import MultiDict, ImmutableMultiDict
from bs4 import BeautifulSoup


class RoutingTestCase(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self._form_data = MultiDict()
        self._summary = MultiDict()
        self._content = None
        self._status_code = None

    def assertUrlEndsWith(self, ending):
        if not self._current_url.endswith(ending):
            raise AssertionError('Current URL {} does not end with {}'.format(self._current_url, ending))

    def login(self, token):
        resp = self.client.get('/session?token=' + token.decode(), follow_redirects=False)
        self._status_code = resp.status_code
        self.assertEquals(resp.status_code, 302)
        self._current_url = resp.headers['Location']
        self.load_current_url()

    def load_current_url(self):
        resp = self.client.get(self._current_url, follow_redirects=True)
        self.assertEquals(resp.status_code, 200)
        self._current_location = self._current_url.split('/').pop()
        self._content = BeautifulSoup(resp.get_data(True), 'html.parser')
        self._form_data.clear()

    def click_button(self, label):
        buttons = self._content.find_all('button')
        for button in buttons:
            if button.string == label:
                self._form_data.add(button['name'], label)
                self.submit_form()
                return

        raise AssertionError("Could not find button \"{}\"".format(label))

    def get_input_fields(self):
        fields = {}
        inputs = self._content.find_all('input')
        for field in inputs:
            if 'type' not in field.attrs:
                # Assume 'text'
                if field['name'] not in fields.keys():
                    fields[field['name']] = field['value']

            elif field['type'] != 'submit' and field['type'] != 'button':
                if field['name'] not in fields.keys():
                    fields[field['name']] = field['value']

        textareas = self._content.find_all('textarea')
        for textarea in textareas:
            if textarea['name'] not in fields.keys():
                fields[textarea['name']] = textarea.string

        selects = self._content.find_all('select')
        for select in selects:
            if select['name'] not in fields.keys():
                fields[select['name']] = select.value or ''

        return fields

    def get_summary_items(self):
        items = {}

        tags = self._content.select("dd a")
        for tag in tags:
            item_id = tag.attrs['href'].split('#')[1]
            items[item_id] = tag.string

        return items

    def go_to_location(self, location):
        base_url = self._current_url.split('/')
        base_url.pop()
        self.go_to_url('/'.join(base_url) + '/' + location)

    def go_to_url(self, url):
        self._current_url = url
        self.load_current_url()

    def submit_form(self):
        if self._current_url.startswith('http://localhost'):
            self._current_url = self._current_url[16:]  # Make it relative, bug in flask client?

        # POST the curent form_data
        post_data = ImmutableMultiDict(self._form_data)
        resp = self.client.post(self._current_url, data=post_data, follow_redirects=False)
        self._form_data.clear()
        self.assertEquals(resp.status_code, 302)

        # Follow the redirect
        self._current_url = resp.headers['Location']
        self.load_current_url()


    def get_all_routing_rules(self):
        '''
        This method would inspect a schema and collect all the routing rules...
        For now, it is hard coded
        '''
        routing_rules = [
            (
                "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",             # Source block
                (
                    "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",         # item
                    "equals",                                       # test
                    "Light Side"                                    # value
                ),
                "96682325-47ab-41e4-a56e-8315a19ffe2a"              # target
            ),
            (
                "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
                (
                    "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
                    "equals",
                    "Dark Side"
                ),
                "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b"
            ),
            (
                "f22b1ba4-d15f-48b8-a1f3-db62b6f34cc0",
                (
                    "ca3ce3a3-ae44-4e30-8f85-5b6a7a2fb23c",
                    "equals",
                    "I prefer Star Trek"
                ),
                "summary"
            ),
            (
                "96682325-47ab-41e4-a56e-8315a19ffe2a",
                (
                    "2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
                    "equals",
                    "Yes"
                ),
                "26f2c4b3-28ac-4072-9f18-a6a6c6f660db"
            ),
            (
                "96682325-47ab-41e4-a56e-8315a19ffe2a",
                (
                    "2e0989b8-5185-4ba6-b73f-c126e3a06ba7",
                    "equals",
                    "No"
                ),
                "66cd681c-c3cb-4e32-8d51-b98337a6b524"
            ),
            (
                "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
                (
                    "pel989b8-5185-4ba6-b73f-c126e3a06ba7",
                    "equals",
                    "Yes"
                ),
                "5ff0d900-530d-4266-8bed-c3d1f11b8d8c"
            ),
            (
                "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
                (
                    "pel989b8-5185-4ba6-b73f-c126e3a06ba7",
                    "equals",
                    "No"
                ),
                "66cd681c-c3cb-4e32-8d51-b98337a6b524"
            ),
            (
                "923ccc84-9d47-4a02-8ebc-1e9d14fcf10b",
                (
                    "pel989b8-5185-4ba6-b73f-c126e3a06ba7",
                    "equals",
                    "Can I be a pain and have a goodies ship"
                ),
                "26f2c4b3-28ac-4072-9f18-a6a6c6f660db"
            ),
            (
                "5ff0d900-530d-4266-8bed-c3d1f11b8d8c",
                True,
                "fab02f02-6ce4-4f22-b61f-0c7880009f08_1"
            ),
            (
                "26f2c4b3-28ac-4072-9f18-a6a6c6f660db",
                True,
                "66cd681c-c3cb-4e32-8d51-b98337a6b524"
            ),
            (
                "fab02f02-6ce4-4f22-b61f-0c7880009f08_1",
                (
                    "repeat",
                    "50dd83c9-8de6-4c3b-be24-e85dd290b855"      # No of repetitions
                ),
                "cd3b74d1-b687-4051-9634-a8f9ce10a27d"
            ),
            (
                "66cd681c-c3cb-4e32-8d51-b98337a6b524",
                (
                    "8fe76762-d07f-4a1f-a315-0b0385940f8c",
                    "not equals",
                    "0"
                ),
                "73ca315e-cab0-4b19-a79b-f850884db9e5_1"
            ),
            (
                "66cd681c-c3cb-4e32-8d51-b98337a6b524",
                (
                    "8fe76762-d07f-4a1f-a315-0b0385940f8c",
                    "equals",
                    "0"
                ),
                "cd3b74d1-b687-4051-9634-a8f9ce10a27d"
            ),
            (
                "73ca315e-cab0-4b19-a79b-f850884db9e5_1",
                (
                    "repeat",
                    "8fe76762-d07f-4a1f-a315-0b0385940f8c"
                ),
                "cd3b74d1-b687-4051-9634-a8f9ce10a27d"          # Implied by schema
            ),
            # These final routes are also implied
            (
                "cd3b74d1-b687-4051-9634-a8f9ce10a27d",
                True,
                "an3b74d1-b687-4051-9634-a8f9ce10ard"
            ),
            (
                "an3b74d1-b687-4051-9634-a8f9ce10ard",
                True,
                "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1"
            ),
            (
                "846f8514-fed2-4bd7-8fb2-4b5fcb1622b1",
                True,
                "summary"
            )
        ]
        return routing_rules

    def get_answers(self):
        answers = {
            "CHOOSE_A_SIDE": [
              'Light Side',
              'Dark Side',
              'I prefer Star Trek'
            ],
            "CHOOSE_A_HERO": [
              'Dan Skywalker',
              'Hans Solarren',
              'Leyoda',
              'Davewbacca'
            ],
            "PICK_A_GOOD_SHIP": [
                'Yes',
                'No'
            ],
            "PICK_A_BADDIE": [
              'Darth Vadan',
              'Jabba the Hutarren',
              'Boba Fetewis',
              'Count Davidu'
            ],
            "PICK_A_BAD_SHIP": [
              'Yes',
              'No',
              'Can I be a pain and have a goodies ship'
            ],
            "HOW_MANY_SHIPS": [
              '1',
              '2'
            ],
            "CHOOSE_A_GOOD_SHIP": [
              'Millennium Falcon',
              'X-Wing'
            ],
            "CHOOSE_A_BAD_SHIP": [
              'TIE Fighter',
              'Death Star'
            ],
            "HOW_MANY_CRAWLERS": [
              '0',
              '1',
              '2'
            ],
            "CRAWLER_DESCRIPTION_1": 'Crawler One',
            "CRAWLER_DESCRIPTION_2": 'Crawler Two',
            "WHICH_SPECIES": [
              'Klingons',
              'Bothans'
            ],
            "CHEWIES_AGE": '234',
            "DEATH_STAR_COST": "40",
            "LIGHTSABRE_TEMP": '1370',
            "TIE_FIGTHER_ANIMAL": "Elephant",
            "WRONG_QUOTE": "Luke, I am your father",
            "GREEN_LIGHTSABRE": [
              [
                "Luke Skywalker", "Yoda", "Qui-Gon Jinn"
              ]
            ],
            "CRAWLER_APPEARANCE": [
              [
                "Luke Skywalker", "The Emperor", "Senator Amidala"
              ]
            ],
            "EMPIRE_RELEASE_START_DAY": '28',
            "EMPIRE_RELEASE_START_MONTH": '05',
            "EMPIRE_RELEASE_START_YEAR": '1983',
            "EMPIRE_RELEASE_END_DAY": '29',
            "EMPIRE_RELEASE_END_MONTH": '05',
            "EMPIRE_RELEASE_END_YEAR": '1983',
            "TOTAL_EWOKS": "77",
            "WHAT_ELSE_STOLEN": "Shield Generator Codes",
            "NO_CHEWIE_MEDAL": "Wookies aren't materialistic",
            "CONFIRM_CHEWIES_AGE": "Yes",
            "EPISODES_1_TO_3": [
              "Awesome, I love them all",
              "I like to pretend they didn't happen"
            ],
            "BINKS_HOME_PLANET": "Naboo",
            "FAVOURITE_FILM": "5"
        }
        return answers
