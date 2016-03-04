from flask.views import MethodView
from flask import render_template
from app.questionnaire.questionnaire_manager import QuestionnaireManager
from app.schema_loader.schema_loader import SchemaLoader

import logging


class QuestionnaireView(MethodView):

    def get(self, questionnaire_id):
        logging.debug("Get request for questionnaire %s", questionnaire_id)

        schema_loader = SchemaLoader()

        json_schema = schema_loader.load_schema(questionnaire_id)
        logging.debug("Schema loaded for %s is %s", questionnaire_id, json_schema)

        questionnaire_manager = QuestionnaireManager(json_schema)
        questionnaire_manager.process_incoming_response()
        rendering_context = questionnaire_manager.get_rendering_context()

        # TODO implement me!
        return render_template('questionnaire.html', questionnaire=rendering_context.get_model())

    def post(self):
        pass
