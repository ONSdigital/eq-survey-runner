import logging
import os
import time

from app.dev_mode.jwt_encoder import Encoder
from app.parser.metadata_parser import MetadataConstants
from app.schema_loader.schema_loader import available_schemas

from flask import abort
from flask import redirect
from flask import render_template
from flask import request

from . import dev_mode_blueprint

logger = logging.getLogger(__name__)


@dev_mode_blueprint.route('/dev', methods=['GET', 'POST'])
def dev_mode():
    if request.method == "POST":
        form = request.form
        user = form.get(MetadataConstants.USER_ID.claim_id)
        exp_time = form.get("exp")
        schema = form.get("schema")
        eq_id, form_type = extract_eq_id_and_form_type(schema)
        period_str = form.get(MetadataConstants.PERIOD_STR.claim_id)
        period_id = form.get(MetadataConstants.PERIOD_ID.claim_id)
        collection_exercise_sid = form.get(MetadataConstants.COLLECTION_EXERCISE_SID.claim_id)
        ref_p_start_date = form.get(MetadataConstants.REF_P_START_DATE.claim_id)
        ref_p_end_date = form.get(MetadataConstants.REF_P_END_DATE.claim_id)
        ru_ref = form.get(MetadataConstants.RU_REF.claim_id)
        ru_name = form.get(MetadataConstants.RU_NAME.claim_id)
        trad_as = form.get(MetadataConstants.TRAD_AS.claim_id)
        return_by = form.get(MetadataConstants.RETURN_BY.claim_id)
        employment_date = form.get(MetadataConstants.EMPLOYMENT_DATE.claim_id)
        payload = create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid,
                                 ref_p_start_date, ref_p_end_date, ru_ref, ru_name, trad_as, return_by, employment_date)
        return redirect("/session?token=" + generate_token(payload).decode())
    else:
        return render_template("dev-page.html", user=os.getenv('USER', 'UNKNOWN'), MetaDataConstants=MetadataConstants,
                               available_schemas=available_schemas())


def extract_eq_id_and_form_type(schema_name):
    try:
        logger.debug("schema file name: %s", schema_name)
        if "_" in schema_name:
            split_schema_name = schema_name.split("_", 1)
            if len(split_schema_name) != 2:
                raise ValueError("Schema file name incorrect %", schema_name)
            eq_id = split_schema_name[0]
            split_rest_of_name = split_schema_name[1].split(".", 1)
            if len(split_rest_of_name) != 2:
                raise ValueError("Schema file name incorrect %", schema_name)
            form_type = split_rest_of_name[0]
        else:
            # No form type associated with
            eq_id = schema_name.split(".", 1)[0]
            form_type = "-1"
        logger.debug("eq-id: %s", eq_id)
        logger.debug("form_type: " + form_type)
        return eq_id, form_type
    except Exception as e:
        logger.exception(e)
        logger.error("Invalid schema file %s", schema_name)
        abort(404)


def create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid, ref_p_start_date,
                   ref_p_end_date, ru_ref, ru_name, trad_as, return_by, employment_date):
    iat = time.time()
    exp = time.time() + float(exp_time)
    return {
            MetadataConstants.USER_ID.claim_id: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            MetadataConstants.EQ_ID.claim_id: eq_id,
            MetadataConstants.PERIOD_STR.claim_id: period_str,
            MetadataConstants.PERIOD_ID.claim_id: period_id,
            MetadataConstants.FORM_TYPE.claim_id: form_type,
            MetadataConstants.COLLECTION_EXERCISE_SID.claim_id: collection_exercise_sid,
            MetadataConstants.REF_P_START_DATE.claim_id: ref_p_start_date,
            MetadataConstants.REF_P_END_DATE.claim_id: ref_p_end_date,
            MetadataConstants.RU_REF.claim_id: ru_ref,
            MetadataConstants.RU_NAME.claim_id: ru_name,
            MetadataConstants.RETURN_BY.claim_id: return_by,
            MetadataConstants.TRAD_AS.claim_id: trad_as,
            MetadataConstants.EMPLOYMENT_DATE.claim_id: employment_date}


def generate_token(payload):
    encoder = Encoder()
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt(token)
    return encrypted_token
