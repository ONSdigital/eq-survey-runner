import unittest
import json

from app.model.questionnaire import Questionnaire
from app.model.group import Group
from app.model.block import Block
from app.model.section import Section
from app.model.question import Question
from app.model.response import Response

from app.surveys.mci.mci_0205 import mci_0205

from app.parser.schema_parser_factory import SchemaParserFactory


class SerialisationTest(unittest.TestCase):
    def test_serialisation(self):
        model = self.create_model()
        serialised = self.serialise_model(model)
        parsed = self.parse_schema(serialised)

        self.assertEquals(model, parsed)

    def create_model(self):
        return mci_0205

    def serialise_model(self, questionnaire):
        json_str = json.dumps(questionnaire.to_json())
        return json_str

    def parse_schema(self, schema):
        parser = SchemaParserFactory.create_parser(json.loads(schema))
        return parser.parse()
