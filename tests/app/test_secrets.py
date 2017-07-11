from unittest import TestCase

from app.secrets import SecretStore, KEY_PURPOSE_AUTHENTICATION, validate_required_submission_keys
from app.setup import validate_required_secrets


class TestSecrets(TestCase):
    def test_validate_required_secrets_fails_on_missing(self):

        secrets = {
            "secrets": {
            }
        }

        with self.assertRaises(Exception) as exception:
            validate_required_secrets(secrets)

        self.assertIn("Missing Secret [EQ_SERVER_SIDE_STORAGE_USER_ID_SALT]", str(exception.exception))

    def test_validate_required_secrets_fails_on_missing_submission_private_key(self):

        secrets = {
            "keys": {
                "1234567890": {
                    "purpose": "submission",
                    "type": "public",
                    "value": "abc",
                }
            }
        }

        with self.assertRaises(Exception) as exception:
            validate_required_submission_keys(secrets)

        self.assertIn("No private submission key loaded", str(exception.exception))

    def test_validate_required_secrets_fails_on_missing_submission_public_key(self):

        secrets = {
            "keys": {
                "1234567890": {
                    "purpose": "submission",
                    "type": "private",
                    "value": "abc",
                }
            }
        }

        with self.assertRaises(Exception) as exception:
            validate_required_submission_keys(secrets)

        self.assertIn("No public submission key loaded", str(exception.exception))

    def test_validate_required_secrets_fails_on_multiple_submission_public_keys(self):

        secrets = {
            "keys": {
                "1234567890": {
                    "purpose": "submission",
                    "type": "public",
                    "value": "abc",
                },
                "abcdefg": {
                    "purpose": "submission",
                    "type": "public",
                    "value": "def",
                }
            }
        }

        with self.assertRaises(Exception) as exception:
            validate_required_submission_keys(secrets)

        self.assertIn("Multiple public submission keys loaded", str(exception.exception))

    def test_validate_required_secrets_fails_on_multiple_submission_private_keys(self):

        secrets = {
            "keys": {
                "1234567890": {
                    "purpose": "submission",
                    "type": "private",
                    "value": "abc",
                },
                "abcdefg": {
                    "purpose": "submission",
                    "type": "private",
                    "value": "def",
                }
            }
        }

        with self.assertRaises(Exception) as exception:
            validate_required_submission_keys(secrets)

        self.assertIn("Multiple private submission keys loaded", str(exception.exception))

    def test_get_private_key_by_kid_fails_when_no_key(self):
        secrets = SecretStore({
            "keys": {
            }
        })

        kid = "invalid_kid"

        with self.assertRaises(Exception) as exception:
            secrets.get_private_key_by_kid(KEY_PURPOSE_AUTHENTICATION, kid)

        self.assertIn("Invalid Private Key Identifier [{}] for Purpose [{}]".format(kid, KEY_PURPOSE_AUTHENTICATION), str(exception.exception))

    def test_get_public_key_by_kid_fails_when_no_key(self):
        secrets = SecretStore({
            "keys": {
            }
        })

        kid = "invalid_kid"

        with self.assertRaises(Exception) as exception:
            secrets.get_public_key_by_kid(KEY_PURPOSE_AUTHENTICATION, kid)

        self.assertIn("Invalid Public Key Identifier [{}] for Purpose [{}]".format(kid, KEY_PURPOSE_AUTHENTICATION), str(exception.exception))
