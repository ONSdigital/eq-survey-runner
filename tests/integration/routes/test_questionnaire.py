import simplejson as json
from mock import Mock

from app.data_model.questionnaire_store import QuestionnaireStore
from app.questionnaire.location import Location
from app.utilities.schema import load_schema_from_name
from app.routes.questionnaire import get_page_title_for_location
from tests.integration.integration_test_case import IntegrationTestCase


class TestQuestionnaire(IntegrationTestCase):
    def setUp(self):
        super().setUp()
        self._application_context = self._application.app_context()
        self._application_context.push()

        storage = Mock()
        data = {'METADATA': 'test', 'ANSWERS': [], 'PROGRESS': []}
        storage.get_user_data = Mock(
            return_value=(json.dumps(data), QuestionnaireStore.LATEST_VERSION)
        )

        self.question_store = QuestionnaireStore(storage)
        self.mock_context = {'block': {'question': {'title': 'Testing title'}}}

    def tearDown(self):
        self._application_context.pop()

    def test_given_introduction_page_when_get_page_title_then_defaults_to_survey_title(
        self
    ):
        # Given
        schema = load_schema_from_name('test_final_confirmation')

        # When
        page_title = get_page_title_for_location(
            schema,
            Location(section_id='first-group', block_id='introduction'),
            self.mock_context,
        )

        # Then
        self.assertEqual(page_title, 'Final confirmation to submit')

    def test_given_interstitial_page_when_get_page_title_then_group_title_and_survey_title(
        self
    ):
        # Given
        schema = load_schema_from_name('test_interstitial_page')

        # When
        page_title = get_page_title_for_location(
            schema,
            Location(section_id='default-section', block_id='breakfast-interstitial'),
            self.mock_context,
        )

        # Then
        self.assertEqual(page_title, 'Favourite food - Interstitial Pages')

    def test_given_questionnaire_page_when_get_page_title_then_question_title_and_survey_title(
        self
    ):
        # Given
        schema = load_schema_from_name('test_final_confirmation')

        # When
        page_title = get_page_title_for_location(
            schema,
            Location(section_id='first-group', block_id='breakfast'),
            self.mock_context,
        )

        # Then
        self.assertEqual(page_title, 'Testing title - Final confirmation to submit')
