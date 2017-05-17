import unittest
from uuid import UUID
from mock import patch

from flask import Flask
from flask_babel import Babel
import app
from app import settings
from app.submitter.submitter import LogSubmitter, RabbitMQSubmitter


class TestCreateApp(unittest.TestCase):
    def setUp(self):
        pass

    def test_returns_application(self):
        self.assertIsInstance(app.create_app(), Flask)

    # Should new relic have direct access to settings?
    # Probably better for create app to have the control
    def test_setups_newrelic(self):
        with patch('newrelic.agent.initialize') as new_relic:
            settings.EQ_NEW_RELIC_ENABLED = "True"
            app.create_app()
            self.assertEqual(new_relic.call_count, 1)

    def test_sets_static_url(self):
        self.assertEqual('/s', app.create_app().static_url_path)

    def test_sets_static_folder_that_exists(self):
        self.assertRegex(app.create_app().static_folder, '../static$')

    def test_sets_content_length(self):
        self.assertGreater(app.create_app().config['MAX_CONTENT_LENGTH'], 0)

    def test_enforces_secure_session(self):
        application = app.create_app()
        self.assertTrue(application.secret_key)
        self.assertTrue(application.permanent_session_lifetime)
        self.assertTrue(application.session_interface)
        # All tests run in dev mode which sets SESSION_COOKIE_SECURE to false
        self.assertFalse(application.config['SESSION_COOKIE_SECURE'])

    # localisation may not be used but is currently attached...
    def test_adds_i18n_to_application(self):
        self.assertIsInstance(app.create_app().babel, Babel) # pylint: disable=no-member

    def test_adds_logging_of_request_ids(self):
        with patch('app.logger') as logger:
            settings.EQ_DEV_MODE = True
            settings.EQ_APPLICATION_VERSION = False
            application = app.create_app()

            application.test_client().get('/')
            self.assertEqual(1, logger.new.call_count)
            _, kwargs = logger.new.call_args
            self.assertTrue(UUID(kwargs['request_id'], version=4))


    def test_enforces_secure_headers(self):
        client = app.create_app().test_client()
        headers = client.get('/').headers
        self.assertEqual('no-cache, no-store, must-revalidate', headers['Cache-Control'])
        self.assertEqual('no-cache', headers['Pragma'])
        self.assertEqual('max-age=31536000; includeSubdomains', headers['Strict-Transport-Security'])
        self.assertEqual('DENY', headers['X-Frame-Options'])
        self.assertEqual('1; mode=block', headers['X-Xss-Protection'])
        self.assertEqual('nosniff', headers['X-Content-Type-Options'])


    # Indirectly covered by higher level integration
    # tests, keeping to highlight that create_app is where
    # it happens.
    def test_adds_blueprints(self):
        self.assertGreater(len(app.create_app().blueprints), 0)

    def test_removes_db_session_on_teardown(self):
        with patch('app.Database.remove') as remove:
            application = app.create_app()
            application.test_client().get('/')

            self.assertEqual(remove.call_count, 1)

    def test_versioned_url_for_with_version(self):
        settings.EQ_APPLICATION_VERSION = 'abc123'
        application = app.create_app()
        application.config['SERVER_NAME'] = "test"

        with application.app_context():
            self.assertEqual(
                'http://test/s/a.jpg?q=abc123',
                app.versioned_url_for('static', filename='a.jpg')
            )

        # This is bad news, should make better use of
        # Flasks application factories pattern so that
        # cross test config bleed isn't possible
        settings.EQ_APPLICATION_VERSION = 'False'

    def test_versioned_url_for_without_version(self):
        settings.EQ_MINIMIZE_VERSION = False
        application = app.create_app()
        application.config['SERVER_NAME'] = "test"

        with application.app_context():
            self.assertEqual(
                'http://test/s/a.jpg?q=False',
                app.versioned_url_for('static', filename='a.jpg')
            )

    def test_versioned_url_for_minimized_assets(self):
        settings.EQ_MINIMIZE_ASSETS = True
        application = app.create_app()
        application.config['SERVER_NAME'] = "test"

        with application.app_context():
            self.assertEqual(
                'http://test/s/some.min.css?q=False',
                app.versioned_url_for('static', filename='some.css')
            )

            self.assertEqual(
                'http://test/s/some.min.js?q=False',
                app.versioned_url_for('static', filename='some.js')
            )

        # This is bad news, should make better use of
        # Flasks application factories pattern so that
        # cross test config bleed isn't possible
        settings.EQ_MINIMIZE_ASSETS = False


    def test_versioned_url_for_regular_assets(self):
        settings.EQ_MINIMIZE_ASSETS = False
        application = app.create_app()
        application.config['SERVER_NAME'] = "test"

        with application.app_context():
            self.assertEqual(
                'http://test/s/some.css?q=False',
                app.versioned_url_for('static', filename='some.css')
            )

            self.assertEqual(
                'http://test/s/some.js?q=False',
                app.versioned_url_for('static', filename='some.js')
            )

    def test_adds_rabbit_submitter_to_the_application(self):
        settings.EQ_RABBITMQ_ENABLED = True
        application = app.create_app()

        self.assertIsInstance(application.eq['submitter'], RabbitMQSubmitter)

        settings.EQ_RABBITMQ_ENABLED = False

    def test_defaults_to_adding_the_log_submitter_to_the_application(self):
        settings.EQ_RABBITMQ_ENABLED = False
        application = app.create_app()

        self.assertIsInstance(application.eq['submitter'], LogSubmitter)

    def test_adds_encrypter_to_the_application(self):
        application = app.create_app()

        self.assertIn('encrypter', application.eq)


if __name__ == '__main__':
    unittest.main()
