import logging
import os
import time

from app.dev_mode.jwt_encoder import Encoder
from app.schema_loader.schema_loader import available_schemas

from flask import redirect
from flask import render_template
from flask import request
from flask import Blueprint


from werkzeug.exceptions import NotFound


# pylint: disable=too-many-locals
logger = logging.getLogger(__name__)
dev_mode_blueprint = Blueprint('dev_mode', __name__, template_folder='templates')


@dev_mode_blueprint.route('/dev', methods=['GET', 'POST'])
def dev_mode():
    if request.method == "POST":
        form = request.form
        user = form.get("user_id")
        exp_time = form.get("exp")
        schema = form.get("schema")
        eq_id, form_type = extract_eq_id_and_form_type(schema)
        period_str = form.get("period_str")
        period_id = form.get("period_id")
        collection_exercise_sid = form.get("collection_exercise_sid")
        ref_p_start_date = form.get("ref_p_start_date")
        ref_p_end_date = form.get("ref_p_end_date")
        ru_ref = form.get("ru_ref")
        ru_name = form.get("ru_name")
        trad_as = form.get("trad_as")
        return_by = form.get("return_by")
        employment_date = form.get("employment_date")
        region_code = form.get("region_code")
        sexual_identity = form.get("sexual_identity")
        variant_flags = {"sexual_identity": sexual_identity}
        payload = create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid,
                                 ref_p_start_date, ref_p_end_date, ru_ref, ru_name, trad_as, return_by, employment_date,
                                 region_code, variant_flags)
        return redirect("/session?token=" + generate_token(payload).decode())

    return render_template("dev-page.html", user=os.getenv('USER', 'UNKNOWN'), available_schemas=available_schemas())


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
        raise NotFound


def create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid, ref_p_start_date,
                   ref_p_end_date, ru_ref, ru_name, trad_as, return_by, employment_date, region_code, variant_flags):
    iat = time.time()
    exp = time.time() + float(exp_time)
    return {
        "user_id": user,
        'iat': str(int(iat)),
        'exp': str(int(exp)),
        "eq_id": eq_id,
        "period_str": period_str,
        "period_id": period_id,
        "form_type": form_type,
        "collection_exercise_sid": collection_exercise_sid,
        "ref_p_start_date": ref_p_start_date,
        "ref_p_end_date": ref_p_end_date,
        "ru_ref": ru_ref,
        "ru_name": ru_name,
        "return_by": return_by,
        "trad_as": trad_as,
        "employment_date": employment_date,
        "region_code": region_code,
        "variant_flags": variant_flags,
    }


def generate_token(payload):
    encoder = Encoder()
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt_token(token)
    return encrypted_token
