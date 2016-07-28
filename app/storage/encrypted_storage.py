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

    JSON_DATA_KEY = 'data'

    def __init__(self, server_storage):
        self.encryption = JWEDirEncrypter()
        self.decryption = JWEDirDecrypter()
        self.server_storage = server_storage

    def store(self, data, user_id, user_ik):
        self.safe_logging("About to encrypt data %s", data)
        encrypted_data = self.encrypt_data(user_id, user_ik, data)
        # self.safe_logging("Encrypted data %s", encrypted_data)
        self.server_storage.store(encrypted_data, user_id, user_ik)

    def get(self, user_id, user_ik):
        data = self.server_storage.get(user_id, user_ik)
        self.safe_logging("About to decrypt data %s", data)
        if EncryptedServerStorageDecorator.JSON_DATA_KEY in data:
            decrypted_data = self.decrypt_data(user_id, user_ik, data)
            self.safe_logging("Decrypted data %s", decrypted_data)
            json_data = json.loads(decrypted_data)
            return json_data
        else:
            return {}

    def encrypt_data(self, user_id, user_ik, data):
        return self.wrap_data(self.encryption.encrypt(json.dumps(data), self._generate_key(user_id, user_ik)))

    def decrypt_data(self, user_id, user_ik, data):
        return self.decryption.decrypt(self.unwrap_data(data), self._generate_key(user_id, user_ik))

    def wrap_data(self, encrypted_data):
        '''
        Wraps the encrypted data as a JSON structure so we can reuse the storage classes
        :param encrypted_data: the encrypted data
        :return: a dict containing the JSON data
        '''
        return {EncryptedServerStorageDecorator.JSON_DATA_KEY: encrypted_data}

    def unwrap_data(self, encrypted_data):
        return encrypted_data[EncryptedServerStorageDecorator.JSON_DATA_KEY]

    def _generate_key(self, user_id, user_ik):
        pepper = settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_PEPPER
        sha256 = hashlib.sha256()
        sha256.update(to_str(user_id).encode('utf-8'))
        sha256.update(to_str(user_ik).encode('utf-8'))
        sha256.update(to_str(pepper).encode('utf-8'))

        # we only need the first 32 characters for the CEK
        cek = sha256.hexdigest()[:32]
        self.safe_logging("Generated cek is %s", cek)
        return to_bytes(cek)

    def has_data(self, user_id):
        return self.server_storage.has_data(user_id)

    def delete(self, user_id):
        self.server_storage.delete(user_id)

    def clear(self):
        self.server_storage.clear()

    def safe_logging(self, msg, param):
        '''
        Only log when DEV mode is enabled and at DEBUG log level
        '''
        if settings.EQ_DEV_MODE:
            logger.debug(msg, param)
