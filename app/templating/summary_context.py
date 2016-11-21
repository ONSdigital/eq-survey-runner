import logging

from app.globals import get_navigator
from app.templating.summary.section import Section

logger = logging.getLogger(__name__)


def build_summary_rendering_context(schema_json, answers):
    """
    Build questionnaire summary context containing metadata and content from the answers of the questionnaire
    :param schema_json: schema of the current questionnaire
    :param answers: all of the answers to the questionnaire
    :return: questionnaire summary context
    """
    path = get_navigator(schema_json).get_routing_path(answers)
    sections = []
    for group in schema_json['groups']:
        for block in group['blocks']:
            if block['id'] in path:
                if "type" not in block or block['type'] != "interstitial":
                    sections.extend([Section(block['id'], section, answers) for section in block['sections']])
    return sections
