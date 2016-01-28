import pika
import pika.credentials
import pika.exceptions
import os
import logging

rabbit_mq_url = os.getenv('EQ_RABBITMQ_URL', 'rabbitmq.eq.ons.digital')
rabbit_mq_queue = os.getenv('EQ_RABBITMQ_QUEUE_NAME', 'eq-submissions')
rabbit_mq_user = os.getenv('EQ_RABBITMQ_USER', 'admin')
rabbit_mq_password = os.getenv('EQ_RABBITMQ_PASSWORD', 'admin')


class Submitter(object):
    def __init__(self):
        self.credentials = pika.credentials.PlainCredentials(rabbit_mq_user, rabbit_mq_password)
        self.connection = None

    def _connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq_url, credentials=self.credentials))
        except pika.exceptions.AMQPError as e:
            logging.error("Unable to open Rabbit MQ connection to  " + rabbit_mq_url + " " + repr(e))
            raise e

    def _disconnect(self):
        try:
            if self.connection:
                self.connection.close()
        except pika.exceptions.AMQPError as e:
            logging.warning("Unable to close Rabbit MQ connection to  " + rabbit_mq_url + " " + repr(e))

    def send(self, token):
        print("Sending token " + str(token))
        try:
            self._connect()
            channel = self.connection.channel()
            channel.queue_declare(queue=rabbit_mq_queue)
            channel.basic_publish(exchange='', routing_key=rabbit_mq_queue, body=token)
            print("Sent to rabbit mq")
        except pika.exceptions.AMQPError as e:
            print(e)
            logging.error("Unable to send " + str(token) + " to " + rabbit_mq_url + " " + repr(e))
        finally:
            self._disconnect()


