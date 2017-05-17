from unittest import TestCase
from uuid import uuid4

from mock import MagicMock
from sqlalchemy.exc import IntegrityError

from app import Database
from app.authentication.jti_claim_storage import JtiTokenUsed, JtiClaimStorage


class TestJtiClaimStorage(TestCase):

    def setUp(self):
        super().setUp()
        self.database = MagicMock(Database("sqlite://", 1, 0))
        self.jti_claim_storage = JtiClaimStorage(self.database)

    def test_should_use_token(self):


        # Given
        jti_token = str(uuid4())

        # When
        self.jti_claim_storage.use_jti_claim(jti_token)

        # Then
        self.assertEqual(self.database.add.call_count, 1)

    def test_should_return_raise_value_error(self):
        # Given
        token = None

        # When
        with self.assertRaises(ValueError):
            self.jti_claim_storage.use_jti_claim(token)

    def test_should_raise_jti_token_used_when_token_already_exists(self):
        # Given
        jti_token = str(uuid4())
        self.database.add.side_effect = [IntegrityError('', '', '')]

        # When
        with self.assertRaises(JtiTokenUsed) as err:
            self.jti_claim_storage.use_jti_claim(jti_token)

        # Then
        self.assertEqual(err.exception.jti_claim, jti_token)

    def test_should_raise_type_error_invalid_uuid(self):
        jti_token = 'jti_token'

        with self.assertRaises(TypeError):
            self.jti_claim_storage.use_jti_claim(jti_token)
