from flask.ext.session.sessions import SqlAlchemySessionInterface


class Encrypter():
    def __init__(self, serializer):
        self.serializer = serializer

    def dumps(self, object):
        print("Encrypter dumps")
        return self.serializer.dumps(object)

    def dump(self, object):
        return self.serializer.dump(object)

    def loads(self, value):
        print("Encrypter loads")
        return self.serializer.loads(value)

    def load(self, value):
        return self.serializer.load(value)


class EncryptedSqlAlchemySessionInterface(SqlAlchemySessionInterface):

    def __init__(self, app, db, table, key_prefix):
        super().__init__(app, db, table, key_prefix)
        print("Here")
        print(super().serializer)
        self.serializer = Encrypter(super().serializer)
