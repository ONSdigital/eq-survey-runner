import pika
import pika.credentials
import pika.exceptions
import logging
from app import settings


class Submitter(object):
    def __init__(self):
        self.connection = None

    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(settings.EQ_RABBITMQ_URL))
        except pika.exceptions.AMQPError as e:
            logging.error("Unable to open Rabbit MQ connection to  " + settings.EQ_RABBITMQ_URL + " " + repr(e))
            raise e

    def _disconnect(self):
        try:
            if self.connection:
                self.connection.close()
        except pika.exceptions.AMQPError as e:
            logging.warning("Unable to close Rabbit MQ connection to  " + settings.EQ_RABBITMQ_URL + " " + repr(e))

    def send(self, token):
        return self.send_message(token, settings.EQ_RABBITMQ_QUEUE_NAME)

    def send_message(self, token, queue):
        token_as_string = str(token)
        logging.info("Sending token " + token_as_string)
        try:
            self._connect()
            channel = self.connection.channel()
            channel.queue_declare(queue=queue)
            channel.basic_publish(exchange='', routing_key=queue, body=token_as_string)
            logging.info("Sent to rabbit mq " + token_as_string)
            return True
        except pika.exceptions.AMQPError as e:
            print(e)
            logging.error("Unable to send " + token_as_string + " to " + settings.EQ_RABBITMQ_URL + " " + repr(e))
            return False
        finally:
            self._disconnect()

    def send_test(self):
        test = "Test connection"
        return self.send_message(test, settings.EQ_RABBITMQ_TEST_QUEUE_NAME)
