import unittest

from app.storage.encrypted_questionnaire_storage import EncryptedQuestionnaireStorage
from app.storage.questionnaire_storage import QuestionnaireStorage
from app.storage.storage_factory import get_storage


class TestStorageFactory(unittest.TestCase):

    def test_database_storage(self):
        self.assertIsInstance(get_storage("1", "key", False), QuestionnaireStorage)

    def test_encrypted_storage(self):
        self.assertIsInstance(get_storage("1", "key", True), EncryptedQuestionnaireStorage)

if __name__ == '__main__':
    unittest.main()
