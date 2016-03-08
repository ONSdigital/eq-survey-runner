from flask.views import MethodView
from flask import render_template
from flask.ext.login import login_required
from app.questionnaire.questionnaire_manager import QuestionnaireManager

import logging


class QuestionnaireView(MethodView):

    @login_required
    def get(self, questionnaire_id):
        logging.debug("Get request for questionnaire %s", questionnaire_id)

        questionnaire_manager = QuestionnaireManager()
        questionnaire_manager.process_incoming_response(questionnaire_id)
        rendering_context = questionnaire_manager.get_rendering_context()

        # TODO implement me!
        return render_template('questionnaire.html', questionnaire=rendering_context.get_model())

    def post(self):
        pass
