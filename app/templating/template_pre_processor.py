from flask_login import current_user
from app.metadata.metadata_store import MetaDataStore
from app.piping.plumber import Plumber
from app.libs.utils import ObjectFromDict, convert_tx_id
import logging


logger = logging.getLogger(__name__)


KNOWN_TEMPLATES = {
            'introduction': "landing-page.html",
            'summary': "submission.html",
            'confirmation': "confirmation.html",
            'thank-you': 'thank-you.html'
}


class TemplatePreProcessor(object):
    def __init__(self, schema, user_journey_manager):
        self._schema = schema
        self.questionnaire_manager = user_journey_manager

    def get_template_name(self):
        current_location = self.questionnaire_manager.get_current_location()
        if current_location in KNOWN_TEMPLATES:
            return KNOWN_TEMPLATES[current_location]
        else:
            # must be a valid location to get this far, so must be within the
            # questionnaire
            return 'questionnaire.html'

    def build_view_data(self):
        # Always plumb the questionnaire
        self._plumb_questionnaire()

        # Collect the answers for all pages except the intro and thank you pages
        current_location = self.questionnaire_manager.get_current_location()
        if current_location != 'introduction' and current_location != 'thank-you':
            self._augment_questionnaire()

        render_data = {
            "meta": {
                "survey": self._build_survey_meta(),
                "respondent": self._build_respondent_meta()
            },
            "questionnaire": self._schema,
            "navigation": self._build_navigation_meta()
        }

        return render_data

    def _build_survey_meta(self):
        survey_meta = {
            "title": self._schema.title,
            "survey_code": self._schema.survey_id,
            "description": self._get_description(),
            "theme": self._schema.theme,
            "return_by": self._format_date(self._get_metadata().return_by),
            "start_date":  self._format_date(self._get_metadata().ref_p_start_date),
            "end_date": self._format_date(self._get_metadata().ref_p_end_date),
            "employment_date": self._format_date(self._get_metadata().employment_date),
            "period_str": self._get_metadata().period_str,
            "submitted_at": self.questionnaire_manager.submitted_at
        }
        return survey_meta

    def _get_description(self):
        if self._schema.introduction and self._schema.introduction.description:
            return self._schema.introduction.description
        else:
            return None

    @staticmethod
    def _format_date(date):
        formatted_date = None
        try:
            # employment date is optional this is why date is checked to see if exists
            if date:
                formatted_date = '{dt.day} {dt:%B} {dt.year}'.format(dt=date)
        except ValueError as e:
            logger.exception(e)
            logger.error("Error parsing meta data for %s", date)
        return formatted_date

    def _build_respondent_meta(self):
        if current_user:
            respondent_id = self._get_metadata().ru_ref
            name = self._get_metadata().ru_name
            trading_as = self._get_metadata().trad_as
        else:
            respondent_id = None
            name = None
            trading_as = None

        respondent_meta = {
            "tx_id": convert_tx_id(self._get_metadata().tx_id),
            "respondent_id": respondent_id,
            "address": {
                "name": name,
                "trading_as": trading_as
            }
        }
        return respondent_meta

    def _build_navigation_meta(self):
        current_location = self.questionnaire_manager.get_current_location()
        if self._schema.item_exists(current_location):
            current_block = self._schema.get_item_by_id(current_location)
            current_group = current_block.container
        else:
            current_block = None
            current_group = None

        navigation_meta = {
            "current_position": current_location,
            "current_block": current_block,
            "current_group": current_group
        }
        return navigation_meta

    def _augment_questionnaire(self):
        current_location = self.questionnaire_manager.get_current_location()

        # Check to see if we are on the submission page set by the JSON (default is summary)
        if current_location == self._schema.submission_page:
            location = self.questionnaire_manager._first

            while location.next_page:
                if self._schema.item_exists(location.item_id):
                    location_state = location.page_state
                    schema_item = self._schema.get_item_by_id(location.item_id)
                    schema_item.augment_with_state(location_state)
                location = location.next_page
        else:
            current_state = self.questionnaire_manager.get_state(current_location)

            # This now feels wrong, but I can't think of a better way of doing this without ripping apart the whole rendering pipeline
            schema_item = self._schema.get_item_by_id(current_state.item_id)
            schema_item.augment_with_state(current_state.page_state)

            self._schema.errors = schema_item.collect_errors()
            self._schema.warnings = schema_item.collect_warnings()

    def _plumb_questionnaire(self):
        piping_context = self._build_piping_context()

        plumber = Plumber(piping_context)

        # loops through the Schema and plumbs each item it finds
        for group in self._schema.groups:
            plumber.plumb_item(group)
            for block in group.blocks:
                plumber.plumb_item(block)
                for section in block.sections:
                    plumber.plumb_item(section)
                    for question in section.questions:
                        plumber.plumb_item(question)
                        for answer in question.answers:
                            plumber.plumb_item(answer)

    def _build_piping_context(self):
        piping_context = {
            "exercise": self._build_exercise_piping_context(),
            "answers": self._build_answers_piping_context()
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
            "return_by": return_by
        })

    def _build_answers_piping_context(self):
        '''
        Get the answer values for all aliased elements and make them available for piping.
        Where answers are not available, use an empty string
        '''
        aliases = self._schema.aliases
        values = {}
        for alias, item_id in aliases.items():
            value = self.questionnaire_manager.find_answer(item_id)
            if value is None:
                value = ""  # Empty string
            values[alias] = value
        return ObjectFromDict(values)

    def _get_metadata(self):
        return MetaDataStore.get_instance(current_user)
