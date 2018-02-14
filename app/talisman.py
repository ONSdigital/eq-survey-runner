import copy
import random
import string

from flask import request
from flask_talisman import Talisman as BaseTalisman

NONCE_LENGTH = 16


class Talisman(BaseTalisman):
    """Extends Talisman to support CSP nonce rotation
    """

    def init_app(self, app, **kwargs):  # pylint: disable=arguments-differ
        self.content_security_policy_nonce_in = kwargs.pop('content_security_policy_nonce_in', [])

        super().init_app(app, **kwargs)

        self.app.before_request(self._make_nonce)

    @staticmethod
    def _make_nonce():
        if not getattr(request, 'csp_nonce', None):
            request.csp_nonce = get_random_string(NONCE_LENGTH)

    def _set_content_security_policy_headers(self, headers):
        """Patches the content_security_policy to add the request-specific nonce value
        """
        original_policy = self.local_options.content_security_policy

        if self.content_security_policy_nonce_in and hasattr(request, 'csp_nonce'):
            policy = copy.deepcopy(original_policy)

            for section in self.content_security_policy_nonce_in:
                policy[section].append("'nonce-{}'".format(request.csp_nonce))

            setattr(self.local_options, 'content_security_policy', policy)

        super()._set_content_security_policy_headers(headers)

        # reset the original policy
        setattr(self.local_options, 'content_security_policy', original_policy)


def get_random_string(length):
    allowed_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(
        random.SystemRandom().choice(allowed_chars)
        for _ in range(length))
