from unittest import TestCase, mock
from unittest.mock import Mock, sentinel
from uuid import uuid4

from google.pubsub_v1.types.pubsub import PubsubMessage

from app.publisher import PubSubPublisher
from app.publisher.exceptions import PublicationFailed


class TestPubSub(TestCase):
    topic_id = 'test-topic-id'
    topic_path = f'projects/my-test-project/topics/{topic_id}'

    def setUp(self) -> None:
        self.publisher = PubSubPublisher('my-test-project')

    # pylint: disable=protected-access
    def test_publish(self):
        future = sentinel.future
        future.add_done_callback = Mock(spec=['__call__'])

        # Use a mock in lieu of the actual batch class.
        batch = Mock(spec=self.publisher._client._batch_class)

        # Set the mock up to accepts the message.
        batch.publish.side_effect = (future,)

        self.publisher._client._set_batch(self.topic_path, batch)

        # Publish message.
        future = self.publisher._publish(self.topic_id, 'test-message')
        assert future is sentinel.future

        # Check mock.
        batch.publish.assert_has_calls([mock.call(PubsubMessage(data=b'test-message'))])

    def test_resolving_message_raises_exception_on_error(self):
        with self.assertRaises(PublicationFailed) as ex:
            # Try resolve the future with an incorrect topic id
            self.publisher.publish(
                'bad_topic',
                'test-message',
                fulfilment_request_transaction_id=str(uuid4()),
            )

        assert '404 Topic not found' in str(ex.exception)
