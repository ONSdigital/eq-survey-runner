import logging

from app import settings
from app.storage.database_storage import DatabaseStorage
from app.storage.encrypted_storage import EncryptedStorageDecorator

logger = logging.getLogger(__name__)


def get_storage():
    logger.debug("Using server side storage %s ", settings.EQ_SERVER_SIDE_STORAGE_TYPE)
    storage = DatabaseStorage()

    if settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION:
        # wrap the storage in an encrypted decorator
        return EncryptedStorageDecorator(storage)

    return storage
