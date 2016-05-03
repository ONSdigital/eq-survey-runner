

class AbstractServerStorage(object):
    '''
    Interface which facilitates server side storage of questionnaire data
    '''
    def store(self, user_id, data):
        pass

    def get(self, user_id):
        pass
