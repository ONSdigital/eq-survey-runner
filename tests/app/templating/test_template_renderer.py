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

    def test_strings_containing_backslashes_are_escaped(self):
        title = '{{ [answers.person_name] | format_household_name }}'
        context = {
            'answers': {
                'person_name': '\\',
            }
        }

        rendered = TemplateRenderer().render(title, **context)

        self.assertEqual(rendered, '\\')

    def test_strings_containing_quotes_are_escaped(self):
        title = '{{ [answers.person_name] | format_household_name }}'
        context = {
            'answers': {
                'person_name': '"',
            }
        }

        rendered = TemplateRenderer().render(title, **context)

        self.assertEqual(rendered, '"')

    def test_household_summary_values_are_escaped(self):
        description = "<h2 class='neptune'>Your household includes:</h2> {{ [answers.first_name, answers.middle_names, answers.last_name]|format_household_summary }}"
        context = {
            'answers': {
                'first_name': ['Alice', 'Bob', '\\', 'Dave'],
                'middle_names': ['', 'Berty', '"', 'Dixon'],
                'last_name': ['Aardvark', 'Brown', '!', 'Davies'],
            }
        }

        rendered = TemplateRenderer().render(description, **context)
        self.assertEqual(rendered, '<h2 class=\'neptune\'>Your household includes:</h2> <ul><li>Alice Aardvark</li><li>Bob Berty Brown</li><li>\ " !</li><li>Dave Dixon Davies</li></ul>')
