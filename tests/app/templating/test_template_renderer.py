import unittest
from datetime import datetime

from app.templating.template_renderer import TemplateRenderer


class TestTemplateRenderer(unittest.TestCase):
    def test_render_schema_item(self):
        title = 'Hello {{name}}'
        context = {'name': 'Joe Bloggs'}

        rendered = TemplateRenderer().render(title, **context)

        self.assertEqual(rendered, 'Hello Joe Bloggs')

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

    def test_household_summary_with_no_names(self):
        description = "<h2 class='neptune'>Your household includes:</h2> " \
                      "{{ []|format_household_summary }}"
        context = {}

        rendered = TemplateRenderer().render(description, **context)
        self.assertEqual(rendered, "<h2 class='neptune'>Your household includes:</h2> "
                                   "")

    def test_render_nested_templatable_property(self):
        guidance = {
            'title': 'Include',
            'description': '{{someone_else}}',
            'list': [
                '{{yourself}}',
                'People here on holiday',
                '{{someone}}',
            ]
        }

        context = {'yourself': 'Joe Bloggs', 'someone': 'Jane Bloggs', 'someone_else': 'John Doe'}

        rendered = TemplateRenderer().render(guidance, **context)

        expected = {
            'title': 'Include',
            'description': 'John Doe',
            'list': [
                'Joe Bloggs',
                'People here on holiday',
                'Jane Bloggs',
            ]
        }

        self.assertEqual(rendered, expected)

    def test_given_none_safe_content_should_return_none(self):
        content = None

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, None)

    def test_given_empty_string_safe_content_should_return_empty_string(self):
        content = ''

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, '')

    def test_should_replace_jinja_template_variable(self):
        content = 'Your answer is {{ answers.your_answer}}'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'Your answer is …')

    def test_should_replace_multiple_jinja_template_variable(self):
        content = 'Your answer is {{ answers.your_answer}} to {{answers.your_other_answer }}'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'Your answer is … to …')

    def test_should_replace_jinja_template_variable_containing_special_characters(self):
        content = 'How is {{ [answers.first_name[group_instance], answers.last_name[group_instance]] | format_household_name }} ' \
                  'related to the people below?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'How is … related to the people below?')

    def test_should_replace_jinja_template_variable_containing_function(self):
        content = 'Is {{ format_start_end_date(meta.survey.start_date, meta.survey.end_date)}} correct?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'Is … correct?')

    def test_should_replace_simple_html_tags(self):
        content = 'This <em>string contains</em> <p><strong>some</strong></p><i>HTML</i>tags?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'This string contains someHTMLtags?')

    def test_should_replace_complex_broken_html_tags(self):
        content = 'This <div style="bleh" a=2>string contains <a href="http://www.ons.gov.uk/not_found">a link</a>'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'This string contains a link')

    def test_should_replace_broken_html_tags(self):
        content = '</lzz> This <em>string contains<p><strong><i><div> some</strong></p><i> HTML </i>tags?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, ' This string contains some HTML tags?')

    def test_should_replace_html_tags_and_jinja_templates_together(self):
        content = 'Is {{ format_something(meta.survey.start_date|length)}} really <strong>correct</strong>?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'Is … really correct?')
