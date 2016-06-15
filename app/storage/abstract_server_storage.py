import logging

logger = logging.getLogger(__name__)


class AbstractServerStorage(object):
    '''
    Interface which facilitates server side storage of questionnaire data
    '''
    def store(self, data, user_id, user_ik=None):
        pass

    def get(self, user_id, user_ik=None):
        pass

    def has_data(self, user_id):
        pass

    def delete(self, user_id):
        pass

    def clear(self):
        pass
