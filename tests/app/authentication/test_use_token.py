from datetime import datetime, timedelta
from uuid import uuid4

from dateutil.tz import tzutc
from mock import patch

from app.authentication.jti_claim_storage import JtiTokenUsed, use_jti_claim
from app.storage.errors import ItemAlreadyExistsError
from tests.app.app_context_test_case import AppContextTestCase


class TestJtiClaimStorage(AppContextTestCase):

    def test_should_use_token(self):
        # Given
        jti_token = str(uuid4())
        expires = datetime.now(tz=tzutc()) + timedelta(seconds=60)

        # When

        with patch('app.storage.data_access.put') as add:
            use_jti_claim(jti_token, expires)

            # Then
            self.assertEqual(add.call_count, 1)

    def test_should_return_raise_value_error(self):
        # Given
        token = None
        expires = datetime.now(tz=tzutc()) + timedelta(seconds=60)

        # When
        with self.assertRaises(ValueError):
            use_jti_claim(token, expires)

    def test_should_raise_jti_token_used_when_token_already_exists(self):
        # Given
        jti_token = str(uuid4())
        expires = datetime.now(tz=tzutc()) + timedelta(seconds=60)

        # When
        with self.assertRaises(JtiTokenUsed) as err:
            with patch('app.storage.data_access.put', side_effect=[ItemAlreadyExistsError()]):
                use_jti_claim(jti_token, expires)

        # Then
        self.assertEqual(err.exception.jti_claim, jti_token)
        self.assertEqual(str(err.exception), "jti claim '{}' has already been used".format(jti_token))

    def test_should_raise_type_error_invalid_uuid(self):
        jti_token = 'jti_token'
        expires = datetime.now(tz=tzutc()) + timedelta(seconds=60)

        with self.assertRaises(TypeError):
            use_jti_claim(jti_token, expires)
