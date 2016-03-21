from flask import render_template, request
from flask_login import login_required, current_user
from .. import main_blueprint
from app.validation.validator import Validator
from app.routing.routing_engine import RoutingEngine
from app.navigation.navigator import Navigator
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.main import errors
from app.utilities.factory import factory
import logging
from app.main.views.root import _load_and_parse_schema
from app.main.views.root import _redirect_to_location


logger = logging.getLogger(__name__)


@main_blueprint.route('/questionnaire', methods=['GET', 'POST'])
@login_required
def questionnaire():

    logger.debug("Current user %s", current_user)

    eq_id = current_user.get_eq_id()
    form_type = current_user.get_form_type()
    logger.debug("Requested questionnaire %s for form type %s", eq_id, form_type)

    schema = _load_and_parse_schema(eq_id, form_type)
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

    return render_template('questionnaire.html', questionnaire=render_data, data={
        "survey_code": schema.survey_id,
        "period": current_user.get_period_str(),
        "respondent_id": current_user.get_ru_ref(),
    })
