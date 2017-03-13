from tests.integration.integration_test_case import IntegrationTestCase


class StarWarsTestCase(IntegrationTestCase):

    def launchSurvey(self, eq_id='0', form_type_id='star_wars'):
        super().launchSurvey(eq_id, form_type_id)

    def start_questionnaire_and_navigate_routing(self):
        self.post(action='start_questionnaire')
        self.assertStatusOK()
        return self._default_routing()

    def _default_routing(self):
        self.post({'choose-your-side-answer': 'Light Side'})
        self.routing_pick_your_character_light_side()

        self.post({
            'light-side-pick-character-answer': 'Leyoda',
            'light-side-pick-ship-answer': 'Yes'
        })
        self.routing_select_your_ship_light_side()

        self.post({'light-side-ship-type-answer': 'Millennium Falcon'})

    def routing_pick_your_character_light_side(self):
        self.assertInPage('A wise choice young Jedi. Pick your hero')
        self.assertInPage('light-side-pick-character-answer')
        self.assertInPage('Do you want to pick a ship?')
        self.assertInPage('light-side-pick-ship-answer')

    def routing_select_your_ship_light_side(self):
        self.assertInPage('Which ship do you want?')
        self.assertInPage('Millennium Falcon')
        self.assertInPage('X-wing')
        self.assertInPage('light-side-ship-type-answer')

    def check_second_quiz_page(self):
        # Pipe Test for section title
        self.assertInPage('On 2 June 1983 how many were employed?')

        # Textarea question
        self.assertInPage('Why doesn\'t Chewbacca receive a medal at the end of A New Hope?')
        self.assertInPage('chewbacca-medal-answer')
