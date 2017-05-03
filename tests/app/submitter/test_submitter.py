from unittest import TestCase

from mock import patch, Mock, call
from pika.exceptions import AMQPError

from app.submitter.submitter import RabbitMQSubmitter


class TestSubmitter(TestCase):
    def setUp(self):
        self.queue_name = 'test_queue'
        self.url1 = 'amqp://localhost:5672/%2F'
        self.url2 = 'amqp://localhost:5672/%2F'

        self.submitter = RabbitMQSubmitter(self.url1, self.url2)

    def test_when_fail_to_connect_to_queue_then_published_false(self):
        # Given
        with patch('app.submitter.submitter.BlockingConnection') as connection:
            connection.side_effect = AMQPError()

            # When
            published = self.submitter.send_message(message={}, queue=self.queue_name, tx_id='12345')

            # Then
            self.assertFalse(published, 'send_message should fail to publish message')

    def test_when_message_sent_then_published_true(self):
        # Given
        with patch('app.submitter.submitter.BlockingConnection'):
            published = self.submitter.send_message(message={}, queue=self.queue_name, tx_id='12345')

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
            published = self.submitter.send_message(message={}, queue=self.queue_name, tx_id='12345')

            # Then
            self.assertTrue(published, 'send_message should publish message')
            # Check we create url for primary then secondary
            url_parameters_calls = [call(self.url1), call(self.url2)]
            url_parameters.assert_has_calls(url_parameters_calls)
            # Check we create connection twice, failing first then with self.url2
            self.assertEqual(connection.call_count, 2)

    def test_when_fail_to_disconnect_then_log_warning_message(self):
        # Given
        connection = Mock()
        error = AMQPError()
        connection.close.side_effect = [error]

        with patch('app.submitter.submitter.BlockingConnection', return_value=connection), \
                patch('app.submitter.submitter.logger') as logger:

            # When
            published = self.submitter.send_message(message={}, queue=self.queue_name, tx_id='12345')

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
            published = self.submitter.send_message(message={}, queue=self.queue_name, tx_id='12345')

            # Then
            self.assertFalse(published, 'send_message should fail to publish message')

    def test_when_message_sent_then_tx_id_is_sent_in_header(self):
        # Given
        channel = Mock()
        connection = Mock()
        connection.channel.side_effect = Mock(return_value=channel)
        with patch('app.submitter.submitter.BlockingConnection', return_value=connection):
            # When
            self.submitter.send_message(message={}, queue=self.queue_name, tx_id='12345')

            # Then
            call_args = channel.basic_publish.call_args
            properties = call_args[1]['properties']
            headers = properties.headers
            self.assertEqual(headers['tx_id'], '12345')

    def test_when_message_sent_with_none_tx_id_then_tx_id_is_not_sent_in_header(self):
        # Given
        channel = Mock()
        connection = Mock()
        connection.channel.side_effect = Mock(return_value=channel)
        with patch('app.submitter.submitter.BlockingConnection', return_value=connection):
            # When
            self.submitter.send_message(message={}, queue=self.queue_name, tx_id=None)

            # Then
            call_args = channel.basic_publish.call_args
            properties = call_args[1]['properties']
            headers = properties.headers
            self.assertEqual(len(headers), 0)
