from app.storage.abstract_server_storage import AbstractServerStorage


DATA = {}


class InMemoryStorage(AbstractServerStorage):
    '''
    In memory server side storage used for testing
    '''

    def store(self, data, user_id, user_ik=None):
        DATA[user_id] = data

    def get(self, user_id, user_ik=None):
        if self.has_data(user_id):
            return DATA[user_id]
        else:
            return None

    def has_data(self, user_id):
        return user_id in DATA

    def delete(self, user_id):
        del DATA[user_id]

    def clear(self):
        DATA.clear()
