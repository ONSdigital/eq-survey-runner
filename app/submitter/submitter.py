import logging

from abc import abstractmethod

from app import settings
from app.submitter.encrypter import Encrypter
from app.submitter.submission_failed import SubmissionFailedException

import pika
import pika.credentials
import pika.exceptions

logger = logging.getLogger(__name__)


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
        logger.info("Message submitted %s", message)
        return True


class RabbitMQSubmitter(Submitter):
    def __init__(self):
        self.connection = None

    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(settings.EQ_RABBITMQ_URL))
        except pika.exceptions.AMQPError as e:
            logger.error('Unable to connect to Prime Message Server')
            logger.info("Unable to open Rabbit MQ connection to  " + settings.EQ_RABBITMQ_URL + " " + repr(e))
            logger.error("Attempting failover to secondary")
            try:
                self.connection = pika.BlockingConnection(pika.URLParameters(settings.EQ_RABBITMQ_URL_SECONDARY))
            except pika.exceptions.AMQPError as err:
                logger.error('Unable to connect to Prime Message Server')
                logger.info("Unable to open Secondary Rabbit MQ connection to %s, ERROR: %s", settings.EQ_RABBITMQ_URL_SECONDARY, repr(e))
                logger.error("Attempting failover to secondary")
                raise err

    def _disconnect(self):
        try:
            if self.connection:
                self.connection.close()
        except pika.exceptions.AMQPError as e:
            logger.warning("Unable to close Rabbit MQ connection to  " + settings.EQ_RABBITMQ_URL + " " + repr(e))

    def send_message(self, message, queue):
        """
        Sends a message to rabbit mq and returns a true or false depending on if it was successful
        :param message: The message to send to the rabbit mq queue
        :param queue: the name of the queue
        :return: a boolean value indicating if it was successful
        """
        message_as_string = str(message)
        logger.info("Sending messaging " + message_as_string)
        try:
            self._connect()
            channel = self.connection.channel()
            channel.queue_declare(queue=queue, durable=True)
            published = channel.basic_publish(exchange='',
                                              routing_key=queue,
                                              body=message_as_string,
                                              mandatory=True,
                                              properties=pika.BasicProperties(
                                                  delivery_mode=2,
                                              ))
            if published:
                logger.info("Sent to rabbit mq " + message_as_string)
            else:
                logger.error('Unable to send message')
                logger.info("Unable to send to rabbit mq " + message_as_string)
            return published
        except pika.exceptions.AMQPError as e:
            logger.error('Unable to send message')
            logger.info("Unable to send " + message_as_string + " to " + settings.EQ_RABBITMQ_URL + " " + repr(e))
            return False
        finally:
            self._disconnect()
