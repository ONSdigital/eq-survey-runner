import unittest
from app.frontend_messages import get_message
from flask.ext.babel import gettext as _

EXPECTED_MESSAGE = {
                  'TITLE': _("Information"),
                  'MSG': _("Unfortunately you can only complete one survey at a time."),
                  'INSTRUCTIONS': _("Close this window to continue with your current survey."),
                  }

class TestFrontEndMessage(unittest.TestCase):
    def test_front_end_messages(self):
        front_end_message = get_message('multiple-surveys')
        self.assertEqual(EXPECTED_MESSAGE, front_end_message)
