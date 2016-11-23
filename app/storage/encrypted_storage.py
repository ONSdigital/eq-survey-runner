import hashlib
import json
import logging

from app import settings
from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
from app.storage.database_storage import DatabaseStorage
from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = logging.getLogger(__name__)


def generate_key(user_id, user_ik, pepper=settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION_KEY_PEPPER):
    sha256 = hashlib.sha256()
    sha256.update(to_str(user_id).encode('utf-8'))
    sha256.update(to_str(user_ik).encode('utf-8'))
    sha256.update(to_str(pepper).encode('utf-8'))

    # we only need the first 32 characters for the CEK
    cek = sha256.hexdigest()[:32]
    return to_bytes(cek)


class EncryptedStorage(DatabaseStorage):

    def __init__(self):
        self.encryption = JWEDirEncrypter()
        self.decryption = JWEDirDecrypter()

    def store(self, data, user_id, user_ik=None):
        encrypted_data = self.encrypt_data(user_id, user_ik, data)
        super(EncryptedStorage, self).store(encrypted_data, user_id)

    def get(self, user_id, user_ik=None):
        data = super(EncryptedStorage, self).get(user_id)
        if 'data' in data:
            decrypted_data = self.decrypt_data(user_id, user_ik, data)
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
