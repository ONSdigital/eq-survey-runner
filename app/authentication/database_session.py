from flask.ext.session.sessions import SqlAlchemySessionInterface
from app.cryptography.jwe_encryption import JWEDirEncrypter
from app.cryptography.jwe_decryption import JWEDirDecrypter
from app import settings
from flask_login import current_user

# this doesn't work I need to create a user survey state table
# the session literally needs to hold the user id which probably can just be stored in the cookie



class Encrypter():

    def __init__(self, serializer):
        self.encryption = JWEDirEncrypter(settings.EQ_SESSION_STORAGE_ENCRYPTION_KEY)
        self.decryption = JWEDirDecrypter(settings.EQ_SESSION_STORAGE_ENCRYPTION_KEY)
        self.serializer = serializer

    def dumps(self, object):

        print("Encrypter dumps")
        print(object)

        serialize = self.serializer.dumps(object)
        encrypted_data = self.encryption.encrypt(serialize, current_user.get_user_id().encode())
        print(encrypted_data)
        return encrypted_data

    def dump(self, object):
        print("Encrypter dump")
        return self.serializer.dump(object)

    def loads(self, value):
        print("Encrypter loads")
        decrypted_data = self.decryption.decrypt(value)
        object = self.serializer.loads(decrypted_data)
        return object

    def load(self, value):
        print("Encrypter load")
        return self.serializer.load(value)


class EncryptedSqlAlchemySessionInterface(SqlAlchemySessionInterface):

    def __init__(self, app, db, table, key_prefix):
        super().__init__(app, db, table, key_prefix)
        print("Here")
        print(super().serializer)
        self.serializer = Encrypter(super().serializer)
