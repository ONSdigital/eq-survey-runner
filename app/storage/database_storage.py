from sqlalchemy import Table, Column, MetaData, String
from app.storage.abstract_server_storage import AbstractServerStorage

metadata = MetaData()

state = Table('state', metadata, Column('user_id', String, primary_key=True), Column('questionnaire-state', String))


class DatabaseStore(AbstractServerStorage):
    '''
    Server side storage using an RDS database (where one column is the entire JSON representation of the questionnaire state)
    '''
    def store(self, data, user_id):
        pass

    def get(self, user_id):
        pass

    def has_data(self, user_id):
        pass

    def delete(self, user_id):
        pass
