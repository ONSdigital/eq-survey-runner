from app.jinja_filters import (
    get_formatted_currency,
    format_number,
    format_unit,
    format_percentage,
)
from app.questionnaire.schema_utils import (
    choose_question_to_display,
    get_answer_ids_in_block,
)
from app.views.contexts.summary.block import Block
from app.views.contexts.summary_context import build_view_context_for_summary
from app.views.handlers.content import Content


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


class CalculatedSummary(Content):

    def get_context(self):
        current_block = self._schema.get_block(self._current_location.block_id)

        section_list = _build_calculated_summary_section_list(
            self._schema,
            current_block,
            self._current_location,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._questionnaire_store.metadata,
        )

        context = build_view_context_for_summary(
            self._schema, current_block['type'], self.path_finder, section_list
        )

        for group in context.get('summary').get('groups'):
            for block in group.get('blocks'):
                block['question'] = Block.get_question(
                    block['id'],
                    self._questionnaire_store.answer_store,
                    self._questionnaire_store.list_store,
                    self._questionnaire_store.metadata,
                    self._schema,
                    self._current_location,
                )

        formatted_total = _get_formatted_total(
            context['summary'].get('groups', []),
            self._questionnaire_store.metadata,
            self._questionnaire_store.answer_store,
            self._questionnaire_store.list_store,
            self._schema,
            current_location=self.current_location,
        )

        context['summary'].update(
            {
                'calculated_question': _get_calculated_question(
                    current_block['calculation'], formatted_total
                ),
                'title': current_block.get('title') % dict(total=formatted_total),
            }
        )

        return context
