import logging
from app.authentication.session_management import session_manager
from flask import request, session
from flask_login import login_required, current_user
from flask import redirect
from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.submitter.converter import SubmitterConstants
from app.submitter.submission_failed import SubmissionFailedException
from .. import main_blueprint
from app.schema.questionnaire import QuestionnaireException
from app.main.errors import page_not_found, internal_server_error, service_unavailable
from flask_themes2 import render_theme_template
from app.metadata.metadata_store import MetaDataStore


logger = logging.getLogger(__name__)


@main_blueprint.route('/questionnaire/<eq_id>/<collection_id>/<location>', methods=["GET", "POST"])
@login_required
def survey(eq_id, collection_id, location):
    # Redirect to thankyou page if the questionnaire has already been submitted
    if SubmitterConstants.SUBMITTED_AT_KEY in session and location != 'thank-you':
        return redirect('/questionnaire/' + eq_id + '/' + collection_id + '/thank-you')

    questionnaire_manager = create_questionnaire_manager()

    if location == 'first':
        questionnaire_manager.go_to_first()
        return redirect('/questionnaire/' + eq_id + '/' + collection_id + '/' + questionnaire_manager.get_current_location())

    if location == 'thank-you':
        delete_user_data()

    try:
        # Go to the location in the url.
        # This will throw an exception if invalid
        # TODO this can go eventually it's crazy
        questionnaire_manager.go_to_location(location)

        # Process the POST request
        if request.method == 'POST':
            return do_post(collection_id, eq_id, location, questionnaire_manager)
        else:
            return do_get(questionnaire_manager, location)

    except QuestionnaireException as e:
        return page_not_found(e)
    except SubmissionFailedException as e:
        # Rabbit MQ connection issue
        return service_unavailable(e)
    except Exception as e:
        return internal_server_error(e)


def do_get(questionnaire_manager, location):
    questionnaire_manager.go_to_state(location)
    context = questionnaire_manager.get_rendering_context()
    template = questionnaire_manager.get_rendering_template()
    try:
        theme = context['meta']['survey']['theme']
        logger.info("Theme selected: {} ".format(theme))
    except KeyError:
        logger.info("No theme set ")
        theme = None
    return render_theme_template(theme, template, meta=context['meta'], content=context['content'], navigation=context['navigation'])


def do_post(collection_id, eq_id, location, questionnaire_manager):
    logger.debug("POST request question - current location %s", location)
    questionnaire_manager.process_incoming_answers(location, request.form)
    next_location = questionnaire_manager.get_current_location()
    current_user.save()
    metadata = MetaDataStore.get_instance(current_user)
    logger.info("Redirecting user to next location %s with tx_id=%s", next_location, metadata.tx_id)
    return redirect('/questionnaire/' + eq_id + '/' + collection_id + '/' + next_location)


def delete_user_data():
    # once the survey has been submitted
    # delete all user data from the database
    current_user.delete_questionnaire_data()
    # and clear out the session state
    session_manager.clear()
