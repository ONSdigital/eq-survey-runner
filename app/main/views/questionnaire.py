import logging
from app.authentication.session_management import session_manager
from flask import render_template, request, session
from flask_login import login_required, current_user
from flask import redirect
from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.submitter.converter import SubmitterConstants
from .. import main_blueprint
from app.schema.questionnaire import QuestionnaireException
from app.main.errors import page_not_found


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
        questionnaire_manager.go_to_location(location)

        # Process the POST request
        if request.method == 'POST':
            logger.debug("POST request question - current location %s", location)
            questionnaire_manager.process_incoming_answers(request.form)
            next_location = questionnaire_manager.get_current_location()

            current_user.save()

            return redirect('/questionnaire/' + eq_id + '/' + collection_id + '/' + next_location)

        context = questionnaire_manager.get_rendering_context()
        template = questionnaire_manager.get_rendering_template()

        return render_template(template,
                               meta=context['meta'],
                               content=context['content'],
                               navigation=context['navigation']
                               )

    except QuestionnaireException:
        return page_not_found(404)


def delete_user_data():
    # once the survey has been submitted
    # delete all user data from the database
    current_user.delete_questionnaire_data()
    # and clear out the session state
    session_manager.clear()
