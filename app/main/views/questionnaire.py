import logging

from app import frontend_messages
from app.main.errors import internal_server_error
from app.main.errors import page_not_found
from app.main.errors import service_unavailable
from app.main.system_message import system_message
from app.metadata.metadata_store import MetaDataStore
from app.questionnaire.questionnaire_manager import InvalidLocationException
from app.questionnaire.questionnaire_manager_factory import QuestionnaireManagerFactory
from app.schema.questionnaire import QuestionnaireException
from app.submitter.submission_failed import SubmissionFailedException

from flask import redirect
from flask import request

from flask_login import current_user
from flask_login import login_required

from flask_themes2 import render_theme_template

from .. import main_blueprint

logger = logging.getLogger(__name__)


@main_blueprint.route('/questionnaire/<eq_id>/<form_type>/<period_id>/<collection_id>/<location>', methods=["GET", "POST"])
@login_required
def survey(eq_id, form_type, period_id, collection_id, location):

    logger.debug("Requesting location : /questionnaire/%s/%s/%s/%s/%s", eq_id, form_type, period_id, collection_id, location)
    try:

        questionnaire_manager = QuestionnaireManagerFactory.get_instance()

        # If the metadata doesn't match the current survey, multiple surveys must be open, which we don't support
        metadata = MetaDataStore.get_instance(current_user)
        current_survey = eq_id + form_type + period_id + collection_id
        metadata_survey = metadata.eq_id + metadata.form_type + metadata.period_id + metadata.collection_exercise_sid

        if not current_survey == metadata_survey:
            return system_message(frontend_messages.multiple_surveys)

        # Redirect to thank you page if the questionnaire has already been submitted
        if questionnaire_manager.submitted and location != 'thank-you':
            return do_redirect(eq_id, form_type, period_id, collection_id, 'thank-you')

        # redirect to the first block if the change your answers link is clicked
        if location == 'first' or location == 'previous':
            location = questionnaire_manager.resolve_location(location)
            questionnaire_manager.go_to(location)
            return do_redirect(eq_id, form_type, period_id, collection_id, location)

        # Process the POST request
        if request.method == 'POST':
            return do_post(collection_id, eq_id, form_type, period_id, location, questionnaire_manager)
        else:
            return do_get(questionnaire_manager, location)

    except QuestionnaireException as e:
        return page_not_found(e)
    except InvalidLocationException as e:
        return do_redirect(eq_id, form_type, period_id, collection_id, questionnaire_manager.get_current_location())
    except SubmissionFailedException as e:
        # Rabbit MQ connection issue
        return service_unavailable(e)
    except Exception as e:
        return internal_server_error(e)


def do_redirect(eq_id, form_type, period_id, collection_id,  location):
    return redirect('/questionnaire/' + eq_id + '/' + form_type + '/' + period_id + '/' + collection_id + '/' + location)


def do_get(questionnaire_manager, location):
    questionnaire_manager.go_to(location)
    context = questionnaire_manager.get_rendering_context(location)
    template = questionnaire_manager.get_rendering_template(location)

    # the special case where a get request modifies state
    if location == 'thank-you':
        questionnaire_manager.delete_user_data()

    try:
        theme = context['meta']['survey']['theme']
        logger.info("Theme selected: {} ".format(theme))
    except KeyError:
        logger.info("No theme set ")
        theme = None
    return render_theme_template(theme, template, meta=context['meta'], content=context['content'])


def do_post(collection_id, eq_id, form_type, period_id, location, questionnaire_manager):
    logger.debug("POST request question - current location %s", location)

    logger.debug("POST request length %s", request.content_length)

    questionnaire_manager.process_incoming_answers(location, request.form)
    next_location = questionnaire_manager.get_current_location()
    metadata = MetaDataStore.get_instance(current_user)
    logger.info("Redirecting user to next location %s with tx_id=%s", next_location, metadata.tx_id)
    return redirect('/questionnaire/' + eq_id + '/' + form_type + '/' + period_id + '/' + collection_id + '/' + next_location)
