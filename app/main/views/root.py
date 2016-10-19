import logging

from app.authentication.authenticator import Authenticator
from app.data_model.questionnaire_store import get_metadata
from app.frontend_messages import get_messages
from app.questionnaire.questionnaire_manager_factory import QuestionnaireManagerFactory

from flask import redirect
from flask import request
from flask import session
from flask import Blueprint

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
    period_id = metadata["period_id"]

    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)
    if not eq_id or not form_type:
        logger.error("Missing EQ id %s or form type %s in JWT", eq_id, form_type)
        raise NotFound

    questionnaire_manager = QuestionnaireManagerFactory.get_instance()

    # get the current location of the user
    current_location = questionnaire_manager.get_current_location()

    return redirect('/questionnaire/' + eq_id + '/' + form_type + '/' + period_id + '/' + collection_id + '/' + current_location)
