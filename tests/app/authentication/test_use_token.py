from unittest import TestCase
from uuid import uuid4

from mock import patch
from sqlalchemy.exc import IntegrityError

from app.authentication.jti_claim_storage import use_jti_claim, JtiTokenUsed


class TestJtiClaimStorage(TestCase):

    def test_should_use_token(self):
        with patch('app.authentication.jti_claim_storage.db_session') as db_session:
            # Given
            jti_token = str(uuid4())

            # When
            use_jti_claim(jti_token)

            # Then
            self.assertEqual(db_session.add.call_count, 1)

    def test_should_return_raise_value_error(self):
        # Given
        token = None

        # When
        with self.assertRaises(ValueError):
            use_jti_claim(token)

    def test_should_raise_jti_token_used_when_token_already_exists(self):
        with patch('app.authentication.jti_claim_storage.db_session') as db_session:
            # Given
            jti_token = str(uuid4())
            db_session.add.side_effect = [IntegrityError('', '', '')]

            # When
            with self.assertRaises(JtiTokenUsed) as err:
                use_jti_claim(jti_token)

            # Then
            self.assertEqual(err.exception.jti_claim, jti_token)

    def test_should_raise_type_error_invalid_uuid(self):
        jti_token = 'jti_token'

        with self.assertRaises(TypeError):
            use_jti_claim(jti_token)
