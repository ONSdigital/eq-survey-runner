from pika import BasicProperties
from pika import BlockingConnection
from pika import URLParameters
from pika.exceptions import AMQPError
from structlog import get_logger

logger = get_logger()


class LogSubmitter():  # pylint: disable=no-self-use

    def send_message(self, message, queue):
        logger.info("sending message")
        logger.info("message payload", message=message, queue=queue)
        return True


class RabbitMQSubmitter():
    def __init__(self, rabbitmq_url, rabbitmq_secondary_url):
        self.rabbitmq_url = rabbitmq_url
        self.rabbitmq_secondary_url = rabbitmq_secondary_url
        self.connection = None

    def _connect(self):
        try:
            logger.info("attempt to open connection", server="primary", category="rabbitmq")
            self.connection = BlockingConnection(URLParameters(self.rabbitmq_url))
        except AMQPError as e:
            logger.error("unable to open connection", exc_info=e, server="primary", category="rabbitmq")
            try:
                logger.info("attempt to open connection", server="secondary", category="rabbitmq")
                self.connection = BlockingConnection(URLParameters(self.rabbitmq_secondary_url))
            except AMQPError as err:
                logger.error("unable to open connection", exc_info=e, server="secondary", category="rabbitmq")
                raise err

    def _disconnect(self):
        try:
            if self.connection:
                logger.info("attempt to close connection", category="rabbitmq")
                self.connection.close()
        except AMQPError as e:
            logger.error("unable to close connection", exc_info=e, category="rabbitmq")

    def send_message(self, message, queue):
        """
        Sends a message to rabbit mq and returns a true or false depending on if it was successful
        :param message: The message to send to the rabbit mq queue
        :param queue: the name of the queue
        :return: a boolean value indicating if it was successful
        """
        message_as_string = str(message)
        logger.info("sending message", category="rabbitmq")
        logger.info("message payload", message=message_as_string, category="rabbitmq")
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
                logger.info("sent message", category="rabbitmq")
            else:
                logger.error("unable to send message", category="rabbitmq")
            return published
        except AMQPError as e:
            logger.error("unable to send message", exc_info=e, category="rabbitmq")
            return False
        finally:
            self._disconnect()
