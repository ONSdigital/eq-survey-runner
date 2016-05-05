import logging
from flask import render_template, request, session
from flask_login import login_required, current_user
from app.utilities.factory import factory
from app.main.views.root import redirect_to_location
from flask import render_template, request, session, redirect
from flask_login import login_required
from app.questionnaire.create_questionnaire_manager import create_questionnaire_manager
from app.submitter.converter import SubmitterConstants
from .. import main_blueprint
from werkzeug.exceptions import NotFound
from app.navigation.navigator import NavigationException


logger = logging.getLogger(__name__)


@main_blueprint.route('/questionnaire/<location>', methods=["GET", "POST"])
@login_required
def survey(location):
    # Redirect to thankyou page if the questionnaire has already been submitted
    if SubmitterConstants.SUBMITTED_AT_KEY in session and location != 'thank-you':
        return redirect('/questionnaire/thank-you')

    questionnaire_manager = create_questionnaire_manager()

    try:
        # Go to the location in the url.
        # This will throw an exception if invalid
        questionnaire_manager.go_to_location(location)

        # Process the POST request
        if request.method == 'POST':
            logger.debug("POST request question - current location %s", location)
            questionnaire_manager.process_incoming_responses(request.form)
            next_location = questionnaire_manager.get_current_location()

            return redirect('/questionnaire/' + next_location)

        context = questionnaire_manager.get_rendering_context()
        template = questionnaire_manager.get_rendering_template()

        return render_template(template,
                               meta=context['meta'],
                               content=context['content'],
                               navigation=context['navigation']
                               )

    except NavigationException:
        raise NotFound()
