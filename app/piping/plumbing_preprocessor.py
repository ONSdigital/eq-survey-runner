from app.libs.utils import ObjectFromDict
from app.metadata.metadata_store import MetaDataStore
from app.piping.plumber import Plumber

from flask_login import current_user


class PlumbingPreprocessor(object):

    def plumb_current_state(self, questionnaire_manager, state, schema):
        piping_context = self._build_piping_context(questionnaire_manager, schema)

        plumber = Plumber(piping_context)

        self._plumb(plumber, state)

    def _plumb(self, plumber, state):
        # plumb the state and then all its children
        if state.schema_item:
            plumber.plumb_item(state.schema_item)
        for child in state.children:
            # recursively plumb each child
            self._plumb(plumber, child)

    def _build_piping_context(self, questionnaire_manager, schema):
        piping_context = {
            "exercise": self._build_exercise_piping_context(),
            "answers": self._build_answers_piping_context(questionnaire_manager, schema),
        }
        return piping_context

    def _build_exercise_piping_context(self):
        '''
        Build the exercise data from the survey metadata
        '''
        start_date = self._get_metadata().ref_p_start_date
        end_date = self._get_metadata().ref_p_end_date
        employment_date = self._get_metadata().employment_date
        return_by = self._get_metadata().return_by

        return ObjectFromDict({
            "start_date": start_date,
            "end_date": end_date,
            "employment_date": employment_date,
            "return_by": return_by,
        })

    def _build_answers_piping_context(self, questionnaire_manager, schema):
        '''
        Get the answer values for all aliased elements and make them available for piping.
        Where answers are not available, use an empty string
        '''
        aliases = schema.aliases
        values = {}
        for alias, item_id in aliases.items():
            value = questionnaire_manager.find_answer(item_id)
            if value is None:
                value = ""  # Empty string
            values[alias] = value
        return ObjectFromDict(values)

    def _get_metadata(self):
        return MetaDataStore.get_instance(current_user)
