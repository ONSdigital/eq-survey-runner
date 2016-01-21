from flask import request
import jwt


class NoTokenException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class InvalidTokenException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


def decode_token(encrypted_token):
    try:
        if encrypted_token:
            decrypted_token = jwt.decode(encrypted_token, 'secret')
            print (decrypted_token)
            return decrypted_token
        else:
            raise NoTokenException("JWT Missing")
    except jwt.DecodeError as e:
        raise InvalidTokenException(repr(e))
