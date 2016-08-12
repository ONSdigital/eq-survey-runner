import hashlib

from flask.sessions import SecureCookieSessionInterface


class SHA256SecureCookieSessionInterface(SecureCookieSessionInterface):

    @staticmethod
    def digest_method():
        return hashlib.sha256()
