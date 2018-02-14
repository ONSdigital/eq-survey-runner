import unittest
from uuid import UUID
from mock import patch

from flask import Flask, request
from flask_babel import Babel

from app import settings
from app.setup import create_app, versioned_url_for
from app.submitter.submitter import LogSubmitter, RabbitMQSubmitter


class TestCreateApp(unittest.TestCase):
    def setUp(self):
        self._setting_overrides = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/questionnaire.db',
            'EQ_DYNAMODB_ENABLED': False
        }

    def test_returns_application(self):
        self.assertIsInstance(create_app(self._setting_overrides), Flask)

    # Should new relic have direct access to settings?
    # Probably better for create app to have the control
    def test_setups_newrelic(self):
        with patch('newrelic.agent.initialize') as new_relic:
            settings.EQ_NEW_RELIC_ENABLED = 'True'
            create_app(self._setting_overrides)
            self.assertEqual(new_relic.call_count, 1)

    def test_sets_static_url(self):
        self.assertEqual('/s', create_app(self._setting_overrides).static_url_path)

    def test_sets_static_folder_that_exists(self):
        self.assertRegex(create_app(self._setting_overrides).static_folder, '../static$')

    def test_sets_content_length(self):
        self.assertGreater(create_app(self._setting_overrides).config['MAX_CONTENT_LENGTH'], 0)

    def test_enforces_secure_session(self):
        application = create_app(self._setting_overrides)
        self.assertTrue(application.secret_key)
        self.assertTrue(application.permanent_session_lifetime)
        self.assertTrue(application.session_interface)

        # This is derived from EQ_ENABLE_SECURE_SESSION_COOKIE which is false
        # when running tests
        self.assertFalse(application.config['SESSION_COOKIE_SECURE'])

    # localisation may not be used but is currently attached...
    def test_adds_i18n_to_application(self):
        self.assertIsInstance(create_app(self._setting_overrides).babel, Babel)  # pylint: disable=no-member

    def test_adds_logging_of_request_ids(self):
        with patch('app.setup.logger') as logger:
            settings.EQ_DEV_MODE = True
            settings.EQ_APPLICATION_VERSION = False
            application = create_app(self._setting_overrides)

            application.test_client().get('/')
            self.assertEqual(1, logger.new.call_count)
            _, kwargs = logger.new.call_args
            self.assertTrue(UUID(kwargs['request_id'], version=4))

    def test_enforces_secure_headers(self):
        with create_app(self._setting_overrides).test_client() as client:
            headers = client.get(
                '/',
                headers={'X-Forwarded-Proto': 'https'} # set protocal so that talisman sets HSTS headers
            ).headers

            self.assertEqual('no-cache, no-store, must-revalidate', headers['Cache-Control'])
            self.assertEqual('no-cache', headers['Pragma'])
            self.assertEqual('max-age=31536000; includeSubDomains', headers['Strict-Transport-Security'])
            self.assertEqual('DENY', headers['X-Frame-Options'])
            self.assertEqual('1; mode=block', headers['X-Xss-Protection'])
            self.assertEqual('nosniff', headers['X-Content-Type-Options'])

            csp_policy_parts = headers['Content-Security-Policy'].split('; ')
            self.assertIn("default-src 'self'", csp_policy_parts)
            self.assertIn(
                "script-src 'self' https://www.google-analytics.com 'nonce-{}'".format(
                    request.csp_nonce),
                csp_policy_parts
            )
            self.assertIn(
                "img-src 'self' data: https://www.google-analytics.com", csp_policy_parts)

    # Indirectly covered by higher level integration
    # tests, keeping to highlight that create_app is where
    # it happens.
    def test_adds_blueprints(self):
        self.assertGreater(len(create_app(self._setting_overrides).blueprints), 0)

    def test_versioned_url_for_with_version(self):
        settings.EQ_APPLICATION_VERSION = 'abc123'
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        with application.app_context():
            self.assertEqual(
                'http://test/s/a.jpg?q=abc123',
                versioned_url_for('static', filename='a.jpg')
            )

        # This is bad news, should make better use of
        # Flasks application factories pattern so that
        # cross test config bleed isn't possible
        settings.EQ_APPLICATION_VERSION = 'False'

    def test_versioned_url_for_without_version(self):
        settings.EQ_MINIMIZE_VERSION = False
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        with application.app_context():
            self.assertEqual(
                'http://test/s/a.jpg?q=False',
                versioned_url_for('static', filename='a.jpg')
            )

    def test_versioned_url_for_minimized_assets(self):
        settings.EQ_MINIMIZE_ASSETS = True
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        with application.app_context():
            self.assertEqual(
                'http://test/s/some.min.css?q=False',
                versioned_url_for('static', filename='some.css')
            )

            self.assertEqual(
                'http://test/s/some.min.js?q=False',
                versioned_url_for('static', filename='some.js')
            )

        # This is bad news, should make better use of
        # Flasks application factories pattern so that
        # cross test config bleed isn't possible
        settings.EQ_MINIMIZE_ASSETS = False

    def test_versioned_url_for_regular_assets(self):
        settings.EQ_MINIMIZE_ASSETS = False
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        with application.app_context():
            self.assertEqual(
                'http://test/s/some.css?q=False',
                versioned_url_for('static', filename='some.css')
            )

            self.assertEqual(
                'http://test/s/some.js?q=False',
                versioned_url_for('static', filename='some.js')
            )

    def test_adds_rabbit_submitter_to_the_application(self):
        settings.EQ_RABBITMQ_ENABLED = True
        application = create_app(self._setting_overrides)

        self.assertIsInstance(application.eq['submitter'], RabbitMQSubmitter)

        settings.EQ_RABBITMQ_ENABLED = False

    def test_defaults_to_adding_the_log_submitter_to_the_application(self):
        settings.EQ_RABBITMQ_ENABLED = False
        application = create_app(self._setting_overrides)

        self.assertIsInstance(application.eq['submitter'], LogSubmitter)


if __name__ == '__main__':
    unittest.main()
