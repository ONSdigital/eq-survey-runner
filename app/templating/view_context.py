from flask import url_for
from app.questionnaire.placeholder_transforms import PlaceholderTransforms
from app.helpers.form_helper import get_form_for_location
from app.jinja_filters import get_formatted_currency, format_number, format_unit, format_percentage
from app.templating.summary_context import build_summary_rendering_context
from app.questionnaire.schema_utils import choose_question_to_display, get_answer_ids_in_block


def build_view_context(block_type, metadata, schema, list_store, answer_store, rendered_block, current_location, form):
    if block_type == 'Summary':
        return build_view_context_for_final_summary(metadata, schema, answer_store, block_type,
                                                    rendered_block)

    if block_type == 'SectionSummary':
        return build_view_context_for_section_summary(metadata, schema, answer_store, block_type, current_location)

    if block_type == 'CalculatedSummary':
        return build_view_context_for_calculated_summary(metadata, schema, answer_store, block_type, current_location)

    if block_type in ('Question', 'ConfirmationQuestion', 'ListAddQuestion', 'ListEditQuestion', 'ListRemoveQuestion'):
        form = form or get_form_for_location(schema, rendered_block, current_location, answer_store, metadata)
        return build_view_context_for_question(rendered_block, form)

    if block_type == 'ListCollector':
        form = form or get_form_for_location(schema, rendered_block, current_location, answer_store, metadata)
        return build_view_context_for_list_collector(rendered_block, list_store, answer_store, form)

    if block_type in ('Introduction', 'Interstitial', 'Confirmation'):
        return build_view_context_for_non_question(rendered_block, metadata)


def generate_list_item_title(answers, block_schema):
    """
    Generate a list item title from the answers within a block. Concatenates stripped answers with a space.
    Assumes that the block has already had variants transformed
    """
    output = []
    for block_answer in block_schema['question']['answers']:
        output.append(next((answer.value for answer in answers if answer.answer_id == block_answer['id']), '').strip())

    output = ' '.join(PlaceholderTransforms.remove_empty_from_list(output))

    return output


def build_view_context_for_list_collector(rendered_block, list_store, answer_store, form):
    question_context = build_view_context_for_question(rendered_block, form)

    list_name = rendered_block['populates_list']
    list_item_ids = list_store[list_name]

    list_title_answer_ids = [answer['id'] for answer in rendered_block['add_block']['question']['answers']]

    list_items = []
    for list_item_id in list_item_ids:
        title_answers = answer_store.get_answers_by_answer_id(answer_ids=list_title_answer_ids, list_item_id=list_item_id)
        if title_answers:
            list_items.append({
                'answers': title_answers,
                'item_title': generate_list_item_title(title_answers, rendered_block['add_block']),
                'edit_link': url_for('questionnaire.get_block',
                                     list_name=list_name,
                                     block_id=rendered_block['edit_block']['id'],
                                     list_item_id=list_item_id),
                'remove_link': url_for('questionnaire.get_block',
                                       list_name=list_name,
                                       block_id=rendered_block['remove_block']['id'],
                                       list_item_id=list_item_id),
            })

    list_collector_context = {
        'list_items': list_items,
        'add_link': url_for('questionnaire.get_block', list_name=rendered_block['populates_list'], block_id=rendered_block['id']),
    }

    return {**question_context, **list_collector_context}


def build_view_context_for_final_summary(metadata, schema, answer_store, block_type, rendered_block):
    section_list = schema.json['sections']

    context = build_view_context_for_summary(schema, section_list, answer_store, metadata, block_type)

    context['summary'].update({
        'is_view_submission_response_enabled': _is_view_submitted_response_enabled(schema.json),
        'collapsible': rendered_block.get('collapsible', False),
    })

    return context


def build_view_context_for_summary(schema, section_list, answer_store, metadata, block_type):
    summary_rendering_context = build_summary_rendering_context(schema, section_list, answer_store, metadata)

    context = {
        'summary': {
            'groups': summary_rendering_context,
            'answers_are_editable': True,
            'summary_type': block_type,
        },
    }
    return context


def build_view_context_for_section_summary(metadata, schema, answer_store, block_type, current_location):
    group = schema.get_group_by_block_id(current_location.block_id)
    section_id = group['parent_id']
    section = schema.get_section(section_id)
    title = section.get('title')

    context = build_view_context_for_summary(schema, [section], answer_store, metadata,
                                             block_type)

    context['summary'].update({
        'title': title,
    })
    return context


def build_view_context_for_calculated_summary(metadata, schema, answer_store, block_type,
                                              current_location):
    block = schema.get_block(current_location.block_id)
    section_list = _build_calculated_summary_section_list(schema, block, current_location, answer_store, metadata)

    context = build_view_context_for_summary(schema, section_list, answer_store, metadata, block_type)

    formatted_total = _get_formatted_total(context['summary'].get('groups', []), metadata, answer_store, schema)

    context['summary'].update({
        'calculated_question': _get_calculated_question(block['calculation'], formatted_total),
        'title': block.get('title') % dict(total=formatted_total),
    })
    return context


def build_view_context_for_non_question(rendered_block, metadata):
    return {
        'block': rendered_block,
        'metadata': dict(metadata),
    }


def build_view_context_for_question(rendered_block, form):  # noqa: C901, E501  pylint: disable=too-complex,line-too-long,too-many-locals,too-many-branches
    question = rendered_block['question']

    context = {
        'block': rendered_block,
        'form': {
            'errors': form.errors,
            'question_errors': form.question_errors,
            'mapped_errors': form.map_errors(),
            'answer_errors': {},
            'data': {},
            'fields': {},
        },
    }

    answer_ids = []

    for answer in question['answers']:
        answer_ids.append(answer['id'])

        if answer['type'] in ('Checkbox', 'Radio'):
            for option in answer['options']:
                if 'detail_answer' in option:
                    answer_ids.append(option['detail_answer']['id'])

    for answer_id in answer_ids:
        context['form']['answer_errors'][answer_id] = form.answer_errors(answer_id)

        if hasattr(form, 'get_data'):
            context['form']['data'][answer_id] = form.get_data(answer_id)

        if answer_id in form:
            context['form']['fields'][answer_id] = form[answer_id]

    return context


def _build_calculated_summary_section_list(schema, rendered_block, current_location, answer_store, metadata):
    """Build up the list of blocks only including blocks / questions / answers which are relevant to the summary"""
    group = schema.get_group_by_block_id(current_location.block_id)
    blocks = []
    answers_to_calculate = rendered_block['calculation']['answers_to_calculate']
    blocks_to_calculate = [schema.get_block_for_answer_id(answer_id) for answer_id in answers_to_calculate]
    unique_blocks = list({block['id']: block for block in blocks_to_calculate}.values())

    for block in unique_blocks:
        if block['type'] == 'Question':
            transformed_block = _remove_unwanted_questions_answers(block, answers_to_calculate, answer_store, metadata, schema)
            if set(get_answer_ids_in_block(transformed_block)) & set(answers_to_calculate):
                blocks.append(transformed_block)

    section = {
        'groups': [
            {
                'id': group['id'],
                'blocks': blocks,
            },
        ],
    }

    return [section]


def _remove_unwanted_questions_answers(block, answer_ids_to_keep, answer_store, metadata, schema):
    """
    Evaluates questions in a block and removes any questions not containing a relevant answer
    """
    block_question = choose_question_to_display(block, schema, answer_store, metadata)

    reduced_block = block.copy()

    matching_answers = []
    for answer_id in answer_ids_to_keep:
        matching_answers.extend(schema.get_answers(answer_id))

    questions_to_keep = [answer['parent_id'] for answer in matching_answers]

    if block_question['id'] in questions_to_keep:
        answers_to_keep = [answer for answer in block_question['answers'] if answer['id'] in answer_ids_to_keep]
        block_question['answers'] = answers_to_keep

    return reduced_block


def _get_formatted_total(groups, metadata, answer_store, schema):
    calculated_total = 0
    answer_format = {'type': None}
    for group in groups:
        for block in group['blocks']:
            question = choose_question_to_display(block, schema, metadata, answer_store)
            for answer in question['answers']:
                if not answer_format['type']:
                    answer_format = {
                        'type': answer['type'],
                        'unit': answer.get('unit'),
                        'unit_length': answer.get('unit_length'),
                        'currency': answer.get('currency'),
                    }
                answer_value = answer.get('value') or 0
                calculated_total += answer_value

    if answer_format['type'] == 'currency':
        return get_formatted_currency(calculated_total, answer_format['currency'])

    if answer_format['type'] == 'unit':
        return format_unit(answer_format['unit'], calculated_total, answer_format['unit_length'])

    if answer_format['type'] == 'percentage':
        return format_percentage(calculated_total)

    return format_number(calculated_total)


def _get_calculated_question(calculation_question, formatted_total):
    calculation_title = calculation_question.get('title')

    return {
        'title': calculation_title,
        'id': 'calculated-summary-question',
        'answers': [
            {
                'id': 'calculated-summary-answer',
                'value': formatted_total,
            },
        ],
    }


def _is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False
