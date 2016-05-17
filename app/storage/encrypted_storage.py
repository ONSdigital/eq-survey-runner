from app import settings
from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
from app.storage.abstract_server_storage import AbstractServerStorage
from app.utilities.strings import to_str
from app.utilities.strings import to_bytes
import json
import hashlib
import logging

logger = logging.getLogger(__name__)


class EncryptedServerStorageDecorator(AbstractServerStorage):

    ENCRYPTED_KEY = 'encrypted'

    def __init__(self, server_storage):
        self.encryption = JWEDirEncrypter()
        self.decryption = JWEDirDecrypter()
        self.server_storage = server_storage

    def store(self, user_id, data):
        logger.debug("About to encrypt data %s", data)
        encrypted_data = self.encryption.encrypt(json.dumps(data), self._generate_key(user_id))
        logger.debug("Encrypted data %s", encrypted_data)
        self.server_storage.store(user_id, {EncryptedServerStorageDecorator.ENCRYPTED_KEY: encrypted_data})

    def get(self, user_id):
        data = self.server_storage.get(user_id)
        logger.debug("About to decrypt data %s", data)
        if EncryptedServerStorageDecorator.ENCRYPTED_KEY in data:
            decrypted_data = self.decryption.decrypt(data[EncryptedServerStorageDecorator.ENCRYPTED_KEY], self._generate_key(user_id))
            if settings.EQ_DEV_MODE:
                logger.debug("Decrypted data %s", decrypted_data)
            json_data = json.loads(decrypted_data)
            if settings.EQ_DEV_MODE:
                logger.debug("JSONify %s", json_data)
            return json_data
        else:
            return {}

    def _generate_key(self, user_id):
        salt = settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_SALT
        sha256 = hashlib.sha256()
        sha256.update(to_str(salt).encode('utf-8'))
        sha256.update(to_str(user_id).encode('utf-8'))

        # we only need the first 32 characters for the CEK
        cek = sha256.hexdigest()[:32]
        if settings.EQ_DEV_MODE:
            logger.debug("Generated cek is %s", cek)
        return to_bytes(cek)

    def has_data(self, user_id):
        return self.server_storage.has_data(user_id)

    def delete(self, user_id):
        self.server_storage.delete(user_id)

    def clear(self):
        self.server_storage.clear()
