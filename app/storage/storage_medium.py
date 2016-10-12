import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


class StorageMedium(metaclass=ABCMeta):
    '''
    Interface which facilitates storage of questionnaire data
    '''
    @abstractmethod
    def store(self, data, user_id, user_ik=None):
        pass

    @abstractmethod
    def get(self, user_id, user_ik=None):
        pass

    @abstractmethod
    def has_data(self, user_id):
        pass

    @abstractmethod
    def delete(self, user_id):
        pass

    @abstractmethod
    def clear(self):
        pass
