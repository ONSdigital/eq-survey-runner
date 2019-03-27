import unittest
from uuid import UUID
from contextlib import contextmanager
from mock import patch, MagicMock

from flask import Flask, request
from flask_babel import Babel

from app import settings
from app.setup import create_app, versioned_url_for, get_database_uri, EmulatorCredentials
from app.storage.datastore import DatastoreStorage
from app.storage.dynamodb import DynamodbStorage
from app.submitter.submitter import LogSubmitter, RabbitMQSubmitter, GCSSubmitter


class TestCreateApp(unittest.TestCase): # pylint: disable=too-many-public-methods
    def setUp(self):
        self._setting_overrides = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:////tmp/questionnaire.db'
        }

    @contextmanager
    def override_settings(self):
        """ Required because although the settings are overriden on the application
        by passing _setting_overrides in, there are many funtions which use the
        imported settings object - this does not get the overrides merged in. this
        helper does that.

        Note - this is not very nice, however it's better than polluting the global
        settings.

        Returns a list of contexts."""
        patches = [patch('app.setup.settings.{}'.format(k), v) for k, v in self._setting_overrides.items()]
        for p in patches:
            p.start()
        yield patches
        for p in patches:
            p.stop()

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
            self._setting_overrides.update({
                'EQ_DEV_MODE': True,
                'EQ_APPLICATION_VERSION': False
            })
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
            self.assertIn("default-src 'self' https://cdn.ons.gov.uk", csp_policy_parts)
            self.assertIn(
                "script-src 'self' https://www.google-analytics.com https://cdn.ons.gov.uk 'nonce-{}'".format(
                    request.csp_nonce),
                csp_policy_parts
            )
            self.assertIn(
                "img-src 'self' data: https://www.google-analytics.com https://cdn.ons.gov.uk", csp_policy_parts)
            self.assertIn(
                "font-src 'self' data: https://cdn.ons.gov.uk", csp_policy_parts)

    # Indirectly covered by higher level integration
    # tests, keeping to highlight that create_app is where
    # it happens.
    def test_adds_blueprints(self):
        self.assertGreater(len(create_app(self._setting_overrides).blueprints), 0)

    def test_versioned_url_for_with_version(self):
        self._setting_overrides['EQ_APPLICATION_VERSION'] = 'abc123'
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        with application.app_context(), self.override_settings():
            self.assertEqual(
                'http://test/s/a.jpg?q=abc123',
                versioned_url_for('static', filename='a.jpg')
            )

    def test_versioned_url_for_without_version(self):
        self._setting_overrides.update({
            'EQ_APPLICATION_VERSION': False,
        })
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        # Patches the application version, since it's used in `versioned_url_for`
        with application.app_context(), self.override_settings():
            self.assertEqual(
                'http://test/s/a.jpg?q=False',
                versioned_url_for('static', filename='a.jpg')
            )

    def test_versioned_url_for_minimized_assets(self):
        self._setting_overrides.update({
            'EQ_MINIMIZE_ASSETS': True,
            'EQ_APPLICATION_VERSION': 'False',
        })
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        with application.app_context(), self.override_settings():
            self.assertEqual(
                'http://test/s/some.min.css?q=False',
                versioned_url_for('static', filename='some.css')
            )

            self.assertEqual(
                'http://test/s/some.min.js?q=False',
                versioned_url_for('static', filename='some.js')
            )

    def test_versioned_url_for_regular_assets(self):
        self._setting_overrides.update({
            'EQ_MINIMIZE_ASSETS': False,
            'EQ_APPLICATION_VERSION': False,
        })
        application = create_app(self._setting_overrides)
        application.config['SERVER_NAME'] = 'test'

        with application.app_context(), self.override_settings():
            self.assertEqual(
                'http://test/s/some.css?q=False',
                versioned_url_for('static', filename='some.css')
            )

            self.assertEqual(
                'http://test/s/some.js?q=False',
                versioned_url_for('static', filename='some.js')
            )

    def test_eq_submission_backend_not_set(self):
        # Given
        self._setting_overrides['EQ_SUBMISSION_BACKEND'] = ''

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert 'Unknown EQ_SUBMISSION_BACKEND' in str(ex.exception)

    def test_adds_gcs_submitter_to_the_application(self):
        # Given
        self._setting_overrides['EQ_SUBMISSION_BACKEND'] = 'gcs'
        self._setting_overrides['EQ_GCS_SUBMISSION_BUCKET_ID'] = '123'

        # When
        with patch('google.cloud.storage.Client'):
            application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq['submitter'], GCSSubmitter)

    def test_gcs_submitter_bucket_id_not_set_raises_exception(self):
        # Given
        self._setting_overrides['EQ_SUBMISSION_BACKEND'] = 'gcs'

        # WHEN
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert 'Setting EQ_GCS_SUBMISSION_BUCKET_ID Missing' in str(ex.exception)

    def test_adds_rabbit_submitter_to_the_application(self):
        # Given
        self._setting_overrides['EQ_SUBMISSION_BACKEND'] = 'rabbitmq'
        self._setting_overrides['EQ_RABBITMQ_HOST'] = 'host-1'
        self._setting_overrides['EQ_RABBITMQ_HOST_SECONDARY'] = 'host-2'

        # When
        application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq['submitter'], RabbitMQSubmitter)

    def test_rabbit_submitter_host_not_set_raises_exception(self):
        # Given
        self._setting_overrides['EQ_SUBMISSION_BACKEND'] = 'rabbitmq'
        self._setting_overrides['EQ_RABBITMQ_HOST'] = ''

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert 'Setting EQ_RABBITMQ_HOST Missing' in str(ex.exception)

    def test_rabbit_submitter_secondary_host_not_set_raises_exception(self):
        #Given
        self._setting_overrides['EQ_SUBMISSION_BACKEND'] = 'rabbitmq'
        self._setting_overrides['EQ_RABBITMQ_HOST_SECONDARY'] = ''

        # When
        with self.assertRaises(Exception) as ex:
            create_app(self._setting_overrides)

        # Then
        assert 'Setting EQ_RABBITMQ_HOST_SECONDARY Missing' in str(ex.exception)

    def test_defaults_to_adding_the_log_submitter_to_the_application(self):
        # When
        application = create_app(self._setting_overrides)

        # Then
        assert isinstance(application.eq['submitter'], LogSubmitter)

    def test_emulator_credentials(self):
        creds = EmulatorCredentials()

        self.assertTrue(creds.valid)

        with self.assertRaises(RuntimeError):
            creds.refresh(None)

    def test_setup_datastore(self):
        self._setting_overrides['EQ_STORAGE_BACKEND'] = 'datastore'

        with patch('google.cloud.datastore.Client'):
            application = create_app(self._setting_overrides)

        self.assertIsInstance(application.eq['storage'], DatastoreStorage)

    def test_setup_dynamodb(self):
        self._setting_overrides['EQ_STORAGE_BACKEND'] = 'dynamodb'

        application = create_app(self._setting_overrides)

        self.assertIsInstance(application.eq['storage'], DynamodbStorage)

    def test_invalid_storage(self):
        self._setting_overrides['EQ_STORAGE_BACKEND'] = 'invalid'

        with self.assertRaises(Exception):
            create_app(self._setting_overrides)

    def test_setup_from_database_components(self):
        # Given
        self._setting_overrides.update({
            'EQ_SERVER_SIDE_STORAGE_DATABASE_HOST': '',
            'EQ_SERVER_SIDE_STORAGE_DATABASE_PORT': '',
            'EQ_SERVER_SIDE_STORAGE_DATABASE_NAME': 'questionnaire.db',
            'EQ_SERVER_SIDE_STORAGE_DATABASE_DRIVER': 'sqlite',
            'SQLALCHEMY_DATABASE_URI': False,
        })

        application = MagicMock()
        application.config = self._setting_overrides
        secret_store = MagicMock()
        secret_store.get_secret_by_name = MagicMock(return_value='')
        application.eq = {'secret_store': secret_store}

        # When
        uri = get_database_uri(application)

        # Then
        self.assertEqual(uri, 'sqlite://:@:/questionnaire.db')
