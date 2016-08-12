import logging

from app import settings
from app.storage.database_storage import DatabaseStorage
from app.storage.encrypted_storage import EncryptedServerStorageDecorator
from app.storage.memory_storage import InMemoryStorage

logger = logging.getLogger(__name__)


class StorageFactory(object):

    @staticmethod
    def get_storage_mechanism():
        logger.debug("Using server side storage %s ", settings.EQ_SERVER_SIDE_STORAGE_TYPE)
        if settings.EQ_SERVER_SIDE_STORAGE_TYPE.upper() == 'DATABASE':
            storage = DatabaseStorage()
        else:
            storage = InMemoryStorage()

        if settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION:
            # wrap the storage in an encrypted decorator
            return EncryptedServerStorageDecorator(storage)
        else:
            return storage
