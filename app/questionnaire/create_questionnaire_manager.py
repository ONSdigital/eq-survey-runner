from app.validation.validator import Validator
from app.routing.routing_engine import RoutingEngine
from app.navigation.navigator import Navigator
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.main import errors
from app.utilities.factory import factory
import logging
from app.main.views.root import load_and_parse_schema

logger = logging.getLogger(__name__)


def create_questionnaire_manager():

    metadata = factory.create("metadata-store")

    eq_id = metadata.get_eq_id()
    form_type = metadata.get_form_type()

    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    schema = load_and_parse_schema(eq_id, form_type)
    if not schema:
        return errors.page_not_found()

    # load the response store
    response_store = factory.create("response-store")

    # load the validation store
    validation_store = factory.create("validation-store")

    # Create the validator
    validator = Validator(schema, validation_store, response_store)

    # Create the routing engine
    routing_engine = RoutingEngine(schema, response_store)

    # load the navigation history
    navigation_history = factory.create("navigation-history")

    # create the navigator
    navigator = Navigator(schema, navigation_history)

    # if navigator.get_current_location() == "introduction" or navigator.get_current_location() is None:
    #     navigator.go_to('questionnaire')

    # instantiate the questionnaire manager
    questionnaire_manager = QuestionnaireManager(schema,
                                                 response_store,
                                                 validator,
                                                 validation_store,
                                                 routing_engine,
                                                 navigator,
                                                 navigation_history,
                                                 metadata)
    return questionnaire_manager
