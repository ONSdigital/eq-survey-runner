from google.cloud import storage
from pika import BasicProperties
from pika import BlockingConnection
from pika import URLParameters
from pika.exceptions import AMQPError
from structlog import get_logger

logger = get_logger()


class LogSubmitter:
    @staticmethod
    def send_message(message, case_id=None, tx_id=None):
        logger.info('sending message')
        logger.info('message payload', message=message, case_id=case_id, tx_id=tx_id)

        return True


class GCSSubmitter:

    def __init__(self, project_id, bucket_name):
        client = storage.Client(project_id)
        self.bucket = client.get_bucket(bucket_name)

    def send_message(self, message, case_id=None, tx_id=None):
        logger.info('sending message')

        if not case_id:
            raise Exception('case_id not passed to GCS submitter')

        blob = self.bucket.blob(case_id)

        metadata = {'case_id': case_id}

        if tx_id:
            metadata['tx_id'] = tx_id

        blob.metadata = metadata
        blob.upload_from_string(str(message).encode('utf8'))

        return True


class RabbitMQSubmitter:
    def __init__(self, host, secondary_host, port, queue, username=None, password=None):
        self.queue = queue
        if username and password:
            self.rabbitmq_url = 'amqp://{username}:{password}@{host}:{port}/%2F'.format(username=username,
                                                                                        password=password,
                                                                                        host=host,
                                                                                        port=port)
            self.rabbitmq_secondary_url = 'amqp://{username}:{password}@{host}:{port}/%2F'.format(username=username,
                                                                                                  password=password,
                                                                                                  host=secondary_host,
                                                                                                  port=port)
        else:
            self.rabbitmq_url = 'amqp://{host}:{port}/%2F'.format(host=host, port=port)
            self.rabbitmq_secondary_url = 'amqp://{host}:{port}/%2F'.format(host=secondary_host, port=port)

    def _connect(self):
        try:
            logger.info('attempt to open connection', server='primary', category='rabbitmq')
            return BlockingConnection(URLParameters(self.rabbitmq_url))
        except AMQPError as e:
            logger.error('unable to open connection', exc_info=e, server='primary', category='rabbitmq')
            try:
                logger.info('attempt to open connection', server='secondary', category='rabbitmq')
                return BlockingConnection(URLParameters(self.rabbitmq_secondary_url))
            except AMQPError as err:
                logger.error('unable to open connection', exc_info=e, server='secondary', category='rabbitmq')
                raise err

    @staticmethod
    def _disconnect(connection):
        try:
            if connection:
                logger.info('attempt to close connection', category='rabbitmq')
                connection.close()
        except AMQPError as e:
            logger.error('unable to close connection', exc_info=e, category='rabbitmq')

    def send_message(self, message, case_id=None, tx_id=None):
        """
        Sends a message to rabbit mq and returns a true or false depending on if it was successful
        :param message: The message to send to the rabbit mq queue
        :param case_id: ID used to identify a single instance of a survey collection for a respondent
        :param tx_id: Transaction ID used to trace a transaction through the whole system.
        :return: a boolean value indicating if it was successful
        """
        message_as_string = str(message)
        logger.info('sending message', category='rabbitmq')
        logger.info('message payload', message=message_as_string, category='rabbitmq')
        connection = None
        try:
            connection = self._connect()
            channel = connection.channel()

            channel.queue_declare(queue=self.queue, durable=True)
            properties = BasicProperties(headers={},
                                         delivery_mode=2)

            if case_id:
                properties.headers['case_id'] = case_id
            if tx_id:
                properties.headers['tx_id'] = tx_id

            published = channel.basic_publish(exchange='',
                                              routing_key=self.queue,
                                              body=message_as_string,
                                              mandatory=True,
                                              properties=properties)
            if published:
                logger.info('sent message', category='rabbitmq')
            else:
                logger.error('unable to send message', category='rabbitmq')
            return published
        except AMQPError as e:
            logger.error('unable to send message', exc_info=e, category='rabbitmq')
            return False
        finally:
            if connection:
                self._disconnect(connection)
