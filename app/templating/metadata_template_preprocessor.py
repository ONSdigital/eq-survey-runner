from flask_login import current_user
from app.metadata.metadata_store import MetaDataStore
from app.libs.utils import convert_tx_id
import logging

logger = logging.getLogger(__name__)


class MetaDataTemplatePreprocessor(object):

    def build_metadata(self, schema):
        render_data = {
            "survey": self._build_survey_meta(schema),
            "respondent": self._build_respondent_meta()
        }
        return render_data

    def _build_respondent_meta(self):
        if self._get_metadata():
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

    def _build_survey_meta(self, schema):
        survey_meta = {
            "title": schema.title,
            "survey_code": schema.survey_id,
            "description": self._get_description(schema),
            "theme": schema.theme,
            "return_by": self._format_date(self._get_metadata().return_by),
            "start_date":  self._format_date(self._get_metadata().ref_p_start_date),
            "end_date": self._format_date(self._get_metadata().ref_p_end_date),
            "employment_date": self._format_date(self._get_metadata().employment_date),
            "period_str": self._get_metadata().period_str
        }
        return survey_meta

    def _get_description(self, schema):
        if schema.introduction and schema.introduction.description:
            return schema.introduction.description
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

    def _get_metadata(self):
        return MetaDataStore.get_instance(current_user)
