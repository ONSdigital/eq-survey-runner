import json

from app import settings
from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
from app.storage.abstract_server_storage import AbstractServerStorage, logger


class EncryptedServerStorageDecorator(AbstractServerStorage):

    ENCRYPTED_KEY = 'encrypted'

    def __init__(self, server_storage):
        self.encryption = JWEDirEncrypter(settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY)
        self.decryption = JWEDirDecrypter(settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY)
        self.server_storage = server_storage

    def store(self, user_id, data):
        logger.debug("About to encrypt data %s", data)
        encrypted_data = self.encryption.encrypt(json.dumps(data))
        logger.debug("Encrypted data %s", encrypted_data)
        self.server_storage.store(user_id, {EncryptedServerStorageDecorator.ENCRYPTED_KEY: encrypted_data})

    def get(self, user_id):
        data = self.server_storage.get(user_id)
        logger.debug("About to decrypt data %s", data)
        decrypted_data = self.decryption.decrypt(data[EncryptedServerStorageDecorator.ENCRYPTED_KEY])
        logger.debug("Decrypted data %s", decrypted_data)
        json_data = json.loads(decrypted_data)
        logger.debug("JSONify %s", json_data)
        return json_data

    def has_data(self, user_id):
        return self.server_storage.has_data(user_id)

    def delete(self, user_id):
        self.server_storage.delete(user_id)

    def clear(self):
        self.server_storage.clear()
