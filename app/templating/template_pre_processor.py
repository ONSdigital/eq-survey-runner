from flask_login import current_user
from app.piping.plumber import Plumber
from app.libs.utils import ObjectFromDict, convert_tx_id
from app.schema.questionnaire import QuestionnaireException
import logging


logger = logging.getLogger(__name__)


class TemplatePreProcessor(object):
    def __init__(self, schema, user_journey_manager, metadata):
        self._schema = schema
        self._user_journey_manager = user_journey_manager
        self._metadata = metadata
        self._current_block = None
        self._current_group = None
        self._plumber = None

    def initialize(self):

        # Get the current location or the first block
        try:
            self._current_block = self._schema.get_item_by_id(self._user_journey_manager.get_current_location())
        except QuestionnaireException:
            self._current_block = self._schema.get_item_by_id(self._schema.groups[0].blocks[0].id)

        # get the group
        self._current_group = self._current_block.container

        piping_context = self._build_piping_context()

        self._plumber = Plumber(piping_context)

    def get_template_name(self):
        known_templates = {
            'introduction': "landing-page.html",
            'summary': "submission.html",
            'thank-you': 'thank-you.html'
        }

        current_location = self._user_journey_manager.get_current_location()
        if current_location in known_templates.keys():
            return known_templates[current_location]
        else:
            # must be a valid location to get this far, so must be within the
            # questionnaire
            return 'questionnaire.html'

    def build_view_data(self):
        # Always plumb the questionnaire
        self._plumb_questionnaire()

        # Collect the answers for all pages except the intro and thank you pages
        current_location = self._user_journey_manager.get_current_location()
        if current_location != 'introduction' and current_location != 'thank-you':

            # We only need to augment the questionnaire if we are still inside it
            if current_location != 'summary':
                self._augment_questionnaire()

        render_data = {
            "meta": {
                "survey": self._build_survey_meta(),
                "respondent": self._build_respondent_meta()
            },
            "content": {
                "introduction": {},
                "questionnaire": self._schema,
                "summary": None,
                "thanks": None
            },
            "navigation": self._build_navigation_meta()
        }

        return render_data

    def _build_survey_meta(self):
        survey_meta = {
            "title": self._schema.title,
            "survey_code": self._schema.survey_id,
            "description": None,
            "theme": self._schema.theme,
            "return_by": None,
            "start_date": None,
            "end_date": None,
            "employment_date": None,
            "period_str": None
        }

        if self._schema.introduction and self._schema.introduction.description:
            survey_meta["description"] = self._schema.introduction.description

        try:
            # Under certain conditions, there is no user so these steps may fail
            survey_meta["return_by"] = "{dt.day} {dt:%B} {dt.year}".format(dt=self._metadata.return_by)
            survey_meta["start_date"] = '{dt.day} {dt:%B} {dt.year}'.format(dt=self._metadata.ref_p_start_date)
            survey_meta["end_date"] = '{dt.day} {dt:%B} {dt.year}'.format(dt=self._metadata.ref_p_end_date)
            survey_meta["employment_date"] = '{dt.day} {dt:%B} {dt.year}'.format(dt=self._metadata.employment_date)
            survey_meta["period_str"] = self._metadata.period_str
        except:
            # But we can silently ignore them under those circumstanes
            pass

        if self._user_journey_manager.submitted_at:
            logger.debug("Template pre-processor submitted at %s", self._user_journey_manager.submitted_at)
            survey_meta['submitted'] = True
            survey_meta['submitted_at'] = self._user_journey_manager.submitted_at

        return survey_meta

    def _build_respondent_meta(self):
        respondent_meta = {
            "tx_id": convert_tx_id(self._metadata.tx_id),
            "respondent_id": None,
            "address": {
                "name": None,
                "trading_as": None
            }
        }
        if current_user:
            respondent_meta["respondent_id"] = self._metadata.ru_ref
            respondent_meta["address"]["name"] = self._metadata.ru_name
            respondent_meta["address"]["trading_as"] = self._metadata.trad_as

        return respondent_meta

    def _build_navigation_meta(self):
        navigation_meta = {
            "history": None,
            "current_position": self._user_journey_manager.get_current_location(),
            "current_block_id": None,
            "current_group_id": None
        }

        navigation_meta["current_block_id"] = self._current_block.id
        navigation_meta["current_group_id"] = self._current_group.id

        return navigation_meta

    def _augment_answer(self, answer):
        answer.value = self._user_journey_manager.get_answer(answer.id)

    def _augment_questionnaire(self):
        current_location = self._user_journey_manager.get_current_location()
        current_state = self._user_journey_manager.get_state(current_location)

        # This now feels wrong, but I can't think of a better way of doing this without ripping apart the whole rendering pipeline
        schema_item = self._schema.get_item_by_id(current_state.item_id)
        schema_item.augment_with_state(current_state.page_state)

        self._schema.errors = schema_item.collect_errors()
        self._schema.warnings = schema_item.collect_warnings()

    def _plumb_questionnaire(self):
        # loops through the Schema and plumbs each item it finds
        for group in self._schema.groups:
            self._plumber.plumb_item(group)
            for block in group.blocks:
                self._plumber.plumb_item(block)
                for section in block.sections:
                    self._plumber.plumb_item(section)
                    for question in section.questions:
                        self._plumber.plumb_item(question)
                        for answer in question.answers:
                            self._plumber.plumb_item(answer)

    def _build_piping_context(self):
        piping_context = {
            "exercise": self._build_exercse_piping_context(),
            "answers": self._build_answers_piping_context()
        }

        return piping_context

    def _build_exercse_piping_context(self):
        '''
        Build the exercise data from the survey metadata
        '''
        start_date = self._metadata.ref_p_start_date
        end_date = self._metadata.ref_p_end_date
        employment_date = self._metadata.employment_date
        return_by = self._metadata.return_by

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
            # TODO remove this try except
            try:
                value = self._user_journey_manager.get_answer(item_id)
            except AttributeError:
                value = None
            if value is None:
                value = ""  # Empty string

            values[alias] = value

        return ObjectFromDict(values)
