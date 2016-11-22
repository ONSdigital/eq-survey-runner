import logging

from app.libs.utils import convert_tx_id
from app.utilities.date_utils import to_date

logger = logging.getLogger(__name__)


def build_metadata_context(metadata):
    """
    :param metadata: user metadata
    :return: metadata context
    """
    render_data = {
        "survey": _build_survey_meta(metadata),
        "respondent": _build_respondent_meta(metadata),
    }
    return render_data


def _build_respondent_meta(metadata):
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


def _build_survey_meta(metadata):
    return {
        "return_by": to_date(metadata["return_by"]),
        "start_date":  to_date(metadata["ref_p_start_date"]),
        "end_date": to_date(metadata["ref_p_end_date"]),
        "employment_date": to_date(metadata["employment_date"]),
        "region_code": metadata["region_code"] if 'region_code' in metadata else None,
        "period_str": metadata["period_str"],
        "eq_id": metadata["eq_id"],
        "collection_id": metadata["collection_exercise_sid"],
        "form_type": metadata["form_type"],
    }
