from collections import OrderedDict
from flask_login import current_user
from app.submitter.converter import SubmitterConstants
from flask import session
from app.piping.plumber import Plumber
from app.libs.utils import ObjectFromDict
from app.model.questionnaire import QuestionnaireException


class Renderer(object):
    def __init__(self, schema, answer_store, validation_store, navigator, metadata):
        self._schema = schema
        self._answer_store = answer_store
        self._validation_store = validation_store
        self._navigator = navigator
        self._metadata = metadata
        self._current_block = None
        self._current_group = None

        start_date = None
        end_date = None
        employment_date = None
        return_by = None

        try:
            start_date = self._metadata.get_ref_p_start_date()
            end_date = self._metadata.get_ref_p_end_date()
            employment_date = self._metadata.get_employment_date()
            return_by = self._metadata.get_return_by()

        except:
            pass

        # Get the current location or the first block
        try:
            self._current_block = self._schema.get_item_by_id(self._navigator.get_current_location())
        except QuestionnaireException:
            self._current_block = self._schema.get_item_by_id(self._navigator.get_first_block())

        # get the group
        self._current_group = self._current_block.container

        context = {
            "exercise": ObjectFromDict({
                "start_date": start_date,
                "end_date": end_date,
                "employment_date": employment_date,
                "return_by": return_by
            })
        }

        self._plumber = Plumber(context)

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

    def render(self):
        self._augment_questionnaire()

        render_data = {
            "meta": {
                "survey": self._render_survey_meta(),
                "respondent": self._render_respondent_meta()
            },
            "content": {
                "introduction": {},
                "questionnaire": self._schema,
                "summary": None,
                "thanks": None
            },
            "navigation": self._render_navigation_meta()
        }

        return render_data

    def _render_survey_meta(self):
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
            survey_meta["return_by"] = "{dt.day} {dt:%B} {dt.year}".format(dt=self._metadata.get_return_by())
            survey_meta["start_date"] = '{dt.day} {dt:%B} {dt.year}'.format(dt=self._metadata.get_ref_p_start_date())
            survey_meta["end_date"] = '{dt.day} {dt:%B} {dt.year}'.format(dt=self._metadata.get_ref_p_end_date())
            survey_meta["employment_date"] = '{dt.day} {dt:%B} {dt.year}'.format(dt=self._metadata.get_employment_date())
            survey_meta["period_str"] = self._metadata.get_period_str()
        except:
            # But we can silently ignore them under those circumstanes
            pass

        # TODO: This is still not the right place to do this...
        if session and SubmitterConstants.SUBMITTED_AT_KEY in session:
            survey_meta['submitted'] = True
            survey_meta['submitted_at'] = session[SubmitterConstants.SUBMITTED_AT_KEY]

        return survey_meta

    def _render_respondent_meta(self):
        respondent_meta = {
            "respondent_id": None,
            "address": {
                "name": None,
                "trading_as": None
            }
        }
        if current_user:
            respondent_meta["respondent_id"] = self._metadata.get_ru_ref()
            respondent_meta["address"]["name"] = self._metadata.get_ru_name()
            respondent_meta["address"]["trading_as"] = self._metadata.get_trad_as()

        return respondent_meta

    def _render_navigation_meta(self):
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
                self._augment_item(group, errors, warnings)
                for block in group.blocks:
                    # ...and the current block
                    if self._current_block.id == block.id:
                        self._augment_item(block, errors, warnings)
                        for section in block.sections:
                            self._augment_item(section, errors, warnings)
                            for question in section.questions:
                                self._augment_item(question, errors, warnings)
                                for answer in question.answers:
                                    self._augment_item(answer, errors, warnings)

        # We need to augment all the answer objects, regardless of the current
        # group/block as the summary page will otherwise fail
        for answer_id in self._answer_store.get_answers().keys():
            answer = self._schema.get_item_by_id(answer_id)
            self._augment_answer(answer)

        self._schema.errors = errors
        self._schema.warnings = warnings

    def _augment_item(self, item, global_errors, global_warnings):
        # Perform any plumbing of variables into displayed text
        self._plumber.plumb_item(item)

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
