from flask import render_template, redirect, request, abort, url_for
from flask_login import login_required, current_user
from .. import main_blueprint
from app.schema_loader.schema_loader import load_schema
from app.responses.response_store import ResponseStoreFactory
from app.validation.validation_store import ValidationStoreFactory
from app.parser.schema_parser_factory import SchemaParserFactory
from app.validation.validator import Validator
from app.routing.routing_engine import RoutingEngine
from app.navigation.navigator import Navigator
from app.navigation.navigation_history import FlaskNavigationHistory
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.authentication.authenticator import Authenticator
from app.authentication.no_token_exception import NoTokenException
from app.authentication.invalid_token_exception import InvalidTokenException
from app.submitter.submitter import Submitter
from app.main import errors
import logging

logger = logging.getLogger(__name__)


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/cover-page', methods=['GET', 'POST'])
@login_required
def cover_page():
    logger.debug("Requesting cover page")
    return render_template('cover-page.html')


@main_blueprint.route('/submission', methods=['GET'])
@login_required
def submission():
    logger.debug("Requesting submission page")
    return render_template('submission.html')


@main_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    logger.debug("Requesting thank you page")

    # load the response store
    response_store = ResponseStoreFactory.create_response_store()

    submitter = Submitter()
    submitter.send(response_store.get_responses())
    return render_template('thank-you.html')


@main_blueprint.route('/session', methods=['GET'])
def login():
    """
    Initial url processing - expects a token parameter and then will authenticate this token. Once authenticated
    it will be placed in the users session
    :return: a 302 redirect to the next location for the user
    """
    authenticator = Authenticator()
    logger.debug("Attempting token authentication")
    try:
        token = authenticator.jwt_login(request)
        logger.debug("Token authenticated - linking to session")

        questionnaire_id = token.get("eq-id")
        logger.debug("Requested questionnaire %s", questionnaire_id)
        if not questionnaire_id:
            logger.error("Missing EQ id in JWT %s", token)
            abort(404)

        # load the schema
        schema = _load_and_parse_schema(questionnaire_id)

        # load the navigation history
        navigation_history = FlaskNavigationHistory()

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


@main_blueprint.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():

    logger.debug("Current user %s", current_user)

    questionnaire_id = current_user.get_eq_id()
    logger.debug("Requested questionnaire %s", questionnaire_id)

    schema = _load_and_parse_schema(questionnaire_id)

    # load the response store
    response_store = ResponseStoreFactory.create_response_store()

    # load the validation store
    validation_store = ValidationStoreFactory.create_validation_store()

    # Create the validator
    validator = Validator(schema, validation_store, response_store)

    # Create the routing engine
    routing_engine = RoutingEngine(schema, response_store)

    # load the navigation history
    navigation_history = FlaskNavigationHistory()

    # create the navigator
    navigator = Navigator(schema, navigation_history)
    if navigator.get_current_location() is None:
        navigator.go_to('questionnaire')

    # instantiate the questionnaire manager
    questionnaire_manager = QuestionnaireManager(schema,
                                                 response_store,
                                                 validator,
                                                 validation_store,
                                                 routing_engine,
                                                 navigator,
                                                 navigation_history)

    if request.method == 'POST':
        questionnaire_manager.process_incoming_responses(request.form)
        current_location = navigator.get_current_location()
        logger.debug("POST request question - current location %s", current_location)

        return _redirect_to_location(current_location)

    render_data = questionnaire_manager.get_rendering_context()

    return render_template('questionnaire.html', questionnaire=render_data)


def _redirect_to_location(current_location):
    """
    Issue a redirect to the next part of the questionnaire
    :param current_location: the current location in the questionnaire
    :return: flask redirect to the next page
    """
    if current_location is None:
        return redirect(url_for("main.cover_page"))
    elif current_location == "completed":
        return redirect(url_for("main.thank_you"))
    else:
        return redirect(url_for("main.questionnaire"))


def _load_and_parse_schema(questionnaire_id):
    """
    Use the schema loader to get the schema from disk. Then use the parse to construct the object model
    :param questionnaire_id: the id of the questionnaire
    :return: an object model
    """
    # load the schema
    json_schema = load_schema(questionnaire_id)
    parser = SchemaParserFactory.create_parser(json_schema)
    schema = parser.parse()
    return schema
