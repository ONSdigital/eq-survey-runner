import unittest

from mock import patch

from app.new_relic import setup_newrelic
from app import settings


class TestSettings(unittest.TestCase):

    def test_new_relic_is_enabled(self):
        with patch('newrelic.agent.initialize') as new_relic:

            settings.EQ_NEW_RELIC_ENABLED = True

            setup_newrelic()

            self.assertEqual(new_relic.call_count, 1)

    def test_new_relic_is_disabled(self):
        with patch('newrelic.agent.initialize') as new_relic:

            settings.EQ_NEW_RELIC_ENABLED = False

            setup_newrelic()

            self.assertEqual(new_relic.call_count, 0)

if __name__ == '__main__':
    unittest.main()
