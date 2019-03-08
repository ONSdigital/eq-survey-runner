# coding: utf-8

# pylint: disable=too-many-public-methods

import datetime

from app.templating.template_renderer import TemplateRenderer
from tests.app.app_context_test_case import AppContextTestCase


class TestTemplateRenderer(AppContextTestCase):
    def test_render_schema_item(self):
        title = 'Hello {{name}}'
        context = {'name': 'Joe Bloggs'}

        rendered = TemplateRenderer().render(title, **context)

        self.assertEqual(rendered, 'Hello Joe Bloggs')

    def test_render_date(self):
        date = '{{date|format_date}}'
        context = {'date': '2017-01-01'}

        with self.app_request_context('/'):
            rendered = TemplateRenderer().render(date, **context)

        self.assertEqual(rendered, "<span class='date'>1 January 2017</span>")

    def test_render_date_month_year(self):
        date = '{{date|format_date}}'
        context = {'date': '2017-01'}

        with self.app_request_context('/'):
            rendered = TemplateRenderer().render(date, **context)

        self.assertEqual(rendered, "<span class='date'>January 2017</span>")

    def test_strings_containing_backslashes_are_escaped(self):
        title = '{{ [answers.person_name] | format_household_name }}'
        context = {
            'answers': {
                'person_name': '\\',
            }
        }

        rendered = TemplateRenderer().render(title, **context)

        self.assertEqual(rendered, '\\')

    def test_strings_containing_quotes_not_changed(self):
        title = '{{ [answers.person_name] | format_household_name }}'
        context = {
            'answers': {
                'person_name': '"',
            }
        }

        rendered = TemplateRenderer().render(title, **context)

        self.assertEqual(rendered, '&#34;')

    def test_household_summary_values_are_escaped_and_not_encoded(self):
        description = "<h2 class='u-fs-m'>Your household includes:</h2> " \
                      '{{ [answers.first_name, answers.middle_names, answers.last_name]|format_household_summary }}'
        context = {
            'answers': {
                'first_name': ['Alice', 'Bob', '\\', 'Dave'],
                'middle_names': ['', 'Berty', '"', 'Dixon'],
                'last_name': ['Aardvark', 'Brown', '!', 'Davies'],
            }
        }

        rendered = TemplateRenderer().render(description, **context)
        self.assertEqual(rendered, "<h2 class='u-fs-m'>Your household includes:</h2> "
                                   '<ul>'
                                   '<li>Alice Aardvark</li>'
                                   '<li>Bob Berty Brown</li>'
                                   r'<li>\ &#34; !</li>'
                                   '<li>Dave Dixon Davies</li>'
                                   '</ul>')

    def test_household_summary_with_no_names(self):
        description = "<h2 class='u-fs-m'>Your household includes:</h2> " \
                      '{{ []|format_household_summary }}'
        context = {}

        rendered = TemplateRenderer().render(description, **context)
        self.assertEqual(rendered, "<h2 class='u-fs-m'>Your household includes:</h2> "
                                   '')

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

    def test_should_replace_jinja_template_variable_containing_function(self):
        content = 'Is {{ format_date_range(metadata.ref_p_start_date, metadata.ref_p_end_date)}} correct?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'Is … correct?')

    def test_should_replace_jinja_template_variable_containing_curly_braces(self):
        content = 'Is {{ calculate_offset_from_weekday_in_last_whole_week(collection_metadata[started_at], {}, SU) }} correct?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'Is … correct?')

    def test_should_replace_jinja_template_condtional_dates(self):
        content = 'Is {{ format_condtional_date(metadata.ref_p_start_date, metadata.ref_p_end_date)}} correct?'

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
        content = 'Is {{ format_something(metadata.ref_p_start_date|length)}} really <strong>correct</strong>?'

        safe_content = TemplateRenderer.safe_content(content)

        self.assertEqual(safe_content, 'Is … really correct?')

    def test_render_max(self):
        content = 'The largest number is {{ max_value(first, second) }}'
        context = {
            'first': 1,
            'second': 2
        }
        rendered = TemplateRenderer().render(content, **context)
        self.assertEqual(rendered, 'The largest number is 2')

    def test_render_max_str(self):
        content = 'The largest string is {{ max_value(first, second) }}'
        context = {
            'first': 'zzz',
            'second': 'zzz1'
        }
        rendered = TemplateRenderer().render(content, **context)
        self.assertEqual(rendered, 'The largest string is zzz1')

    def test_render_max_date(self):
        content = 'The most recent date is {{ max_value(first, second) }}'
        now = datetime.datetime.utcnow()
        then = now - datetime.timedelta(seconds=60)
        context = {
            'first': now,
            'second': then
        }
        rendered = TemplateRenderer().render(content, **context)
        self.assertEqual(rendered, 'The most recent date is {}'.format(now))

    def test_render_min(self):
        content = 'The smallest number is {{ min_value(first, second) }}'
        context = {
            'first': 1,
            'second': 2
        }
        rendered = TemplateRenderer().render(content, **context)
        self.assertEqual(rendered, 'The smallest number is 1')

    def test_render_min_str(self):
        content = 'The smallest string is {{ min_value(first, second) }}'
        context = {
            'first': 'zzz',
            'second': 'zzz1'
        }
        rendered = TemplateRenderer().render(content, **context)
        self.assertEqual(rendered, 'The smallest string is zzz')

    def test_render_min_date(self):
        content = 'The least recent date is {{ min_value(first, second) }}'
        now = datetime.datetime.utcnow()
        then = now - datetime.timedelta(seconds=60)
        context = {
            'first': now,
            'second': then
        }
        rendered = TemplateRenderer().render(content, **context)
        self.assertEqual(rendered, 'The least recent date is {}'.format(then))
