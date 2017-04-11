import unittest
from app import get_minimized_asset
from app import settings

class TestAppInit(unittest.TestCase):


    def test_get_minimized_asset_with_env(self):
        settings.EQ_MINIMIZE_ASSETS = True
        self.assertEqual('some.min.css', get_minimized_asset('some.css'))
        self.assertEqual('some.min.js', get_minimized_asset('some.js'))

    def test_get_minimized_asset_without_env(self):
        settings.EQ_MINIMIZE_ASSETS = False

        filename = 'some.css'
        self.assertEqual(filename, get_minimized_asset(filename))

        filename = 'some.js'
        self.assertEqual(filename, get_minimized_asset(filename))


if __name__ == '__main__':
    unittest.main()
