import logging

from app.questionnaire.navigator import Navigator
from app.templating.summary.section import Section

logger = logging.getLogger(__name__)


def build_summary_rendering_context(schema_json, answer_store):
    """
    Build questionnaire summary context containing metadata and content from the answers of the questionnaire
    :param schema_json: schema of the current questionnaire
    :param answer_store: all of the answers to the questionnaire
    :return: questionnaire summary context
    """
    navigator = Navigator(schema_json, answer_store)
    path = navigator.get_routing_path()
    sections = []
    for group in schema_json['groups']:
        for block in group['blocks']:
            if block['id'] in [b['block_id'] for b in path]:
                if "type" not in block or block['type'] != "interstitial":
                    sections.extend([Section(group['id'], 0, block['id'], section, answer_store.map()) for section in block['sections']])
    return sections
