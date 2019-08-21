from typing import List, Mapping

from flask import url_for

from app.data_model.answer_store import AnswerStore
from app.data_model.list_store import ListStore
from app.jinja_filters import (
    get_formatted_currency,
    format_number,
    format_unit,
    format_percentage,
)
from app.questionnaire.location import Location
from app.questionnaire.path_finder import PathFinder
from app.questionnaire.questionnaire_schema import QuestionnaireSchema
from app.questionnaire.schema_utils import (
    choose_question_to_display,
    get_answer_ids_in_block,
)
from app.views.contexts.list_collector import build_list_items_summary_context
from app.views.contexts.summary.group import Group


def build_summary_rendering_context(
    schema: QuestionnaireSchema,
    answer_store: AnswerStore,
    list_store: ListStore,
    metadata: Mapping,
    current_location: Location = None,
    sections: List[Mapping] = None,
) -> List:
    path_finder = PathFinder(schema, answer_store, metadata, list_store=list_store)

    sections = sections or schema.get_sections()
    paths = [path_finder.routing_path(section['id']) for section in sections]

    return [
        Group(
            group,
            path,
            answer_store,
            list_store,
            metadata,
            schema,
            current_location=current_location,
        ).serialize()
        for path, section in zip(paths, sections)
        for group in section['groups']
    ]


def build_view_context_for_final_summary(
    metadata, schema, answer_store, list_store, rendered_block, current_location
):
    context = build_view_context_for_summary(
        schema,
        answer_store,
        list_store,
        metadata,
        rendered_block['type'],
        current_location,
    )

    context['summary'].update(
        {
            'is_view_submission_response_enabled': _is_view_submitted_response_enabled(
                schema.json
            ),
            'collapsible': rendered_block.get('collapsible', False),
        }
    )

    return context


def build_view_context_for_summary(
    schema,
    answer_store,
    list_store,
    metadata,
    block_type,
    current_location,
    sections=None,
):
    summary_rendering_context = build_summary_rendering_context(
        schema, answer_store, list_store, metadata, current_location, sections
    )

    context = {
        'summary': {
            'groups': summary_rendering_context,
            'answers_are_editable': True,
            'summary_type': block_type,
        }
    }
    return context


def build_view_context_for_section_summary(
    metadata, schema, answer_store, list_store, block_type, current_location, language
):
    group = schema.get_group_for_block_id(current_location.block_id)
    section_id = group['parent_id']
    section = schema.get_section(section_id)
    title = section.get('title')

    context = build_view_context_for_summary(
        schema,
        answer_store,
        list_store,
        metadata,
        block_type,
        current_location,
        [section],
    )

    list_collector_blocks = schema.get_visible_list_blocks_for_section(section)

    list_summaries = []

    for list_collector_block in list_collector_blocks:
        list_summary = {
            'title': list_collector_block['summary']['title'],
            'add_link': url_for(
                'questionnaire.block',
                list_name=list_collector_block['for_list'],
                block_id=list_collector_block['add_block']['id'],
            ),
            'add_link_text': list_collector_block['summary']['add_link_text'],
            'empty_list_text': list_collector_block['summary']['empty_list_text'],
            'list_items': build_list_items_summary_context(
                list_collector_block, schema, answer_store, list_store, language
            ),
            'list_name': list_collector_block['for_list'],
        }
        list_summaries.append(list_summary)

    context['summary'].update(
        {'title': title, 'list_summaries': list_summaries}
    )

    return context


def build_view_context_for_calculated_summary(
    metadata, schema, answer_store, list_store, block_type, current_location
):
    block = schema.get_block(current_location.block_id)

    section_list = _build_calculated_summary_section_list(
        schema, block, current_location, answer_store, list_store, metadata
    )

    context = build_view_context_for_summary(
        schema,
        answer_store,
        list_store,
        metadata,
        block_type,
        current_location,
        section_list,
    )

    formatted_total = _get_formatted_total(
        context['summary'].get('groups', []),
        metadata,
        answer_store,
        list_store,
        schema,
        current_location=current_location,
    )

    context['summary'].update(
        {
            'calculated_question': _get_calculated_question(
                block['calculation'], formatted_total
            ),
            'title': block.get('title') % dict(total=formatted_total),
        }
    )
    return context


def _build_calculated_summary_section_list(
    schema, rendered_block, current_location, answer_store, list_store, metadata
):
    """Build up the list of blocks only including blocks / questions / answers which are relevant to the summary"""
    section_id = schema.get_section_id_for_block_id(current_location.block_id)
    group = schema.get_group_for_block_id(current_location.block_id)
    blocks = []
    answers_to_calculate = rendered_block['calculation']['answers_to_calculate']
    blocks_to_calculate = [
        schema.get_block_for_answer_id(answer_id) for answer_id in answers_to_calculate
    ]
    unique_blocks = list({block['id']: block for block in blocks_to_calculate}.values())

    for block in unique_blocks:
        if block['type'] == 'Question':
            transformed_block = _remove_unwanted_questions_answers(
                block,
                answers_to_calculate,
                answer_store,
                list_store,
                metadata,
                schema,
                current_location=current_location,
            )
            if set(get_answer_ids_in_block(transformed_block)) & set(
                answers_to_calculate
            ):
                blocks.append(transformed_block)

    return [{'id': section_id, 'groups': [{'id': group['id'], 'blocks': blocks}]}]


def _remove_unwanted_questions_answers(
    block,
    answer_ids_to_keep,
    answer_store,
    list_store,
    metadata,
    schema,
    current_location,
):
    """
    Evaluates questions in a block and removes any questions not containing a relevant answer
    """
    block_question = choose_question_to_display(
        block,
        schema,
        answer_store,
        list_store,
        metadata,
        current_location=current_location,
    )

    reduced_block = block.copy()

    matching_answers = []
    for answer_id in answer_ids_to_keep:
        matching_answers.extend(schema.get_answers_by_answer_id(answer_id))

    questions_to_keep = [answer['parent_id'] for answer in matching_answers]

    if block_question['id'] in questions_to_keep:
        answers_to_keep = [
            answer
            for answer in block_question['answers']
            if answer['id'] in answer_ids_to_keep
        ]
        block_question['answers'] = answers_to_keep

    return reduced_block


def _get_formatted_total(
    groups, metadata, answer_store, list_store, schema, current_location
):
    calculated_total = 0
    answer_format = {'type': None}
    for group in groups:
        for block in group['blocks']:
            question = choose_question_to_display(
                block,
                schema,
                metadata,
                answer_store,
                list_store,
                current_location=current_location,
            )
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
        return format_unit(
            answer_format['unit'], calculated_total, answer_format['unit_length']
        )

    if answer_format['type'] == 'percentage':
        return format_percentage(calculated_total)

    return format_number(calculated_total)


def _get_calculated_question(calculation_question, formatted_total):
    calculation_title = calculation_question.get('title')

    return {
        'title': calculation_title,
        'id': 'calculated-summary-question',
        'answers': [{'id': 'calculated-summary-answer', 'value': formatted_total}],
    }


def _is_view_submitted_response_enabled(schema):
    view_submitted_response = schema.get('view_submitted_response')
    if view_submitted_response:
        return view_submitted_response['enabled']

    return False
