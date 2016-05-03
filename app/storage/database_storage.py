from app.storage.abstract_server_storage import AbstractServerStorage


class DatabaseStorage(AbstractServerStorage):

    def store(self, user_id, data):
        pass

    def get(self, user_id):
        pass
