from app.navigation.navigator import Navigator
from app.navigation.navigation_history import NavigationHistory
from app.metadata.metadata_store import MetaDataStore
from tests.app.framework.sr_unittest import SurveyRunnerTestCase
from app.schema.questionnaire import Questionnaire
import unittest
from app.schema.group import Group
from app.schema.block import Block
from app.navigation.navigation_state import NavigationException
from app.routing.routing_engine import RoutingEngine


class NavigatorTest(SurveyRunnerTestCase):

    def test_get_current_location(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            group = Group()
            group.id = 'group-1'
            schema.register(group)
            block = Block()
            block.id = 'block-1'
            schema.register(block)
            group.add_block(block)
            schema.add_group(group)

            navigation_history = NavigationHistory()
            navigator = Navigator(schema, MetaDataStore(), navigation_history, RoutingEngine(schema))
            #  brand new session shouldn't have a current location
            self.assertEquals('block-1', navigator.get_current_location())

    def test_get_current_location_with_intro(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            schema.introduction = "anything"

            navigation_history = NavigationHistory()
            navigator = Navigator(schema, MetaDataStore(), navigation_history, RoutingEngine(schema))
            #  brand new session shouldn't have a current location
            self.assertEquals("introduction", navigator.get_current_location())

    def test_go_to(self):
        with self.application.test_request_context():
            schema = Questionnaire()
            group = Group()
            group.id = 'group-1'
            schema.register(group)
            block = Block()
            block.id = 'block-1'
            schema.register(block)
            group.add_block(block)
            schema.add_group(group)

            navigation_history = NavigationHistory()
            navigator = Navigator(schema, MetaDataStore(), navigation_history, RoutingEngine(schema))

            self.assertRaises(NavigationException, navigator.go_to, 'introduction')

            navigation_history = NavigationHistory()
            navigator = Navigator(schema, MetaDataStore(), navigation_history, RoutingEngine(schema))
            navigator.go_to("block-1")
            self.assertEquals("block-1", navigator.get_current_location())

            schema.introduction = {'description': 'Some sort of intro'}

            navigation_history = NavigationHistory()
            navigator = Navigator(schema, MetaDataStore(), navigation_history, RoutingEngine(schema))
            navigator.go_to("introduction")
            self.assertEquals("introduction", navigator.get_current_location())

if __name__ == '__main__':
    unittest.main()
