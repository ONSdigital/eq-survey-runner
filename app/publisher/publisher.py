from abc import ABC, abstractmethod

import json
import google.auth  # pylint disable=unused-import
from google.api_core.exceptions import AlreadyExists
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.futures import Future
from google.auth import jwt
from structlog import get_logger

from app.publisher.exceptions import PublicationFailed

logger = get_logger(__name__)


class Publisher(ABC):
    @abstractmethod
    def publish(self, topic_id, message, fulfilment_request_transaction_id):
        pass  # pragma: no cover


class PubSubPublisher(Publisher):
    def __init__(self, project_id, credentials_file):
        logger.info('connecting to pubsub')
        if credentials_file:
            service_account_info = json.load(open(credentials_file))
            publisher_audience = "https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
            credentials_pub = jwt.Credentials.from_service_account_info(
                service_account_info, audience=publisher_audience,
            )
            self._client = PublisherClient(credentials=credentials_pub)
        else:
            self._client = PublisherClient()
        self._project_id = project_id

    def _publish(self, topic_id, message):
        logger.info("publishing message", topic_id=topic_id)
        topic_path = self._client.topic_path(self._project_id, topic_id)
        response: Future = self._client.publish(topic_path, message.encode('utf-8'))
        return response

    def publish(self, topic_id, message: bytes, fulfilment_request_transaction_id: str):
        response = self._publish(topic_id, message)
        try:
            # Resolve the future
            message_id = response.result()
            logger.info(  # pragma: no cover
                "message published successfully",
                topic_id=topic_id,
                message_id=message_id,
                fulfilment_request_transaction_id=fulfilment_request_transaction_id,
            )
        except Exception as ex:  # pylint:disable=broad-except
            logger.exception(
                "message publication failed",
                topic_id=topic_id,
            )
            raise PublicationFailed(ex)

    def create_topic(self, topic_id):
        try:
            logger.info('creating topic')
            topic_path = self._client.topic_path(self._project_id, topic_id)
            self._client.create_topic(request={"name": topic_path})
        except AlreadyExists:
            logger.info("Topic already exists")
        except Exception as ex:
            logger.error(
                "failed", exc_info=ex,
            )


class LogPublisher(Publisher):
    def publish(self, topic_id, message: bytes, fulfilment_request_transaction_id: str):
        logger.info(
            "publishing message",
            topic_id=topic_id,
            message=message,
            fulfilment_request_transaction_id=fulfilment_request_transaction_id,
        )
