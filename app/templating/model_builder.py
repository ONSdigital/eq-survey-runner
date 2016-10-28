import logging

from app.globals import get_answers
from app.templating.metadata_template_preprocessor import MetaDataTemplatePreprocessor

from app.templating.summary.section import Section

from flask import g

from flask_login import current_user

logger = logging.getLogger(__name__)


def build_questionnaire_model(questionnaire_schema, state_item):
    '''
    :param questionnaire_schema: variable substituted questionnaire schema
    :param state_items:
    :param previous_location:
    :return: context dict for questionnaire page variable substitution.
    '''
    metadata_template_preprocessor = MetaDataTemplatePreprocessor()
    render_data = {
      "meta": metadata_template_preprocessor.build_metadata(questionnaire_schema),
      "content": state_item,
    }

    logger.debug("Rendering data is %s", render_data)

    return render_data


def build_summary_model(questionnaire_schema):
    '''
    :param questionnaire_schema: variable substituted questionnaire schema
    :param previous_location:
    :return: context dict for summary page variable substitution.
    '''
    metadata_template_preprocessor = MetaDataTemplatePreprocessor()

    render_data = {
      "meta": metadata_template_preprocessor.build_metadata(questionnaire_schema),
      "content": _build_summary(questionnaire_schema),
    }

    logger.debug("Rendering data is %s", render_data)

    return render_data


def _build_summary(questionnaire_schema):
    q_manager = g.questionnaire_manager
    answers = get_answers(current_user)
    path = q_manager.navigator.get_routing_path(answers)
    sections = []
    for group in questionnaire_schema['groups']:
        for block in group['blocks']:
            if block['id'] in path:
                sections.extend([Section(block['id'], section, answers) for section in block['sections']])
    return sections
