from flask import request, abort, session, redirect
from flask_login import current_user
from .. import main_blueprint
from app.schema_loader.schema_loader import load_schema
from app.parser.schema_parser_factory import SchemaParserFactory
from app.navigation.navigator import Navigator
from app.authentication.authenticator import Authenticator
from app.authentication.no_token_exception import NoTokenException
from app.authentication.invalid_token_exception import InvalidTokenException
from app.main import errors
from app.utilities.factory import factory
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

        metadata = factory.create("metadata-store")
        eq_id = metadata.get_eq_id()
        form_type = metadata.get_form_type()

        logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)
        if not eq_id or not form_type:
            logger.error("Missing EQ id %s or form type %s in JWT", eq_id, form_type)
            abort(404)

        # load the schema
        schema = load_and_parse_schema(eq_id, form_type)
        if not schema:
            return errors.page_not_found()

        # load the navigation history
        navigation_history = factory.create("navigation-history")

        # create the navigator
        navigator = Navigator(schema, navigation_history)

        # get the current location of the user
        current_location = navigator.get_current_location()

        current_user.save()

        return redirect('/questionnaire/' + current_location)

    except NoTokenException as e:
        logger.warning("Unable to authenticate user")
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        logger.warning("Invalid Token provided")
        return errors.forbidden(e)


def load_and_parse_schema(eq_id, form_type):
    """
    Use the schema loader to get the schema from disk. Then use the parse to construct the object model
    :param eq_id: the id of the questionnaire
    :param form_type: the form type
    :return: an object model
    """
    # load the schema

    json_schema = load_schema(eq_id, form_type)
    if json_schema:
        parser = SchemaParserFactory.create_parser(json_schema)
        schema = parser.parse()
        return schema
    else:
        return None
