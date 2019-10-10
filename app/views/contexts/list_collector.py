from flask import url_for
from flask_babel import lazy_gettext

from app.questionnaire.placeholder_renderer import PlaceholderRenderer
from app.views.contexts.question import build_question_context


def get_item_title(list_block_summary, list_item_id, is_primary, placeholder_renderer):
    rendered_summary = placeholder_renderer.render(list_block_summary, list_item_id)

    if is_primary:
        rendered_summary['item_title'] += lazy_gettext(' (You)')

    return rendered_summary['item_title']


def build_list_items_summary_context(
    list_collector_block, schema, answer_store, list_store, language, return_to=None
):
    list_name = list_collector_block['for_list']
    list_item_ids = list_store[list_name].items

    primary_person = list_store[list_name].primary_person

    placeholder_renderer = PlaceholderRenderer(
        language, schema=schema, answer_store=answer_store
    )

    list_items = []

    for list_item_id in list_item_ids:
        is_primary = list_item_id == primary_person
        list_item_context = {}

        if 'summary' in list_collector_block:
            list_item_context = {
                'item_title': get_item_title(
                    list_collector_block['summary'],
                    list_item_id,
                    is_primary,
                    placeholder_renderer,
                ),
                'primary_person': is_primary,
            }

            if 'edit_block' in list_collector_block:
                list_item_context['edit_link'] = url_for(
                    'questionnaire.block',
                    list_name=list_name,
                    block_id=list_collector_block['edit_block']['id'],
                    list_item_id=list_item_id,
                    return_to=return_to,
                )

            if 'remove_block' in list_collector_block:
                list_item_context['remove_link'] = url_for(
                    'questionnaire.block',
                    list_name=list_name,
                    block_id=list_collector_block['remove_block']['id'],
                    list_item_id=list_item_id,
                    return_to=return_to,
                )

        list_items.append(list_item_context)

    return list_items


def build_list_collector_context(
    list_collector_block, schema, answer_store, list_store, language, form
):
    question_context = build_question_context(list_collector_block, form)
    list_collector_context = {
        'list': {
            'list_items': build_list_items_summary_context(
                list_collector_block, schema, answer_store, list_store, language
            ),
            'editable': True,
        }
    }

    return {**question_context, **list_collector_context}
