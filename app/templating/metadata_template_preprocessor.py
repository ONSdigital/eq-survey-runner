import logging

from app.globals import get_metadata
from app.libs.utils import convert_tx_id
from app.utilities.date_utils import to_date

from flask_login import current_user

logger = logging.getLogger(__name__)


class MetaDataTemplatePreprocessor(object):

    def build_metadata(self, questionnaire_schema):
        render_data = {
            "survey": self._build_survey_meta(questionnaire_schema),
            "respondent": self._build_respondent_meta(),
        }
        return render_data

    @staticmethod
    def _build_respondent_meta():
        metadata = get_metadata(current_user)

        if metadata:
            respondent_id = metadata["ru_ref"]
            name = metadata["ru_name"]
            trading_as = metadata["trad_as"]
        else:
            respondent_id = None
            name = None
            trading_as = None

        respondent_meta = {
            "tx_id": convert_tx_id(metadata["tx_id"]),
            "respondent_id": respondent_id,
            "address": {
                "name": name,
                "trading_as": trading_as,
            },
        }
        return respondent_meta

    def _build_survey_meta(self, questionnaire_schema):
        introduction = questionnaire_schema['introduction']
        metadata = get_metadata(current_user)

        survey_meta = {
            "title": questionnaire_schema['title'],
            "survey_code": questionnaire_schema['survey_id'],
            "description": self._get_description(introduction),
            "information_to_provide": self._get_info_to_provide(introduction),
            "theme": questionnaire_schema['theme'],
            "return_by": self._format_date(metadata["return_by"]),
            "start_date":  self._format_date(metadata["ref_p_start_date"]),
            "end_date": self._format_date(metadata["ref_p_end_date"]),
            "employment_date": self._format_date(metadata["employment_date"]),
            "period_str": metadata["period_str"],
            "collection_id": metadata["collection_exercise_sid"],
            "eq_id": metadata["eq_id"],
            "form_type": metadata["form_type"],
            "period_id": metadata["period_id"],
        }
        return survey_meta

    @staticmethod
    def _get_info_to_provide(introduction):
        if introduction and introduction.get('information_to_provide') is not None:
            return introduction['information_to_provide']

        return None

    @staticmethod
    def _get_description(introduction):
        if introduction and introduction['description']:
            return introduction['description']

        return None

    @staticmethod
    def _format_date(input_date_string):
        formatted_date = to_date(input_date_string)

        if formatted_date:
            return '{dt.day} {dt:%B} {dt.year}'.format(dt=formatted_date)
        return None
