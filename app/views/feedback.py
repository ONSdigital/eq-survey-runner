from flask import Blueprint, redirect, url_for, escape, request, current_app, g
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from sdc.crypto.encrypter import encrypt
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired
from structlog import get_logger

from app.helpers import template_helper
from app.keys import KEY_PURPOSE_SUBMISSION
from app.submitter.submission_failed import SubmissionFailedException
from app.globals import get_metadata, get_session_store
from app.submitter.converter import convert_feedback
from app.utilities.schema import load_schema_from_session_data

logger = get_logger()

feedback_blueprint = Blueprint(name='feedback',
                               import_name=__name__,
                               url_prefix='/feedback')


class FeedbackForm(FlaskForm):
    message = TextAreaField('message', validators=[InputRequired()])
    name = StringField('name')
    email = StringField('email')


@feedback_blueprint.before_request
def before_request():
    logger.info('feedback request', url_path=request.full_path)

    session = get_session_store()
    if session:
        logger.bind(tx_id=session.session_data.tx_id)
        g.schema = load_schema_from_session_data(session.session_data)


@feedback_blueprint.route('', methods=['GET'])
@login_required
def get_form():
    form = FeedbackForm()
    content = {
        'csrf_token': form.csrf_token,
    }
    return _render_template('feedback', content=content)


@feedback_blueprint.route('', methods=['POST'])
@login_required
def send_feedback():

    if 'action[sign_out]' in request.form:
        return redirect(url_for('session.get_sign_out'))

    form = FeedbackForm()

    if form.validate():

        metadata = get_metadata(current_user)

        message = convert_feedback(
            escape(request.form.get('message')),
            escape(request.form.get('name')),
            escape(request.form.get('email')),
            request.referrer or '',
            metadata,
            g.schema.json['survey_id'],
        )

        encrypted_message = encrypt(message, current_app.eq['key_store'], key_purpose=KEY_PURPOSE_SUBMISSION)
        sent = current_app.eq['submitter'].send_message(encrypted_message, case_id=metadata.get('case_id'), tx_id=metadata.get('tx_id'))

        if not sent:
            raise SubmissionFailedException()

    if request.form.get('redirect', 'true') == 'true':
        return redirect(url_for('feedback.thank_you'))

    return '', 200


@feedback_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    return _render_template('feedback_sent')


@feedback_blueprint.route('/thank-you', methods=['POST'])
@login_required
def post_thank_you():
    if 'action[sign_out]' in request.form:
        return redirect(url_for('session.get_sign_out'))

    return redirect(url_for('feedback.thank_you'))


@template_helper.with_session_timeout
@template_helper.with_analytics
@template_helper.with_metadata_context
def _render_template(template, **kwargs):
    return template_helper.render_template(template, **kwargs)
