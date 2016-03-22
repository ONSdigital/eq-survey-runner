from flask import render_template, redirect, request, abort, url_for, session
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
    return render_template('index.html')


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
        user = authenticator.jwt_login(request)
        logger.debug("Token authenticated - linking to session")

        eq_id = user.get_eq_id()
        form_type = user.get_form_type()
        logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)
        if not eq_id or not form_type:
            logger.error("Missing EQ id %s or form type %s in JWT", eq_id, form_type)
            abort(404)

        # load the schema
        schema = _load_and_parse_schema()
        if not schema:
            return errors.page_not_found()

        # load the navigation history
        navigation_history = factory.create("navigation-history")

        # create the navigator
        navigator = Navigator(schema, navigation_history)

        # get the current location of the user
        current_location = navigator.get_current_location()

        return _redirect_to_location(current_location)

    except NoTokenException as e:
        logger.warning("Unable to authenticate user")
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        logger.warning("Invalid Token provided")
        return errors.forbidden(e)


def _redirect_to_location(current_location):
    """
    Issue a redirect to the next part of the questionnaire
    :param current_location: the current location in the questionnaire
    :return: flask redirect to the next page
    """

    if current_location == 'introduction':
        return redirect(url_for("main.cover_page"))
    elif current_location == "completed":
        return redirect(url_for("main.submission"))
    elif current_location == "submitted":
        return redirect(url_for("main.thank_you"))
    elif current_location == 'questionnaire':
        return redirect(url_for("main.questionnaire"))
    else:
        return errors.page_not_found()


def _load_and_parse_schema():
    """
    Use the schema loader to get the schema from disk. Then use the parse to construct the object model
    :param eq_id: the id of the questionnaire
    :param form_type: the form type
    :return: an object model
    """
    # load the schema

    json_schema = load_schema(current_user.get_eq_id(), current_user.get_form_type())
    if json_schema:
        parser = SchemaParserFactory.create_parser(json_schema)
        schema = parser.parse()
        return schema
    else:
        return errors.page_not_found()
