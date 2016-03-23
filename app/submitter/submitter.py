import pika
import pika.credentials
import pika.exceptions
import logging
from app import settings
from app.submitter.converter import Converter

logger = logging.getLogger(__name__)


class Submitter(object):
    def __init__(self):
        self.connection = None

    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(settings.EQ_RABBITMQ_URL))
        except pika.exceptions.AMQPError as e:
            logger.error("Unable to open Rabbit MQ connection to  " + settings.EQ_RABBITMQ_URL + " " + repr(e))
            raise e

    def _disconnect(self):
        try:
            if self.connection:
                self.connection.close()
        except pika.exceptions.AMQPError as e:
            logger.warning("Unable to close Rabbit MQ connection to  " + settings.EQ_RABBITMQ_URL + " " + repr(e))

    def send_responses(self, user, schema, responses):
        message = Converter.prepare_responses(user, schema, responses)
        return self.send(message)

    def send(self, message):
        return self.send_message(message, settings.EQ_RABBITMQ_QUEUE_NAME)

    def send_message(self, message, queue):
        '''
        Sends a message to rabbit mq and returns a timestamp for submission
        :param message: The message to send to the rabbit mq queue
        :param queue: the name of the queue
        :return: a timestamp indicating the time it was submitted
        '''
        message_as_string = str(message)
        logger.info("Sending messaging " + message_as_string)
        try:
            self._connect()
            channel = self.connection.channel()
            channel.queue_declare(queue=queue)
            published = channel.basic_publish(exchange='', routing_key=queue, body=message_as_string, mandatory=True)
            if published:
                logger.info("Sent to rabbit mq " + message_as_string)
            else:
                logger.error("Unable to send to rabbit mq " + message_as_string)
            return published
        except pika.exceptions.AMQPError as e:
            logger.error("Unable to send " + message_as_string + " to " + settings.EQ_RABBITMQ_URL + " " + repr(e))
            return False
        finally:
            self._disconnect()

    def send_test(self):
        test = "Test connection"
        return self.send_message(test, settings.EQ_RABBITMQ_TEST_QUEUE_NAME)
