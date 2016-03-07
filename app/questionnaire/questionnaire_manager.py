
from app.renderer.renderer import Renderer
from app.schema_loader import schema_loader
from app.parser.schema_parser_factory import SchemaParserFactory

import logging


class QuestionnaireManager(object):
    def __init__(self):
        self._rendering_context = None

    def process_incoming_response(self, questionnaire_id):
        # get this value from settings
        json_schema = schema_loader.load_schema(questionnaire_id)
        logging.debug("Schema loaded for %s is %s", questionnaire_id, json_schema)

        # model comes from the schema parser when it's ready
        model = self.create_model(json_schema)
        logging.debug("Constructed model %s", model)

        renderer = Renderer()
        self._rendering_context = renderer.render(model)
        logging.debug("Rendered context")

    def get_rendering_context(self):
        return self._rendering_context

    def create_model(self, json_schema):
        parser = SchemaParserFactory.create_parser(json_schema)
        return parser.parse()
