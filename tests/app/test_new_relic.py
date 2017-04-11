import unittest
from mock import patch

from app.new_relic import setup_newrelic

class TestSettings(unittest.TestCase):

    def test_new_relic_is_enabled(self):
        with patch('newrelic.agent.initialize') as new_relic:

            setup_newrelic()

            self.assertEqual(new_relic.call_count, 1)

if __name__ == '__main__':
    unittest.main()
