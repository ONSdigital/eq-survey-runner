from app.navigation.navigation_state import NavigationContext
from app.parser.schema_parser_factory import SchemaParserFactory
import unittest
import json


class NavigationContextTest(unittest.TestCase):

    def setUp(self):
        schema_file = open('app/data/0_star_wars.json')
        schema = schema_file.read()
        schema = json.loads(schema)
        # create a parser
        parser = SchemaParserFactory.create_parser(schema)
        self.questionnaire = parser.parse()

    def test_to_dict(self):
        navigation_context = NavigationContext(self.questionnaire)
        self.assertEquals("introduction", navigation_context.to_dict()['current_position'])

    def test_from_dict(self):
        state = {"current_position": "introduction"}
        navigation_context = NavigationContext(self.questionnaire)
        navigation_context.from_dict(state)
        self.assertEquals("introduction", navigation_context.state.get_location())


if __name__ == '__main__':
    unittest.main()
