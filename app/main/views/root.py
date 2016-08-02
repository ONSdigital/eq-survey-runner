from flask import request, abort, session, redirect
from flask_login import current_user
from .. import main_blueprint

from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.authentication.authenticator import Authenticator
from app.authentication.no_token_exception import NoTokenException
from app.authentication.invalid_token_exception import InvalidTokenException
from app.main import errors
from app.metadata.metadata_store import MetaDataStore
import logging


logger = logging.getLogger(__name__)


@main_blueprint.route('/', methods=['GET'])
def root():
    return errors.index()


@main_blueprint.route('/session', methods=['GET'])
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
    try:
        authenticator.jwt_login(request)
        logger.debug("Token authenticated - linking to session")

        metadata = MetaDataStore.get_instance(current_user)
        eq_id = metadata.eq_id
        collection_id = metadata.collection_exercise_sid
        form_type = metadata.form_type

        logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)
        if not eq_id or not form_type:
            logger.error("Missing EQ id %s or form type %s in JWT", eq_id, form_type)
            abort(404)

        user_journey_manager = create_questionnaire_manager()

        # get the current location of the user
        current_location = user_journey_manager.get_current_location()

        current_user.save()

        return redirect('/questionnaire/' + eq_id + '/' + collection_id + '/' + current_location)

    except NoTokenException as e:
        logger.warning("Unable to authenticate user")
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        logger.warning("Invalid Token provided")
        return errors.forbidden(e)
    except RuntimeError as e:
        return errors.internal_server_error(e)
