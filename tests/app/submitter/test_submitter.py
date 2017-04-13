from unittest import TestCase

from mock import patch, Mock, call
from pika.exceptions import AMQPError

from app import settings
from app.submitter.submitter import RabbitMQSubmitter, LogSubmitter, SubmitterFactory, Submitter


class TestSubmitter(TestCase):

    def test_when_fail_to_connect_to_queue_then_published_false(self):
        # Given
        with patch('app.submitter.submitter.BlockingConnection') as connection:
            connection.side_effect = AMQPError()

            submitter = RabbitMQSubmitter()

            # When
            published = submitter.send_message(message={}, queue='test_queue')

            # Then
            self.assertFalse(published, 'send_message should fail to publish message')

    def test_when_message_sent_then_published_true(self):
        # Given
        with patch('app.submitter.submitter.BlockingConnection'):
            published = RabbitMQSubmitter().send_message(message={}, queue='test_queue')

            # When

            # Then
            self.assertTrue(published, 'send_message should publish message')

    def test_when_first_connection_fails_then_secondary_succeeds(self):
        # Given
        with patch('app.submitter.submitter.BlockingConnection') as connection, \
                patch('app.submitter.submitter.URLParameters') as url_parameters:
            secondary_connection = Mock()
            connection.side_effect = [AMQPError(), secondary_connection]

            # When
            published = RabbitMQSubmitter().send_message(message={}, queue='test_queue')

            # Then
            self.assertTrue(published, 'send_message should publish message')
            # Check we create url for primary then secondary
            url_parameters_calls = [call(settings.EQ_RABBITMQ_URL), call(settings.EQ_RABBITMQ_URL_SECONDARY)]
            url_parameters.assert_has_calls(url_parameters_calls)
            # Check we create connection twice, failing first then with settings.EQ_RABBITMQ_URL_SECONDARY
            self.assertEqual(connection.call_count, 2)

    def test_when_fail_to_disconnect_then_log_warning_message(self):
        # Given
        connection = Mock()
        error = AMQPError()
        connection.close.side_effect = [error]
        settings.EQ_RABBITMQ_URL = 'amqp://localhost:5672/%2F'
        with patch('app.submitter.submitter.BlockingConnection', return_value=connection), \
                patch('app.submitter.submitter.logger') as logger:

            # When
            published = RabbitMQSubmitter().send_message(message={}, queue='test_queue')

            # Then
            self.assertTrue(published)
            logger.error.assert_called_once_with('unable to close connection', category='rabbitmq', exc_info=error)

    def test_when_fail_to_publish_message_then_returns_false(self):
        # Given
        channel = Mock()
        channel.basic_publish = Mock(return_value=False)
        connection = Mock()
        connection.channel.side_effect = Mock(return_value=channel)
        with patch('app.submitter.submitter.BlockingConnection', return_value=connection):
            # When
            published = RabbitMQSubmitter().send_message(message={}, queue='test_queue')

            # Then
            self.assertFalse(published, 'send_message should fail to publish message')

    def test_log_submitter_send_message(self):
        # Given
        with patch('app.submitter.submitter.BlockingConnection'):
            # When
            sent_message = LogSubmitter().send_message(message={}, queue='test_queue')

            # Then
            self.assertEqual(sent_message, True)

    def test_get_submitter_settings_enabled(self):
        settings.EQ_RABBITMQ_ENABLED = True
        test = SubmitterFactory.get_submitter()
        self.assertIsInstance(type(test), cls=object)

    def test_get_submitter_settings_not_enabled(self):
        settings.EQ_RABBITMQ_ENABLED = False
        test = SubmitterFactory.get_submitter()
        self.assertIsInstance(type(test), cls=object)

    def test_submitter_send_message(self):
        test = Submitter.send_message(self, message={}, queue='test_queue')
        self.assertEqual(test, False)

    def test_submitter_encrypt_message(self):
        test = Submitter.encrypt_message(message={})
        self.assertIsInstance(test, cls=str)
