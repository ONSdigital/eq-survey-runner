
from app.renderer.renderer import Renderer
from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response
from app.schema_loader import schema_loader


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
        """
        Temporary method to hard code a questionnaire model to get hamish started
        :param: json_schema this parameter will be converted to a question model
        :return: object model representing a schema
        """

        questionnaire = Questionnaire()
        questionnaire.id = "22"
        questionnaire.survey_id = "23"
        questionnaire.title = "Monthly Business Survey - Retail Sales Index"
        questionnaire.description = "MCI Description"

        group = Group()
        group.id = "14ba4707-321d-441d-8d21-b8367366e766"
        group.title = ""
        questionnaire.groups = [group]

        block = Block()
        block.id = "cd3b74d1-b687-4051-9634-a8f9ce10a27d"
        block.title = "Monthly Business Survey"
        group.blocks = [block]

        section = Section()
        section.id = "2cd99c83-186d-493a-a16d-17cb3c8bd302"
        section.title = ""
        block.sections = [section]

        question = Question()
        question.id = "4ba2ec8a-582f-4985-b4ed-20355deba55a"
        question.title = "On 12 January 2016 what was the number of employees for the business named above?"
        question.description = "An employee is anyone aged 16 years or over that your organisation directly " \
                               "pays from its payroll(s), in return for carrying out a full-time or part-time " \
                               "job or being on a training scheme."
        section.questions = [question]

        response = Response()
        response.id = "29586b4c-fb0c-4755-b67d-b3cd398cb30a"
        response.label = "Male employees working more than 30 hours per week?"
        response.guidance = "How many men work for your company?"
        response.type = "Integer"
        question.responses = [response]

        return questionnaire
