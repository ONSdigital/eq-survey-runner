from flask import Blueprint, redirect, url_for, escape, request, current_app, g
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired

from app.helpers import template_helper
from app.submitter.encrypter import encrypt
from app.submitter.submission_failed import SubmissionFailedException
from app.globals import get_metadata
from app.submitter.converter import convert_feedback
from app.utilities.schema import load_schema_from_metadata

from structlog import get_logger

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
    metadata = get_metadata(current_user)
    if metadata:
        logger.bind(tx_id=metadata['tx_id'])
        g.schema_json = load_schema_from_metadata(metadata)


@feedback_blueprint.route('', methods=['GET'])
@login_required
def get_form():
    form = FeedbackForm()
    return _render_template('feedback', form=form)


@feedback_blueprint.route('', methods=['POST'])
@login_required
def send_feedback():
    form = FeedbackForm()

    if form.validate():

        metadata = get_metadata(current_user)

        message = convert_feedback(
            escape(request.form.get('message')),
            escape(request.form.get('name')),
            escape(request.form.get('email')),
            request.referrer or '',
            metadata,
            g.schema_json['survey_id'],
        )

        encrypted_message = encrypt(message, current_app.eq['secret_store'])
        sent = current_app.eq['submitter'].send_message(encrypted_message,
                                                        current_app.config['EQ_RABBITMQ_QUEUE_NAME'],
                                                        metadata['tx_id'])

        if not sent:
            raise SubmissionFailedException()

    return redirect(url_for('feedback.thank_you'))


@feedback_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    return _render_template('feedback_sent')


@template_helper.with_session_timeout
@template_helper.with_analytics
@template_helper.with_metadata
def _render_template(template, **kwargs):
    return template_helper.render_template(template, **kwargs)
