from unittest import TestCase

from app.setup import validate_required_secrets


class TestSecrets(TestCase):
    def test_validate_required_secrets_fails_on_missing(self):

        secrets = {
            ""
        }

        with self.assertRaises(Exception) as exception:
            validate_required_secrets(secrets)

        self.assertIn("Missing Secret [EQ_SUBMISSION_SDX_PUBLIC_KEY]", str(exception.exception))
