from flask import render_template, redirect, request, abort
from app.authentication.encoder import Encoder
from app.authentication.user import UserConstants
from app.schema_loader.schema_loader import available_schemas
from flask.ext.cors import cross_origin
from . import dev_mode_blueprint
import os
import time
import logging

logger = logging.getLogger(__name__)


@dev_mode_blueprint.route('/dev/render-template', methods=['POST'])
@cross_origin()
def template():
    payload = request.get_json()
    return render_template('partials/' + payload['template'] + '.html', **payload['data'])


@dev_mode_blueprint.route('/dev', methods=['GET', 'POST'])
def dev_mode():
    if request.method == "POST":
        form = request.form
        user = form.get(UserConstants.USER_ID)
        exp_time = form.get("exp")
        schema = form.get("schema")
        eq_id, form_type = extract_eq_id_and_form_type(schema)
        period_str = form.get(UserConstants.PERIOD_STR)
        period_id = form.get(UserConstants.PERIOD_ID)
        collection_exercise_sid = form.get(UserConstants.COLLECTION_EXERCISE_SID)
        ref_p_start_date = form.get(UserConstants.REF_P_START_DATE)
        ref_p_end_date = form.get(UserConstants.REF_P_END_DATE)
        ru_ref = form.get(UserConstants.RU_REF)
        ru_name = form.get(UserConstants.RU_NAME)
        trad_as = form.get(UserConstants.TRAD_AS)
        return_by = form.get(UserConstants.RETURN_BY)
        payload = create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid,
                                 ref_p_start_date, ref_p_end_date, ru_ref, ru_name, trad_as, return_by)
        return redirect("/session?token=" + generate_token(payload).decode())
    else:
        return render_template("dev-page.html", user=os.getenv('USER', 'UNKNOWN'), UserConstants=UserConstants,
                               available_schemas=available_schemas())


def extract_eq_id_and_form_type(schema_name):
    try:
        logger.debug("schema file name: %s", schema_name)
        split_schema_name = schema_name.split("_", 1)
        if len(split_schema_name) != 2:
            raise ValueError("Schema file name incorrect %", schema_name)
        eq_id = split_schema_name[0]
        logger.debug("eq-id: %s", eq_id)
        split_rest_of_name = split_schema_name[1].split(".", 1)
        if len(split_rest_of_name) != 2:
            raise ValueError("Schema file name incorrect %", schema_name)
        form_type = split_rest_of_name[0]
        logger.debug("form_type: " + form_type)
        return eq_id, form_type
    except Exception as e:
        logger.exception("Invalid schema file %s", schema_name, e)
        abort(404)


def create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid, ref_p_start_date,
                   ref_p_end_date, ru_ref, ru_name, trad_as, return_by):
    iat = time.time()
    exp = time.time() + float(exp_time)
    return {
            UserConstants.USER_ID: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            UserConstants.EQ_ID: eq_id,
            UserConstants.PERIOD_STR: period_str,
            UserConstants.PERIOD_ID: period_id,
            UserConstants.FORM_TYPE: form_type,
            UserConstants.COLLECTION_EXERCISE_SID: collection_exercise_sid,
            UserConstants.REF_P_START_DATE: ref_p_start_date,
            UserConstants.REF_P_END_DATE: ref_p_end_date,
            UserConstants.RU_REF: ru_ref,
            UserConstants.RU_NAME: ru_name,
            UserConstants.RETURN_BY: return_by,
            UserConstants.TRAD_AS: trad_as}


def generate_token(payload):
    encoder = Encoder()
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt(token)
    return encrypted_token
