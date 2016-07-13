from app.questionnaire_state.user_journey_manager import UserJourneyManager
from app.questionnaire_state.page import Page

import unittest


class TestUserJourneyManager(unittest.TestCase):

    def test_append(self):
        user_journey_manager = UserJourneyManager(None)

        page1 = Page("first", None)
        page2 = Page("second", None)
        page3 = Page("third", None)

        self.assertIsNone(user_journey_manager._current)
        self.assertIsNone(user_journey_manager._first)
        user_journey_manager._append(page1)

        self.assertEqual(page1, user_journey_manager._first)
        self.assertEqual(page1, user_journey_manager._current)
        self.assertIsNone(page1.previous_page)
        self.assertIsNone(page1.next_page)

        user_journey_manager._append(page2)
        self.assertEqual(page1, user_journey_manager._first)
        self.assertEqual(page2, user_journey_manager._current)
        self.assertIsNone(page1.previous_page)
        self.assertEqual(page1.next_page, page2)
        self.assertEqual(page2.previous_page, page1)
        self.assertIsNone(page2.next_page)

        user_journey_manager._append(page3)
        self.assertEqual(page1, user_journey_manager._first)
        self.assertEqual(page3, user_journey_manager._current)
        self.assertEqual(page2.previous_page, page1)
        self.assertEqual(page2.next_page, page3)
        self.assertEqual(page3.previous_page, page2)
        self.assertIsNone(page3.next_page)

    def test_pop(self):
        user_journey_manager = UserJourneyManager(None)

        page1 = Page("first", None)
        page2 = Page("second", None)
        page3 = Page("third", None)
        page4 = Page("fourth", None)

        user_journey_manager._append(page1)
        user_journey_manager._append(page2)
        user_journey_manager._append(page3)
        user_journey_manager._append(page4)

        self.assertEqual(page1, user_journey_manager._first)
        self.assertEqual(page4, user_journey_manager._current)

        popped = user_journey_manager._pop()
        self.assertEqual(page4, popped)
        self.assertIsNone(popped.previous_page)
        self.assertIsNone(popped.next_page)
        self.assertEqual(page3, user_journey_manager._current)
        self.assertIsNone(page3.next_page)

    def test_truncate(self):
        user_journey_manager = UserJourneyManager(None)

        page1 = Page("first", None)
        page2 = Page("second", None)
        page3 = Page("third", None)
        page4 = Page("fourth", None)

        user_journey_manager._append(page1)
        user_journey_manager._append(page2)
        user_journey_manager._append(page3)
        user_journey_manager._append(page4)

        self.assertEqual(page1, user_journey_manager._first)
        self.assertEqual(page4, user_journey_manager._current)

        self.assertEqual(0, len(user_journey_manager._archive))

        user_journey_manager._truncate(page3)

        self.assertEqual(2, len(user_journey_manager._archive))
        self.assertEqual(page4, user_journey_manager._archive[0])
        self.assertEqual(page3, user_journey_manager._archive[1])

        self.assertIsNone(page3.next_page)
        self.assertIsNone(page3.previous_page)

        self.assertIsNone(page4.next_page)
        self.assertIsNone(page4.previous_page)

        self.assertEqual(page2, user_journey_manager._current)
        self.assertIsNone(page2.next_page)
