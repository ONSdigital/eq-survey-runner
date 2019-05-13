from unittest import TestCase

from app.secrets import validate_required_secrets, EXPECTED_SECRETS


class TestSecrets(TestCase):
    def test_validate_required_secrets_fails_on_missing(self):

        secrets = {'secrets': {}}

        with self.assertRaises(Exception) as exception:
            validate_required_secrets(secrets)

        self.assertIn(
            'Missing Secret [EQ_SERVER_SIDE_STORAGE_USER_ID_SALT]',
            str(exception.exception),
        )

    def test_validate_required_secrets_passes(self):
        secrets = {'secrets': {secret: 'abc' for secret in EXPECTED_SECRETS}}
        self.assertIsNone(validate_required_secrets(secrets))
