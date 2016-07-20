from app.validation.validator import Validator
from app.questionnaire_state.user_journey_manager import UserJourneyManager
from app.routing.routing_engine import RoutingEngine
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.main import errors
from app.utilities.factory import factory
from app.metadata.metadata_store import MetaDataStore
from flask_login import current_user
import logging
from app.main.views.root import load_and_parse_schema

logger = logging.getLogger(__name__)


def create_questionnaire_manager():

    metadata = MetaDataStore.get_instance(current_user)

    eq_id = metadata.eq_id
    form_type = metadata.form_type

    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    schema = load_and_parse_schema(eq_id, form_type)
    if not schema:
        return errors.page_not_found()

    # load the validation store
    validation_store = factory.create("validation-store")

    user_journey_manager = UserJourneyManager.get_instance()
    if not user_journey_manager:
        logger.debug("Constructing brand new User Journey Manager")
        user_journey_manager = UserJourneyManager.new_instance(schema)
    # Create the validator
    validator = Validator(schema, validation_store, user_journey_manager)

    # Create the routing engine
    routing_engine = RoutingEngine(schema)

    # instantiate the questionnaire manager
    questionnaire_manager = QuestionnaireManager(schema,
                                                 user_journey_manager,
                                                 validator,
                                                 validation_store,
                                                 routing_engine,
                                                 metadata)
    return questionnaire_manager
