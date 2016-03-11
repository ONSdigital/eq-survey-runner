from flask import render_template, json, redirect, request
from .. import main_blueprint
from app.schema_loader.schema_loader import load_schema
from app.responses.response_store import ResponseStoreFactory
from app.validation.validation_store import ValidationStoreFactory
from app.parser.schema_parser_factory import SchemaParserFactory
from app.validation.validation_result import ValidationResult
from app.routing.routing_engine import RoutingEngine
from app.navigation.navigator import Navigator
from app.navigation.navigation_history import NavigationHistory
from app.questionnaire.questionnaire_manager import QuestionnaireManager


@main_blueprint.route('/', methods=['GET'])
def root():
    return render_template('index.html')


@main_blueprint.route('/questionnaire/mci/', methods=['GET'])
def mci_survey():
    with main_blueprint.open_resource('../data/mci.json') as f:
        data = json.load(f)
    return render_template('questionnaire.html', questionnaire=data)


@main_blueprint.route('/cover-page', methods=['GET'])
def cover_page():
    return render_template('cover-page.html')


@main_blueprint.route('/questionnaire/<questionnaire_id>', methods=['GET', 'POST'])
def questionnaire(questionnaire_id):

    # load the schema
    json_schema = load_schema(questionnaire_id)
    parser = SchemaParserFactory.create_parser(json_schema)
    schema = parser.parse()

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
    navigation_history = NavigationHistory()

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
