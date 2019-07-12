# coding: utf-8
import re
from datetime import datetime

import flask
import flask_babel
from babel import units, numbers
from jinja2 import Markup, escape, evalcontextfilter

from app.questionnaire.rules import convert_to_datetime

blueprint = flask.Blueprint('filters', __name__)


@blueprint.app_template_filter()
def format_number(value):
    if value or value == 0:
        return numbers.format_decimal(value, locale=flask_babel.get_locale())

    return ''


def get_formatted_currency(value, currency='GBP'):
    if value or value == 0:
        return numbers.format_currency(
            number=value, currency=currency, locale=flask_babel.get_locale()
        )

    return ''


@blueprint.app_template_filter()
def get_currency_symbol(currency='GBP'):
    return numbers.get_currency_symbol(currency, locale=flask_babel.get_locale())


@blueprint.app_template_filter()
def format_percentage(value):
    return '{}%'.format(value)


def format_unit(unit, value, length='short'):
    return units.format_unit(
        value=value,
        measurement_unit=unit,
        length=length,
        locale=flask_babel.get_locale(),
    )


def format_unit_input_label(unit, unit_length='short'):
    """
    This function is used to only get the unit of measurement text.  If the unit_length
    is long then only the plural form of the word is returned (e.g., Hours, Years, etc).

    :param (str) unit unit of measurement
    :param (str) unit_length length of unit text, can be one of short/long/narrow
    """
    if unit_length == 'long':
        return units.format_unit(
            value=2,
            measurement_unit=unit,
            length=unit_length,
            locale=flask_babel.get_locale(),
        ).replace('2 ', '')
    return units.format_unit(
        value='',
        measurement_unit=unit,
        length=unit_length,
        locale=flask_babel.get_locale(),
    ).strip()


def format_duration(value):
    parts = []

    if 'years' in value and (value['years'] > 0 or len(value) == 1):
        parts.append(
            flask_babel.ngettext('%(num)s year', '%(num)s years', value['years'])
        )
    if 'months' in value and (
        value['months'] > 0
        or len(value) == 1
        or ('years' in value and value['years'] == 0)
    ):
        parts.append(
            flask_babel.ngettext('%(num)s month', '%(num)s months', value['months'])
        )
    return ' '.join(parts)


def get_format_multilined_string(value):
    escaped_value = escape(value)
    new_line_regex = r'(?:\r\n|\r|\n)+'
    value_with_line_break_tag = re.sub(new_line_regex, '<br>', escaped_value)
    return '{}'.format(value_with_line_break_tag)


def get_format_date(value):
    """Format a datetime string.

    :param (jinja2.nodes.EvalContext) context: Evaluation context.
    :param (any) value: Value representing a datetime.
    :returns (str): Formatted datetime.
    """
    value = value[0] if isinstance(value, list) else value
    date_format = 'd MMMM yyyy'
    if value and re.match(r'\d{4}-\d{2}$', value):
        date_format = 'MMMM yyyy'
    if value and re.match(r'\d{4}$', value):
        date_format = 'yyyy'

    date_to_format = convert_to_datetime(value).date()
    result = "<span class='date'>{date}</span>".format(
        date=flask_babel.format_date(date_to_format, format=date_format)
    )

    return result


@evalcontextfilter
@blueprint.app_template_filter()
def format_datetime(context, value):
    london_date_time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
    london_date = london_date_time.date()
    formatted_date = flask_babel.format_date(london_date, format='d MMMM yyyy')
    formatted_time = flask_babel.format_time(london_date_time, format='HH:mm')

    result = "<span class='date'>{date}</span>".format(
        date=flask_babel.gettext(
            '%(date)s at %(time)s', date=formatted_date, time=formatted_time
        )
    )
    return mark_safe(context, result)


def get_format_date_range(start_date, end_date):
    return flask_babel.gettext(
        '%(from_date)s to %(to_date)s',
        from_date=get_format_date(start_date),
        to_date=get_format_date(end_date),
    )


@blueprint.app_template_filter()
def language_urls(languages, current_language):
    if not any(language[0] == current_language for language in languages):
        current_language = 'en'

    return [LanguageConfig(language, current_language) for language in languages]


@blueprint.app_context_processor
def format_unit_processor():
    return dict(format_unit=format_unit)


@blueprint.app_context_processor
def format_unit_input_label_processor():
    return dict(format_unit_input_label=format_unit_input_label)


@blueprint.app_context_processor
def get_currency_symbol_processor():
    return dict(get_currency_symbol=get_currency_symbol)


@blueprint.app_context_processor
def language_urls_processor():
    return dict(language_urls=language_urls)


def mark_safe(context, value):
    if context.autoescape:
        value = Markup(value)
    return value


@blueprint.app_template_filter()
def setAttribute(dictionary, key, value):
    dictionary[key] = value
    return dictionary


@blueprint.app_template_filter()
def setAttributes(dictionary, attributes):
    for key in attributes:
        dictionary[key] = attributes[key]
    return dictionary


@blueprint.app_template_filter()
def should_wrap_with_fieldset(question):
    answers = question['answers']

    if len(answers) > 1 and not any(answer['type'] == 'Date' for answer in answers):
        return True

    return False


@blueprint.app_context_processor
def should_wrap_with_fieldset_processor():
    return {'should_wrap_with_fieldset': should_wrap_with_fieldset}


class LabelConfig:
    def __init__(self, _for, text, description=None):
        self._for = _for
        self.text = text
        self.description = description


class CheckboxConfig:
    def __init__(self, option, index, form, answer):
        self.id = option.id
        self.name = option.name
        self.value = option.data
        self.checked = option.checked

        label_description = None
        answer_option = answer['options'][index]

        if answer_option and 'description' in answer_option:
            label_description = answer_option['description']

        self.label = LabelConfig(option.id, option.label.text, label_description)

        if option.detail_answer_id:
            detail_answer = form['fields'][option.detail_answer_id]
            self.other = OtherConfig(detail_answer)


class RadioConfig:
    def __init__(self, option, index, form, answer):
        self.id = option.id
        self.name = option.name
        self.value = option.data
        self.checked = option.checked

        label_description = None
        answer_option = answer['options'][index]

        if answer_option and 'description' in answer_option:
            label_description = answer_option['description']

        self.label = LabelConfig(option.id, option.label.text, label_description)

        if option.detail_answer_id:
            detail_answer = form['fields'][option.detail_answer_id]
            self.other = OtherConfig(detail_answer)


class RelationshipRadioConfig:
    def __init__(self, option, index, answer):
        self.id = option.id
        self.name = option.name
        self.value = option.data
        self.checked = option.checked

        label_description = None
        answer_option = answer['options'][index]

        self.label = LabelConfig(option.id, option.label.text, label_description)

        if answer_option:
            self.attributes = {
                'data-title': answer_option['title'],
                'data-playback': answer_option['playback'],
            }


class OtherConfig:
    def __init__(self, detail_answer):
        self.id = detail_answer.id
        self.name = detail_answer.name
        self.value = detail_answer.data or ''
        self.label = LabelConfig(detail_answer.id, detail_answer.label.text)


@blueprint.app_template_filter()
def map_checkbox_config(form, answer):
    options = form['fields'][answer['id']]

    return [CheckboxConfig(option, i, form, answer) for i, option in enumerate(options)]


@blueprint.app_context_processor
def map_checkbox_config_processor():
    return dict(map_checkbox_config=map_checkbox_config)


@blueprint.app_template_filter()
def map_radio_config(form, answer):
    options = form['fields'][answer['id']]

    return [RadioConfig(option, i, form, answer) for i, option in enumerate(options)]


@blueprint.app_context_processor
def map_radio_config_processor():
    return dict(map_radio_config=map_radio_config)


@blueprint.app_template_filter()
def map_relationships_config(form, answer):
    options = form['fields'][answer['id']]

    return [
        RelationshipRadioConfig(option, i, answer) for i, option in enumerate(options)
    ]


@blueprint.app_context_processor
def map_relationships_config_processor():
    return dict(map_relationships_config=map_relationships_config)


class SelectOptionConfig:
    def __init__(self, option, select):
        self.text = option[1]
        self.value = option[0]
        self.selected = select.data == self.value
        self.disabled = self.value == '' and select.flags.required


@blueprint.app_template_filter()
def map_select_config(select):
    return [SelectOptionConfig(tuple[1], select) for tuple in enumerate(select.choices)]


@blueprint.app_context_processor
def map_select_config_processor():
    return dict(map_select_config=map_select_config)


class LanguageConfig:
    def __init__(self, language, current_language):
        self.ISOCode = language[0]
        self.url = '?language_code=' + self.ISOCode
        self.text = language[1]
        self.current = self.ISOCode == current_language


class SummaryAction:
    def __init__(
        self, block, answer, answer_title, edit_link_text, edit_link_aria_label
    ):
        self.text = edit_link_text
        self.ariaLabel = edit_link_aria_label + ' ' + answer_title
        self.url = block['link'] + '#' + answer['id']

        qa_attribute = answer['id'] + '-edit'
        self.attributes = dict(**{'data-qa': qa_attribute})


class SummaryRowItemValue:
    def __init__(self, text, other=None):
        self.text = text

        if other:
            self.other = other


class SummaryRowItem:
    def __init__(  # noqa: C901, R0912  pylint: disable=too-complex,too-many-branches
        self,
        block,
        question,
        answer,
        multiple_answers,
        answers_are_editable,
        no_answer_provided,
        edit_link_text,
        edit_link_aria_label,
        summary_type,
    ):

        if 'type' in answer:
            answer_type = answer['type']
        else:
            answer_type = 'calculated'

        if (
            (
                multiple_answers
                or answer_type == 'relationship'
                or summary_type == 'CalculatedSummary'
            )
            and 'label' in answer
            and answer['label']
        ):
            self.title = answer['label']
            self.titleAttributes = {'data-qa': answer['id'] + '-label'}
        else:
            self.title = question['title']
            self.titleAttributes = {'data-qa': question['id']}

        value = answer['value']

        self.attributes = {'data-qa': answer['id']}

        if value is None or value == '':
            self.valueList = [SummaryRowItemValue(no_answer_provided)]
        elif answer_type == 'checkbox':
            self.valueList = [
                SummaryRowItemValue(val.label, val.detail_answer_value) for val in value
            ]
        elif answer_type == 'currency':
            self.valueList = [
                SummaryRowItemValue(get_formatted_currency(value, answer['currency']))
            ]
        elif answer_type in ['date', 'monthyeardate', 'yeardate']:
            if question['type'] == 'DateRange':
                self.valueList = [
                    SummaryRowItemValue(
                        get_format_date_range(value['from'], value['to'])
                    )
                ]
            else:
                self.valueList = [SummaryRowItemValue(get_format_date(value))]
        elif answer_type == 'duration':
            self.valueList = [SummaryRowItemValue(format_duration(value))]
        elif answer_type == 'number':
            self.valueList = [SummaryRowItemValue(format_number(value))]
        elif answer_type == 'percentage':
            self.valueList = [SummaryRowItemValue(format_percentage(value))]
        elif answer_type == 'radio':
            detail_answer_value = value['detail_answer_value']
            self.valueList = [SummaryRowItemValue(value['label'], detail_answer_value)]
        elif answer_type == 'textarea':
            self.valueList = [SummaryRowItemValue(get_format_multilined_string(value))]
        elif answer_type == 'unit':
            self.valueList = [
                SummaryRowItemValue(
                    format_unit(answer['unit'], value, answer['unit_length'])
                )
            ]
        else:
            self.valueList = [SummaryRowItemValue(value)]

        if answers_are_editable:
            self.actions = [
                SummaryAction(
                    block, answer, self.title, edit_link_text, edit_link_aria_label
                )
            ]


class SummaryRow:
    def __init__(
        self,
        block,
        question,
        summary_type,
        answers_are_editable,
        no_answer_provided,
        edit_link_text,
        edit_link_aria_label,
    ):
        self.title = question['title']
        self.rowItems = []

        multiple_answers = len(question['answers']) > 1

        if summary_type == 'CalculatedSummary' and not answers_are_editable:
            self.total = True

        for answer in question['answers']:
            self.rowItems.append(
                SummaryRowItem(
                    block,
                    question,
                    answer,
                    multiple_answers,
                    answers_are_editable,
                    no_answer_provided,
                    edit_link_text,
                    edit_link_aria_label,
                    summary_type,
                )
            )


@blueprint.app_template_filter()
def map_summary_item_config(
    group,
    summary_type,
    answers_are_editable,
    no_answer_provided,
    edit_link_text,
    edit_link_aria_label,
    calculated_question,
):
    rows = []

    for block in group['blocks']:
        rows.append(
            SummaryRow(
                block,
                block['question'],
                summary_type,
                answers_are_editable,
                no_answer_provided,
                edit_link_text,
                edit_link_aria_label,
            )
        )
        if summary_type == 'CalculatedSummary':
            rows.append(
                SummaryRow(
                    block, calculated_question, summary_type, False, None, None, None
                )
            )

    return rows


@blueprint.app_context_processor
def map_summary_item_config_processor():
    return dict(map_summary_item_config=map_summary_item_config)


@blueprint.app_template_filter()
def map_list_collector_config(
    list_items,
    icon,
    edit_link_text,
    edit_link_aria_label,
    remove_link_text,
    remove_link_aria_label,
):
    rows = []

    for list_item in list_items:
        item_name = list_item.get('item_title')
        new_row = {
            'title': item_name,
            'rowItems': [
                {
                    'icon': icon,
                    'actions': [
                        {
                            'text': edit_link_text,
                            'ariaLabel': edit_link_aria_label.format(
                                item_name=item_name
                            ),
                            'url': list_item.get('edit_link'),
                            'attributes': {'data-qa': 'change-item-link'},
                        }
                    ],
                }
            ],
        }

        if not list_item.get('primary_person'):
            new_row['rowItems'][0]['actions'].append(
                {
                    'text': remove_link_text,
                    'ariaLabel': remove_link_aria_label.format(item_name=item_name),
                    'url': list_item.get('remove_link'),
                    'attributes': {'data-qa': 'remove-item-link'},
                }
            )

        rows.append(new_row)

    return rows


@blueprint.app_context_processor
def map_list_collector_config_processor():
    return dict(map_list_collector_config=map_list_collector_config)


@blueprint.app_template_filter()
def format_paragraphs(text):
    return '\n'.join(f'<p>{paragraph}</p>' for paragraph in text.splitlines())


@blueprint.app_context_processor
def paragraphs_processor():
    return dict(format_paragraphs=format_paragraphs)
