from flask_babel import gettext

from app import create_app
from app.questionnaire_state.state_answer import StateAnswer
from app.schema.answer import Answer
from app.schema.widgets.relationship_widget import RelationshipWidget
from tests.integration.integration_test_case import IntegrationTestCase


class TestRenderRelationshipWidget(IntegrationTestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()

    def tearDown(self):
        self.app_context.pop()

    def test_render_widget_should_contain_current_person(self):
        with self.app.test_request_context():
            # Given
            widget = RelationshipWidget('relationship')
            widget.current_person = 'Joe Bloggs'
            answer = Answer()
            answer.label = '%(current_person)s is the &hellip; of %(other_person)s'
            answer.options = [{'label': 'Husband or wife', 'value': 'Husband or wife'},
                              {'label': 'Son or daughter', 'value': 'Son or daughter'}]
            state_answer = StateAnswer('who-related', answer)
            state_answer.input = 'Husband or wife'

            # When
            rendered = widget.render(state_answer)

            # Then
            self.assertRegex(rendered, 'Joe Bloggs is the ')

    def test_render_widget_should_contain_other_person(self):
        with self.app.test_request_context():
            # Given
            widget = RelationshipWidget('relationship')
            widget.other_person = 'Jane Doe'
            answer = Answer()
            answer.label = '%(current_person)s is the &hellip; of %(other_person)s'
            answer.options = [{'label': 'Husband or wife', 'value': 'Husband or wife'},
                              {'label': 'Son or daughter', 'value': 'Son or daughter'}]
            state_answer = StateAnswer('who-related', answer)
            state_answer.input = 'Husband or wife'

            # When
            rendered = widget.render(state_answer)

            # Then
            self.assertRegex(rendered, 'of Jane Doe')
