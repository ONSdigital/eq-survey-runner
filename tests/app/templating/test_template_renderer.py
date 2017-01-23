import unittest
from datetime import datetime

from app.schema.question import Question
from app.templating.template_renderer import TemplateRenderer


class TestTemplateRenderer(unittest.TestCase):
    def test_render_schema_item(self):
        question = Question()
        question.title = 'Hello {{name}}'
        question.templatable_properties = ['title']
        context = {'name': 'Joe Bloggs'}

        schema = TemplateRenderer().render_schema_items(question, context)

        self.assertEqual(schema.title, 'Hello Joe Bloggs')

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
        description = "<h2 class='neptune'>Your household includes:</h2> " \
                      "{{ [answers.first_name, answers.middle_names, answers.last_name]|format_household_summary }}"
        context = {
            'answers': {
                'first_name': ['Alice', 'Bob', '\\', 'Dave'],
                'middle_names': ['', 'Berty', '"', 'Dixon'],
                'last_name': ['Aardvark', 'Brown', '!', 'Davies'],
            }
        }

        rendered = TemplateRenderer().render(description, **context)
        self.assertEqual(rendered, "<h2 class='neptune'>Your household includes:</h2> "
                                   "<ul>"
                                   "<li>Alice Aardvark</li>"
                                   "<li>Bob Berty Brown</li>"
                                   r'<li>\ " !</li>'
                                   "<li>Dave Dixon Davies</li>"
                                   "</ul>")

    def test_render_nested_templatable_property(self):
        question = Question()
        question.guidance = [
            {
                'title': 'Include',
                'description': '{{someone_else}}',
                'list': [
                    '{{yourself}}',
                    'People here on holiday',
                    ['{{someone}}']
                ]

            }
        ]
        context = {'yourself': 'Joe Bloggs', 'someone': 'Jane Bloggs', 'someone_else': 'John Doe'}

        schema = TemplateRenderer().render_schema_items(question, context)

        expected = [
            {
                'title': 'Include',
                'description': 'John Doe',
                'list': [
                    'Joe Bloggs',
                    'People here on holiday',
                    ['Jane Bloggs']
                ]
            }
        ]
        self.assertEqual(schema.guidance, expected)
