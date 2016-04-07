from flask.sessions import SecureCookieSessionInterface
import hashlib


class SHA256SecureCookieSessionInterface(SecureCookieSessionInterface):

    @staticmethod
    def digest_method():
        return hashlib.sha256()
