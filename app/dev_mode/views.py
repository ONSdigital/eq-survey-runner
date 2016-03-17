from flask import render_template, redirect, request
from app.authentication.encoder import Encoder
from app.authentication.user import USER_ID, RU_REF, RU_NAME, REF_P_START_DATE, REF_P_END_DATE, \
  COLLECTION_EXERCISE_SID, EQ_ID, FORM_TYPE, PERIOD_ID, PERIOD_STR
from . import dev_mode_blueprint
import os
import time


@dev_mode_blueprint.route('/dev', methods=['GET', 'POST'])
def dev_mode():
    if request.method == "POST":
        form = request.form
        user = form.get("user_id")
        exp_time = form.get("exp")
        eq_id = form.get("eq_id")
        period_str = form.get("period_str")
        period_id = form.get("period_id")
        form_type = form.get("form_type")
        collection_exercise_sid = form.get("collection_exercise_sid")
        ref_p_start_date = form.get("ref_p_start_date")
        ref_p_end_date = form.get("ref_p_end_date")
        ru_ref = form.get("ru_ref")
        ru_name = form.get("ru_name")

        payload = create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid,
                                 ref_p_start_date, ref_p_end_date, ru_ref, ru_name)
        return redirect("/session?token=" + generate_token(payload).decode())
    else:
        return render_template("dev-page.html", user=os.getenv('USER', 'UNKNOWN'))


def create_payload(user, exp_time, eq_id, period_str, period_id, form_type, collection_exercise_sid, ref_p_start_date,
                   ref_p_end_date, ru_ref, ru_name):
    iat = time.time()
    exp = time.time() + float(exp_time)
    return {
            USER_ID: user,
            'iat': str(int(iat)),
            'exp': str(int(exp)),
            EQ_ID: eq_id,
            PERIOD_STR: period_str,
            PERIOD_ID: period_id,
            FORM_TYPE: form_type,
            COLLECTION_EXERCISE_SID: collection_exercise_sid,
            REF_P_START_DATE: ref_p_start_date,
            REF_P_END_DATE: ref_p_end_date,
            RU_REF: ru_ref,
            RU_NAME: ru_name}


def generate_token(payload):
    encoder = Encoder()
    token = encoder.encode(payload)
    encrypted_token = encoder.encrypt(token)
    return encrypted_token
