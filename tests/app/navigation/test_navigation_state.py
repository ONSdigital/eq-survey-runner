from app.navigation.navigation_state import NavigationState
import unittest


class NavigationStateTest(unittest.TestCase):

    def test_to_dict(self):
        navigation_state = NavigationState()
        navigation_state.current_position = "start"
        self.assertEquals("start", navigation_state.to_dict()['current_position'])

    def test_from_dict(self):
        state = {"current_position": "start"}
        navigation_state = NavigationState()
        navigation_state.from_dict(state)
        self.assertEquals("start", navigation_state.current_position)


if __name__ == '__main__':
    unittest.main()
