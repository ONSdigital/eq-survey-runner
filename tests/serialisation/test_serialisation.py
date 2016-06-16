import unittest
import json
from app.surveys.mci_0205 import mci_0205
from app.surveys.mci_0203 import mci_0203
from app.surveys.star_wars import star_wars

from app.parser.schema_parser_factory import SchemaParserFactory


class SerialisationTest(unittest.TestCase):

    def test_star_wars(self):
        self.serialisation(star_wars,'0_star_wars.json')

    def test_mci_0205(self):
        self.serialisation(mci_0205, '1_0205.json')

    def test_mci_203(self):
        self.serialisation(mci_0203, '1_0203.json')

    def serialisation(self, python_model,location):
        serialised = self.serialise_model(python_model)
        parsed = self.parse_schema(serialised)
        self.assertEquals(python_model, parsed)
        self.compare_manual_and_generated(parsed, location)

    def serialise_model(self, questionnaire):
        json_str = json.dumps(questionnaire.to_json())
        return json_str

    def parse_schema(self, schema):
        parser = SchemaParserFactory.create_parser(json.loads(schema))
        return parser.parse()

    def compare_manual_and_generated(self, from_code, location):
        with open('tests/app/data_manually_created/'+ location) as f:
            serialised = f.read()
        from_file = self.parse_schema(serialised)
        self.assertEquals(from_file, from_code)
