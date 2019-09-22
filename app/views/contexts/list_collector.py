from flask import url_for
from flask_babel import lazy_gettext

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.question import build_question_context


def build_list_items_summary_context(
    list_collector_block, schema, answer_store, list_store, language, return_to=None
):
    list_name = list_collector_block['for_list']
    list_item_ids = list_store[list_name].items

    primary_person = list_store[list_name].primary_person

    list_items = []

    for list_item_id in list_item_ids:
        placeholder_renderer = PlaceholderRenderer(
            language, schema=schema, answer_store=answer_store
        )

        try:
            rendered_summary = placeholder_renderer.render(
                list_collector_block['summary'], list_item_id
            )
        except KeyError:
            return []

        is_primary = list_item_id == primary_person

        if is_primary:
            rendered_summary['item_title'] += lazy_gettext(' (You)')

        list_items.append(
            {
                'item_title': rendered_summary['item_title'],
                'edit_link': url_for(
                    'questionnaire.block',
                    list_name=list_name,
                    block_id=list_collector_block['edit_block']['id'],
                    list_item_id=list_item_id,
                    return_to=return_to,
                ),
                'remove_link': url_for(
                    'questionnaire.block',
                    list_name=list_name,
                    block_id=list_collector_block['remove_block']['id'],
                    list_item_id=list_item_id,
                    return_to=return_to,
                ),
                'primary_person': is_primary,
            }
        )

    return list_items


def build_list_collector_context(
    list_collector_block, schema, answer_store, list_store, language, form
):
    question_context = build_question_context(list_collector_block, form)
    list_collector_context = {
        'list_items': build_list_items_summary_context(
            list_collector_block, schema, answer_store, list_store, language
        ),
        'add_link': url_for(
            'questionnaire.block',
            list_name=list_collector_block['for_list'],
            block_id=list_collector_block['id'],
        ),
    }

    return {**question_context, **list_collector_context}
