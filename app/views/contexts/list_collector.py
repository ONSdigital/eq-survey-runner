from flask import url_for
from flask_babel import lazy_gettext

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.question import build_question_context


def build_list_items_summary_context(
    rendered_block, answer_store, list_store, language
):
    list_name = rendered_block['for_list']
    list_item_ids = list_store[list_name].items
    list_answer_ids = [
        answer['id'] for answer in rendered_block['add_block']['question']['answers']
    ]

    primary_person = list_store[list_name].primary_person

    list_items = []

    for list_item_id in list_item_ids:
        placeholder_renderer = PlaceholderRenderer(
            language, answer_store=answer_store, list_item_id=list_item_id
        )

        try:
            rendered_summary = placeholder_renderer.render(rendered_block['summary'])
        except KeyError:
            return []

        if list_item_id == primary_person:
            is_primary = True
            rendered_summary['item_title'] += lazy_gettext(' (You)')
        else:
            is_primary = False

        list_items.append(
            {
                'answers': answer_store.get_answers_by_answer_id(
                    list_answer_ids, list_item_id
                ),
                'item_title': rendered_summary['item_title'],
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

    return list_items


def build_list_collector_context(
    rendered_block, answer_store, list_store, language, form
):
    question_context = build_question_context(rendered_block, form)
    list_collector_context = {
        'list_items': build_list_items_summary_context(
            rendered_block, answer_store, list_store, language
        ),
        'add_link': url_for(
            'questionnaire.block',
            list_name=rendered_block['for_list'],
            block_id=rendered_block['id'],
        ),
    }

    return {**question_context, **list_collector_context}
