import logging


from app.globals import get_answers, get_metadata
from app.piping.plumber import Plumber

from app.utilities.date_utils import to_date

from flask_login import current_user

logger = logging.getLogger(__name__)


def get_schema_template_context(questionnaire_manager, schema):
    '''
    :param questionnaire_manager: to retrieve answers
    :param schema:
    :return: context dict for schema variable substitution.
    '''
    return {
      "exercise": _build_exercise(),
      "answers": _build_answers(questionnaire_manager, schema),
    }


def _build_exercise():
    '''
    Build the exercise data from the survey metadata
    '''
    metadata = get_metadata(current_user)

    return {
        "start_date": to_date(metadata["ref_p_start_date"]),
        "end_date": to_date(metadata["ref_p_end_date"]),
        "employment_date": to_date(metadata["employment_date"]),
        "return_by": to_date(metadata["return_by"]),
    }


def _build_answers(questionnaire_manager, schema):
    '''
    Get the answer values for all aliased elements and make them available for piping.
    Where answers are not available, use an empty string
    '''
    aliases = schema.aliases
    values = {}
    for alias, item_id in aliases.items():
        value = get_answers(current_user).get(item_id)
        if value is None:
            value = ""  # Empty string
        values[alias] = value
    return values


class PlumbingPreprocessor(object):

    def plumb_current_state(self, questionnaire_manager, state, schema):
        piping_context = get_schema_template_context(questionnaire_manager, schema)

        plumber = Plumber(piping_context)

        self._plumb(plumber, state)

    def _plumb(self, plumber, state):
        # plumb the state and then all its children
        if state.schema_item:
            plumber.plumb_item(state.schema_item)
        for child in state.children:
            # recursively plumb each child
            self._plumb(plumber, child)
