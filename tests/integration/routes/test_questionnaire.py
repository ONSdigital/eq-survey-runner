import simplejson as json
from mock import Mock

from app.data_model.questionnaire_store import QuestionnaireStore
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

