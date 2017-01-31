from abc import abstractmethod

from pika import BasicProperties
from pika import BlockingConnection
from pika import URLParameters
from pika.exceptions import AMQPError
from structlog import get_logger

from app import settings
from app.submitter.encrypter import Encrypter
from app.submitter.submission_failed import SubmissionFailedException

logger = get_logger()


class SubmitterFactory(object):

    @staticmethod
    def get_submitter():
        if settings.EQ_RABBITMQ_ENABLED:
            return RabbitMQSubmitter()
        else:
            return LogSubmitter()


class Submitter(object):

    def send_answers(self, message):
        """
        Sends the answers to rabbit mq and returns a timestamp for submission
        :param message: The payload to submit
        :raise: a submission failed exception
        """
        encrypted_message = self.encrypt_message(message)
        sent = self.send_message(encrypted_message, settings.EQ_RABBITMQ_QUEUE_NAME)
        if not sent:
            raise SubmissionFailedException()

    def send_test(self):
        test = "Test connection"
        return self.send_message(test, settings.EQ_RABBITMQ_TEST_QUEUE_NAME)

    @abstractmethod
    def send_message(self, message, queue):
        return False

    @staticmethod
    def encrypt_message(message):
        return Encrypter().encrypt(message)


class LogSubmitter(Submitter):

    def send_message(self, message, queue):
        logger.info("message submitted", message=message)
        return True


class RabbitMQSubmitter(Submitter):
    def __init__(self):
        self.connection = None

    def _connect(self):
        try:
            self.connection = BlockingConnection(URLParameters(settings.EQ_RABBITMQ_URL))
        except AMQPError as e:
            logger.error("unable to open rabbit mq connection", exc_info=e, rabbit_url=settings.EQ_RABBITMQ_URL)
            try:
                self.connection = BlockingConnection(URLParameters(settings.EQ_RABBITMQ_URL_SECONDARY))
            except AMQPError as err:
                logger.error("unable to open rabbit mq connection", exc_info=e, rabbit_url=settings.EQ_RABBITMQ_URL_SECONDARY)
                raise err

    def _disconnect(self):
        try:
            if self.connection:
                self.connection.close()
        except AMQPError as e:
            logger.error("unable to close rabbit mq connection", exc_info=e, rabbit_url=settings.EQ_RABBITMQ_URL)

    def send_message(self, message, queue):
        """
        Sends a message to rabbit mq and returns a true or false depending on if it was successful
        :param message: The message to send to the rabbit mq queue
        :param queue: the name of the queue
        :return: a boolean value indicating if it was successful
        """
        message_as_string = str(message)
        logger.info("sending message to rabbit mq", message=message_as_string)
        try:
            self._connect()
            channel = self.connection.channel()
            channel.queue_declare(queue=queue, durable=True)
            published = channel.basic_publish(exchange='',
                                              routing_key=queue,
                                              body=message_as_string,
                                              mandatory=True,
                                              properties=BasicProperties(
                                                  delivery_mode=2,
                                              ))
            if published:
                logger.info("sent message to rabbit mq")
            else:
                logger.error("unable to send message to rabbit mq", message=message_as_string)
            return published
        except AMQPError as e:
            logger.error("unable to send message to rabbit mq", exc_info=e, message=message_as_string)
            return False
        finally:
            self._disconnect()
