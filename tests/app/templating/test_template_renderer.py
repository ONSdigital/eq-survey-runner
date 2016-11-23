import unittest
from datetime import datetime

from app.questionnaire_state.state_question import StateQuestion
from app.schema.question import Question
from app.templating.template_renderer import TemplateRenderer


class TestTemplateRenderer(unittest.TestCase):

    def test_render_state_item(self):
        question = Question()
        question.title = 'Hello {{name}}'
        question.templatable_properties = ['title']
        state = StateQuestion('id', question)
        context = {'name': 'Joe Bloggs'}

        rendered_state = TemplateRenderer().render_state(state, context)

        self.assertEqual(rendered_state.schema_item.title, 'Hello Joe Bloggs')

    def test_render_date(self):
        date = '{{date|format_date}}'
        context = {'date': datetime.strptime('01/01/2017', '%d/%m/%Y')}

        rendered = TemplateRenderer().render(date, **context)

        self.assertEqual(rendered, '1 January 2017')
