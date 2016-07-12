from collections import OrderedDict
from flask_login import current_user
from app.submitter.converter import SubmitterConstants
from flask import session
from app.piping.plumber import Plumber
from app.libs.utils import ObjectFromDict
from app.schema.questionnaire import QuestionnaireException


class TemplatePreProcessor(object):
    def __init__(self, schema, answer_store, validation_store, navigator, metadata):
        self._schema = schema
        self._answer_store = answer_store
        self._validation_store = validation_store
        self._navigator = navigator
        self._metadata = metadata
        self._current_block = None
        self._current_group = None

        # Get the current location or the first block
        try:
            self._current_block = self._schema.get_item_by_id(self._navigator.get_current_location())
        except QuestionnaireException:
            self._current_block = self._schema.get_item_by_id(self._navigator.get_first_block())

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

        current_location = self._navigator.get_current_location()
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
        current_location = self._navigator.get_current_location()
        if current_location != 'introduction' and current_location != 'thank-you':
            self._collect_answers()

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

        # TODO: This is still not the right place to do this...
        if session and SubmitterConstants.SUBMITTED_AT_KEY in session:
            survey_meta['submitted'] = True
            survey_meta['submitted_at'] = session[SubmitterConstants.SUBMITTED_AT_KEY]

        return survey_meta

    def _build_respondent_meta(self):
        respondent_meta = {
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
            "current_position": self._navigator.get_current_location(),
            "current_block_id": None,
            "current_group_id": None
        }

        navigation_meta["current_block_id"] = self._current_block.id
        navigation_meta["current_group_id"] = self._current_group.id

        return navigation_meta

    def _augment_answer(self, answer):
        answer.value = None
        if answer.id in self._answer_store.get_answers().keys():
            answer.value = self._answer_store.get_answer(answer.id)

    def _augment_questionnaire(self):
        errors = OrderedDict()
        warnings = OrderedDict()

        # loops through the Schema and get errors and warnings in order
        # augments each item in the schema as required
        for group in self._schema.groups:
            # We only do this for the current group...
            if self._current_group.id == group.id:
                self._collect_errors(group, errors, warnings)
                for block in group.blocks:
                    # ...and the current block
                    if self._current_block.id == block.id:
                        self._collect_errors(block, errors, warnings)
                        for section in block.sections:
                            self._collect_errors(section, errors, warnings)
                            for question in section.questions:
                                self._collect_errors(question, errors, warnings)
                                for answer in question.answers:
                                    self._collect_errors(answer, errors, warnings)

        self._schema.errors = errors
        self._schema.warnings = warnings

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

    def _collect_answers(self):
        # Collect all the answers and add them to the schema
        for answer_id in self._answer_store.get_answers().keys():
            answer = self._schema.get_item_by_id(answer_id)
            self._augment_answer(answer)

    def _collect_errors(self, item, global_errors, global_warnings):
        item.is_valid = None
        item.errors = []
        item.warnings = []

        item_result = self._validation_store.get_result(item.id)

        if item_result:
            item.is_valid = item_result.is_valid
            if not item_result.is_valid:
                global_errors[item.id] = item_result.errors
                global_warnings[item.id] = item_result.warnings
                item.errors = item_result.get_errors()
                item.warnings = item_result.get_warnings()

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
            value = self._answer_store.get_answer(item_id)
            if value is None:
                value = ""  # Empty string

            values[alias] = value

        return ObjectFromDict(values)
