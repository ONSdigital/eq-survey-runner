import unittest

from app import settings
from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from app.storage.questionnaire_storage import QuestionnaireStorage
from app.storage.storage_factory import get_storage


class TestStorageFactory(unittest.TestCase):

    def test_database_storage(self):
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION = False
        self.assertIsInstance(get_storage("1", "key"), QuestionnaireStorage)

    def test_encrypted_storage(self):
        settings.EQ_SERVER_SIDE_STORAGE_ENCRYPTION = True
        self.assertIsInstance(get_storage("1", "key"), EncryptedQuestionnaireStorage)

if __name__ == '__main__':
    unittest.main()
