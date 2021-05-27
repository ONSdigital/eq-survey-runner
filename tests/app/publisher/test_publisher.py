from unittest import TestCase, mock
from unittest.mock import Mock, patch, sentinel
from uuid import uuid4

from google.pubsub_v1.types.pubsub import PubsubMessage

from app.publisher import PubSubPublisher
from app.publisher.exceptions import PublicationFailed


class TestPubSub(TestCase):
    topic_id = "test-topic-id"
    topic_path = f"projects/test-project-id/topics/{topic_id}"

    def setUp(self) -> None:
        with patch(
            "app.publisher.publisher.google.auth._default._get_explicit_environ_credentials",
            return_value=(Mock(), "test-project-id"),
        ):
            self.publisher = PubSubPublisher()

    # pylint: disable=protected-access
    def test_publish(self):
        future = sentinel.future
        future.add_done_callback = Mock(spec=["__call__"])

        # Use a mock in lieu of the actual batch class.
        batch = Mock(spec=self.publisher._client._batch_class)

        # Set the mock up to accepts the message.
        batch.publish.side_effect = (future,)

        self.publisher._client._set_batch(self.topic_path, batch)

        # Publish message.
        future = self.publisher._publish(self.topic_id, b"test-message")
        assert future is sentinel.future

        # Check mock.
        batch.publish.assert_has_calls([mock.call(PubsubMessage(data=b"test-message"))])

    def test_resolving_message_raises_exception_on_error(self):
        with self.assertRaises(PublicationFailed) as ex:
            # Try resolve the future with an invalid credentials
            self.publisher.publish(
                self.topic_id,
                b"test-message",
                fulfilment_request_transaction_id=str(uuid4()),
            )

        assert "403 The request is missing a valid API key." in str(ex.exception)
