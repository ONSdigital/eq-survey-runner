from uuid import uuid4

from mock import patch
from sqlalchemy.exc import IntegrityError

from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from tests.app.app_context_test_case import AppContextTestCase


class TestJtiClaimStorage(AppContextTestCase):

    def test_should_use_token(self):
        # Given
        jti_token = str(uuid4())

        # When
        with patch('app.data_model.models.db.session.add') as add:
            use_jti_claim(jti_token)

            # Then
            self.assertEqual(add.call_count, 1)

    def test_should_return_raise_value_error(self):
        # Given
        token = None

        # When
        with self.assertRaises(ValueError):
            use_jti_claim(token)

    def test_should_raise_jti_token_used_when_token_already_exists(self):
        # Given
        jti_token = str(uuid4())

        # When
        with self.assertRaises(JtiTokenUsed) as err:
            with patch('app.data_model.models.db.session.add', side_effect=[IntegrityError('', '', '')]):
                use_jti_claim(jti_token)

        # Then
        self.assertEqual(err.exception.jti_claim, jti_token)
        self.assertEqual(str(err.exception), "jti claim '{}' has already been used".format(jti_token))

    def test_should_raise_type_error_invalid_uuid(self):
        jti_token = 'jti_token'

        with self.assertRaises(TypeError):
            use_jti_claim(jti_token)
