import os
import re
import time
from uuid import uuid4

from flask import Blueprint, redirect, render_template, request, current_app
from structlog import get_logger

from app.cryptography.jwt_encoder import Encoder
from app.utilities.schema import available_json_schemas

# pylint: disable=too-many-locals
logger = get_logger()
dev_mode_blueprint = Blueprint('dev_mode', __name__, template_folder='templates')


@dev_mode_blueprint.route('/dev', methods=['GET', 'POST'])
def dev_mode():
    if request.method == "POST":
        form = request.form
        user_id = form.get("user_id")
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
        language_code = form.get("language_code")
        sexual_identity = form.get("sexual_identity") == "true"
        variant_flags = {"sexual_identity": sexual_identity}
        roles = ['dumper']
        payload = create_payload(user_id=user_id,
                                 exp_time=exp_time,
                                 eq_id=eq_id,
                                 period_str=period_str,
                                 period_id=period_id,
                                 form_type=form_type,
                                 collection_exercise_sid=collection_exercise_sid,
                                 ref_p_start_date=ref_p_start_date,
                                 ref_p_end_date=ref_p_end_date,
                                 ru_ref=ru_ref,
                                 ru_name=ru_name,
                                 trad_as=trad_as,
                                 return_by=return_by,
                                 employment_date=employment_date,
                                 region_code=region_code,
                                 language_code=language_code,
                                 variant_flags=variant_flags,
                                 roles=roles)

        return redirect("/session?token=" + generate_token(payload).decode())

    return render_template("dev-page.html", user=os.getenv('USER', 'UNKNOWN'), available_schemas=available_json_schemas())


@dev_mode_blueprint.route('/dev/flush', methods=['POST'])
def dev_flush_mode_post():
    form = request.form
    schema = form.get("schema")
    eq_id, form_type = extract_eq_id_and_form_type(schema)
    collection_exercise_sid = form.get("collection_exercise_sid")
    ru_ref = form.get("ru_ref")

    payload = {
        'iat': time.time(),
        'exp': time.time() + 1000,
        "eq_id": eq_id,
        "form_type": form_type,
        "collection_exercise_sid": collection_exercise_sid,
        "ru_ref": ru_ref,
        "roles": ["flusher"],
    }

    return redirect("/flush?token=" + generate_token(payload).decode())


@dev_mode_blueprint.route('/dev/flush', methods=['GET'])
def dev_flush_mode_get():
    return render_template("dev-flush-page.html", available_schemas=available_json_schemas())


def extract_eq_id_and_form_type(schema_name):
    logger.debug("extracting eq_id and form type from schema name", schema_name=schema_name)
    match = re.match(r"^([a-z0-9]+)_(\w+)\.json$", schema_name)
    if match:
        eq_id = match.group(1)
        form_type = match.group(2)
    else:
        raise ValueError('Schema filename incorrect format: %s', schema_name)
    logger.debug("parsed eq_id and form_type", eq_id=eq_id, form_type=form_type)
    return eq_id, form_type


def create_payload(**metadata):
    iat = time.time()
    exp = time.time() + float(metadata['exp_time'])

    payload = {
        'user_id': metadata['user_id'],
        'iat': str(int(iat)),
        'exp': str(int(exp)),
        'jti': str(uuid4()),
        'eq_id': metadata['eq_id'],
        'period_str': metadata['period_str'],
        'period_id': metadata['period_id'],
        'form_type': metadata['form_type'],
        'collection_exercise_sid': metadata['collection_exercise_sid'],
        'ref_p_start_date': metadata['ref_p_start_date'],
        'ru_ref': metadata['ru_ref'],
        'ru_name': metadata['ru_name'],
        'return_by': metadata['return_by'],
        'trad_as': metadata['trad_as'],
        'employment_date': metadata['employment_date'],
        'region_code': metadata['region_code'],
        'language_code': metadata['language_code'],
        'variant_flags': metadata['variant_flags'],
        'roles': metadata.get('roles', []),
    }
    if metadata.get('ref_p_end_date'):
        payload["ref_p_end_date"] = metadata['ref_p_end_date']
    return payload


def generate_token(payload):
    rrm_private_key = current_app.config['EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY']
    rrm_private_key_password = current_app.config['EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD']
    sr_public_key = current_app.config['EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY']
    encoder = Encoder(rrm_private_key, rrm_private_key_password, sr_public_key)
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt_token(token)
    return encrypted_token
