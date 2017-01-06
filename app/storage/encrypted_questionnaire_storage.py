import hashlib
import logging

from app import settings
from app.cryptography.jwe_decryption import JWEDirDecrypter
from app.cryptography.jwe_encryption import JWEDirEncrypter
from app.storage.questionnaire_storage import QuestionnaireStorage
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


class EncryptedQuestionnaireStorage(QuestionnaireStorage):

    def __init__(self, user_id, user_ik):
        super().__init__(user_id)
        if user_ik is None:
            raise ValueError('User ik must be set')
        self.encryption = JWEDirEncrypter()
        self.decryption = JWEDirDecrypter()
        self.user_ik = user_ik

    def add_or_update(self, data):
        encrypted_data = self.encrypt_data(data)
        super(EncryptedQuestionnaireStorage, self).add_or_update(encrypted_data)

    def get_user_data(self):
        data = super(EncryptedQuestionnaireStorage, self).get_user_data()
        if 'data' in data:
            decrypted_data = self.decrypt_data(self.user_id, self.user_ik, data)
            return decrypted_data

    def encrypt_data(self, data):
        sha_key = generate_key(self.user_id, self.user_ik)
        encrypted = self.encryption.encrypt(data, sha_key)
        return {'data': encrypted}

    def decrypt_data(self, user_id, user_ik, encrypted_data):
        sha_key = generate_key(user_id, user_ik)
        return self.decryption.decrypt(encrypted_data['data'], sha_key)
