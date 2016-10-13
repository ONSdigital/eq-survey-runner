import hashlib
import json
import logging

from app import settings
from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
from app.storage.storage_medium import StorageMedium
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = logging.getLogger(__name__)


def _safe_logging(msg, param):
    if settings.EQ_DEV_MODE:
        logger.debug(msg, param)


def generate_key(user_id, user_ik, pepper=settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_PEPPER):
    sha256 = hashlib.sha256()
    sha256.update(to_str(user_id).encode('utf-8'))
    sha256.update(to_str(user_ik).encode('utf-8'))
    sha256.update(to_str(pepper).encode('utf-8'))

    # we only need the first 32 characters for the CEK
    cek = sha256.hexdigest()[:32]
    _safe_logging("Generated cek is %s", cek)
    return to_bytes(cek)


class EncryptedStorage(StorageMedium):

    def __init__(self, server_storage):
        self.encryption = JWEDirEncrypter()
        self.decryption = JWEDirDecrypter()
        self.server_storage = server_storage

    def store(self, data, user_id, user_ik):
        _safe_logging("About to encrypt data %s", data)
        encrypted_data = self.encrypt_data(user_id, user_ik, data)
        _safe_logging("Encrypted data %s", encrypted_data)
        self.server_storage.store(encrypted_data, user_id, user_ik)

    def get(self, user_id, user_ik):
        data = self.server_storage.get(user_id, user_ik)
        _safe_logging("About to decrypt data %s", data)
        if 'data' in data:
            decrypted_data = self.decrypt_data(user_id, user_ik, data)
            _safe_logging("Decrypted data %s", decrypted_data)
            json_data = json.loads(decrypted_data)
            return json_data
        else:
            return {}

    def encrypt_data(self, user_id, user_ik, data):
        sha_key = generate_key(user_id, user_ik)
        encrypted = self.encryption.encrypt(json.dumps(data), sha_key)
        return {'data': encrypted}

    def decrypt_data(self, user_id, user_ik, encrypted_data):
        sha_key = generate_key(user_id, user_ik)
        return self.decryption.decrypt(encrypted_data['data'], sha_key)

    def has_data(self, user_id):
        return self.server_storage.has_data(user_id)

    def delete(self, user_id):
        self.server_storage.delete(user_id)

    def clear(self):
        self.server_storage.clear()
