import logging

from app.authentication.authenticator import Authenticator
from app.frontend_messages import get_messages

from app.globals import get_answer_store, get_completed_blocks, get_metadata
from app.questionnaire.navigator import Navigator
from app.utilities.schema import get_schema

from flask import redirect
from flask import request
from flask import session
from flask import Blueprint
from flask import url_for

from flask.ext.themes2 import render_theme_template

from flask_login import current_user

from werkzeug.exceptions import NotFound

logger = logging.getLogger(__name__)


root_blueprint = Blueprint('root', __name__)


@root_blueprint.after_request
def add_cache_control(response):
    response.cache_control.no_cache = True
    return response


@root_blueprint.route('/', methods=['GET'])
def root():
    raise NotFound


@root_blueprint.route('/information/<message_identifier>', methods=['GET'])
def information(message_identifier):
    front_end_message = get_messages(message_identifier)
    if front_end_message:
        logger.debug(front_end_message)
        return render_theme_template('default', 'information.html',
                                     messages=front_end_message)
    raise NotFound


@root_blueprint.route('/session', methods=['GET'])
def login():
    """
    Initial url processing - expects a token parameter and then will authenticate this token. Once authenticated
    it will be placed in the users session
    :return: a 302 redirect to the next location for the user
    """

    # logging in again clears any session state
    if session:
        session.clear()

    authenticator = Authenticator()
    logger.debug("Attempting token authentication")

    authenticator.jwt_login(request)
    logger.debug("Token authenticated - linking to session")

    metadata = get_metadata(current_user)

    eq_id = metadata["eq_id"]
    collection_id = metadata["collection_exercise_sid"]
    form_type = metadata["form_type"]

    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    if not eq_id or not form_type:
        logger.error("Missing EQ id %s or form type %s in JWT", eq_id, form_type)
        raise NotFound

    json, _ = get_schema(metadata)

    navigator = Navigator(json, metadata, get_answer_store(current_user))
    current_location = navigator.get_latest_location(get_completed_blocks(current_user))

    if current_location['block_id'] == 'introduction':
        return redirect(url_for('questionnaire.get_introduction',
                                eq_id=eq_id,
                                form_type=form_type,
                                collection_id=collection_id))
    elif current_location['block_id'] == 'summary':
        return redirect(url_for('questionnaire.get_summary',
                                eq_id=eq_id,
                                form_type=form_type,
                                collection_id=collection_id))
    elif current_location['block_id'] == 'thank-you':
        return redirect(url_for('questionnaire.get_thank_you',
                                eq_id=eq_id,
                                form_type=form_type,
                                collection_id=collection_id))
    elif current_location['block_id'] == 'confirmation':
        return redirect(url_for('questionnaire.get_confirmation',
                                eq_id=eq_id,
                                form_type=form_type,
                                collection_id=collection_id))

    return redirect(url_for('questionnaire.get_block',
                            eq_id=eq_id,
                            form_type=form_type,
                            collection_id=collection_id,
                            group_id=current_location['group_id'],
                            group_instance=current_location['group_instance'],
                            block_id=current_location['block_id']))
