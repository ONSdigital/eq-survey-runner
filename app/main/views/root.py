from flask import render_template, redirect, request, abort, url_for
from flask_login import login_required
from .. import main_blueprint
from app.schema_loader.schema_loader import load_schema
from app.responses.response_store import ResponseStoreFactory
from app.validation.validation_store import ValidationStoreFactory
from app.parser.schema_parser_factory import SchemaParserFactory
from app.validation.validation_result import ValidationResult
from app.routing.routing_engine import RoutingEngine
from app.navigation.navigator import Navigator
from app.navigation.navigation_history import FlaskNavigationHistory
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.authentication.authenticator import Authenticator
from app.authentication.session_management import session_manager
from app.authentication.no_token_exception import NoTokenException
from app.authentication.invalid_token_exception import InvalidTokenException
from app.main import errors
import logging

logger = logging.getLogger(__name__)


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/cover-page', methods=['GET', 'POST'])
@login_required
def cover_page():
    return render_template('cover-page.html')


@main_blueprint.route('/submission', methods=['GET'])
@login_required
def submission():
    return render_template('submission.html')


@main_blueprint.route('/thank-you', methods=['GET'])
@login_required
def thank_you():
    return render_template('thank-you.html')


@main_blueprint.route('/session', methods=['GET'])
def login():
    """
    Initial url processing - expects a token parameter and then will authenticate this token. Once authenticated
    it will be placed in the users session
    :return: a 302 redirect to the cover page
    """
    authenticator = Authenticator()
    logger.debug("Attempting token authentication")
    try:
        token = authenticator.jwt_login(request)
        logger.debug("Token authenticated - linking to session")

        questionnaire_id = token.get("eq-id")
        logger.debug("Requested questionnaire %s", questionnaire_id)
        if not questionnaire_id:
            abort(404)

        session_manager.add_token(token)

        schema = load_and_parse_schema(questionnaire_id)

        # load the navigation history
        navigation_history = FlaskNavigationHistory()

        # create the navigator
        navigator = Navigator(schema, navigation_history)

        current_location = navigator.get_current_location()

        if current_location == "start":
            return redirect(url_for("main.cover_page"))
        elif current_location == "completed":
            return redirect(url_for("main.thank_you"))
        else:
            return redirect(url_for("main.questionnaire"))

    except NoTokenException as e:
        logger.warning("Unable to authenticate user")
        return errors.unauthorized(e)
    except InvalidTokenException as e:
        logger.warning("Invalid Token provided")
        return errors.forbidden(e)


@main_blueprint.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():
    token = session_manager.get_token()
    questionnaire_id = token.get("eq-id")
    logger.debug("Requested questionnaire %s", questionnaire_id)

    schema = load_and_parse_schema(questionnaire_id)

    # load the response store
    response_store = ResponseStoreFactory.create_response_store()

    # load the validation store
    validation_store = ValidationStoreFactory.create_validation_store()

    # Create the validator
    class Validator(object):
        def __init__(self, validation_store, schema):
            self._schema = schema
            self._validation_store = validation_store

        def validate(self, responses):
            for key, value in responses.items():
                self._validation_store.store_result(key, ValidationResult(True))

    validator = Validator(validation_store, schema)

    # Create the routing engine
    routing_engine = RoutingEngine(schema, response_store)

    # load the navigation history
    navigation_history = FlaskNavigationHistory()

    # create the navigator
    navigator = Navigator(schema, navigation_history)

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

        return redirect(request.path)

    render_data = questionnaire_manager.get_rendering_context()

    return render_template('questionnaire.html', questionnaire=render_data['schema'])


def load_and_parse_schema(questionnaire_id):
    # load the schema
    json_schema = load_schema(questionnaire_id)
    parser = SchemaParserFactory.create_parser(json_schema)
    schema = parser.parse()
    return schema
