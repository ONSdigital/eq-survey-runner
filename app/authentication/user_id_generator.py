import binascii

from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from structlog import get_logger

from app.utilities.strings import to_bytes
from app.utilities.strings import to_str

logger = get_logger()


class UserIDGenerator:
    def __init__(self, iterations, user_id_salt, user_ik_salt):
        if user_id_salt is None:
            raise ValueError('user_id_salt is required')
        if user_ik_salt is None:
            raise ValueError('user_ik_salt is required')

        self._iterations = iterations
        self._user_id_salt = user_id_salt
        self._user_ik_salt = user_ik_salt

    def generate_id(self, response_id):
        salt = to_bytes(self._user_id_salt)
        user_id = self._generate(response_id, salt)
        return to_str(user_id)

    def generate_ik(self, response_id):
        salt = to_bytes(self._user_ik_salt)
        user_ik = self._generate(response_id, salt)
        return to_str(user_ik)

    def _generate(self, key_material, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self._iterations,
            backend=backend,
        )
        generated_key = kdf.derive(to_bytes(key_material))
        return binascii.hexlify(generated_key)
