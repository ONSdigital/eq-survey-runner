from flask import url_for
from flask_babel import lazy_gettext

from app.views.contexts.question import build_question_context
from app.questionnaire.placeholder_transforms import PlaceholderTransforms


def build_list_collector_context(rendered_block, form, list_store, answer_store):
    question_context = build_question_context(rendered_block, form)

    list_name = rendered_block['for_list']
    list_item_ids = list_store[list_name].items

    list_title_answer_ids = [
        answer['id'] for answer in rendered_block['add_block']['question']['answers']
    ]

    primary_person = list_store[list_name].primary_person

    list_items = []
    for list_item_id in list_item_ids:
        title_answers = answer_store.get_answers_by_answer_id(
            answer_ids=list_title_answer_ids, list_item_id=list_item_id
        )
        is_primary = list_item_id == primary_person
        if title_answers:
            item_title = _generate_list_item_title(
                title_answers, rendered_block['add_block']
            )

            if is_primary:
                item_title += lazy_gettext(' (You)')

            list_items.append(
                {
                    'answers': title_answers,
                    'item_title': item_title,
                    'edit_link': url_for(
                        'questionnaire.block',
                        list_name=list_name,
                        block_id=rendered_block['edit_block']['id'],
                        list_item_id=list_item_id,
                    ),
                    'remove_link': url_for(
                        'questionnaire.block',
                        list_name=list_name,
                        block_id=rendered_block['remove_block']['id'],
                        list_item_id=list_item_id,
                    ),
                    'primary_person': is_primary,
                }
            )

    list_collector_context = {
        'list_items': list_items,
        'add_link': url_for(
            'questionnaire.block',
            list_name=rendered_block['for_list'],
            block_id=rendered_block['id'],
        ),
    }

    return {**question_context, **list_collector_context}


def _generate_list_item_title(answers, block_schema):
    """
    Generate a list item title from the answers within a block. Concatenates stripped answers with a space.
    Assumes that the block has already had variants transformed
    """
    output = []
    for block_answer in block_schema['question']['answers']:
        output.append(
            next(
                (
                    answer.value
                    for answer in answers
                    if answer.answer_id == block_answer['id']
                ),
                '',
            ).strip()
        )

    output = ' '.join(PlaceholderTransforms.remove_empty_from_list(output))

    return output
