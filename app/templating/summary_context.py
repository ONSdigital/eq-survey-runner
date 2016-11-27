import logging

from app.questionnaire.navigator import Navigator
from app.templating.summary.section import Section

from flask import url_for

logger = logging.getLogger(__name__)


def build_summary_rendering_context(schema_json, answer_store, metadata):
    """
    Build questionnaire summary context containing metadata and content from the answers of the questionnaire
    :param schema_json: schema of the current questionnaire
    :param answer_store: all of the answers to the questionnaire
    :param metadata: all of the metadata
    :return: questionnaire summary context
    """
    navigator = Navigator(schema_json, metadata, answer_store)
    path = navigator.get_routing_path()
    sections = []
    for group in schema_json['groups']:
        for block in group['blocks']:
            if block['id'] in [b['block_id'] for b in path]:
                if "type" not in block or block['type'] != "interstitial":
                    link = url_for('questionnaire.get_block',
                                   eq_id=metadata['eq_id'],
                                   form_type=metadata['form_type'],
                                   collection_id=metadata['collection_exercise_sid'],
                                   group_id=group['id'],
                                   group_instance=0,
                                   block_id=block['id'])
                    sections.extend([Section(section, answer_store.map(), link) for section in block['sections']])
    return sections
