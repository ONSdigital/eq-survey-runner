#!/usr/bin/env python

import argparse
import os
import yaml

import hashlib

from yaml.representer import SafeRepresenter
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PublicFormat

KEY_PURPOSE_AUTHENTICATION = 'authentication'
KEY_PURPOSE_SUBMISSION = 'submission'

# This script generates a yml file in the following format.
# It is made up of two parts. string secrets (passwords) and keys (public and private)
# keys:
#   1234567890123456789012345678901234567890:
#     purpose: submission
#     type: public
#     value: |
#       -----BEGIN PUBLIC KEY-----
#       #######################
#       -----END PUBLIC KEY-----
# secrets:
#   PASSWORD: 'secret_value'


class LiteralUnicode(str):
    pass


def change_style(style, representer):
    """
    This function is used to format the key value as a multi-line string maintaining the line breaks
    """
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer

represent_literal_unicode = change_style('|', SafeRepresenter.represent_str)
yaml.add_representer(LiteralUnicode, represent_literal_unicode)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate Survey Runner secrets file.')
    parser.add_argument('folder', type=str,
                        help='The folder that contains the secrets and keys')

    args = parser.parse_args()

    keys_folder = args.folder


def get_file_contents(folder, filename, trim=False):
    with open(os.path.join(folder, filename), 'r') as f:
        data = f.read()
        if trim:
            data = data.rstrip('\r\n')
    return data


def generate_kid_from_key(dict, key_type, purpose, public_key, private_key=None, kid_override=None):
    if not kid_override:
        hash_object = hashlib.sha1(public_key.encode())
        kid = hash_object.hexdigest()

    key = {
        "type": key_type,
        "purpose": purpose,
        "value": LiteralUnicode(private_key if private_key else public_key),
    }

    dict[kid_override if kid_override else kid] = key


def add_public_key_to_dict(dict, purpose, public_key, kid_override=None):
    public_key_data = get_file_contents(keys_folder, public_key)

    generate_kid_from_key(dict, "public", purpose, public_key_data, kid_override=kid_override)


def add_private_key_to_dict(dict, purpose, private_key, kid_override=None):
    private_key_data = get_file_contents(keys_folder, private_key)

    private_key = load_pem_private_key(private_key_data.encode(), None, backend=backend)

    pub_key = private_key.public_key()

    pub_bytes = pub_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

    generate_kid_from_key(dict, "private", purpose, pub_bytes.decode(), private_key_data, kid_override=kid_override)

keys = {}

add_public_key_to_dict(keys, KEY_PURPOSE_SUBMISSION, 'sdc-submission-encryption-sdx-public-key.pem')
add_public_key_to_dict(keys, KEY_PURPOSE_AUTHENTICATION, 'sdc-user-authentication-signing-rrm-public-key.pem')

add_private_key_to_dict(keys, KEY_PURPOSE_AUTHENTICATION, 'sdc-user-authentication-encryption-sr-private-key.pem')
add_private_key_to_dict(keys, KEY_PURPOSE_SUBMISSION, 'sdc-submission-signing-sr-private-key.pem')


# Support depricated kid value until it is no longer used
add_public_key_to_dict(keys, KEY_PURPOSE_AUTHENTICATION, 'sdc-user-authentication-signing-rrm-public-key.pem', kid_override='EDCRRM')
# Support default value until all upstream systems are passing kid
add_private_key_to_dict(keys, KEY_PURPOSE_AUTHENTICATION, 'sdc-user-authentication-encryption-sr-private-key.pem',
                        kid_override='EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY')

secrets = {}

secrets['EQ_SERVER_SIDE_STORAGE_USER_ID_SALT'] = get_file_contents(keys_folder, 'eq-server-side-storage-user-id-salt.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_USER_IK_SALT'] = get_file_contents(keys_folder, 'eq-server-side-storage-user-ik-salt.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER'] = get_file_contents(keys_folder, 'eq-server-side-storage-encryption-user-pepper.txt', True)
secrets['EQ_SECRET_KEY'] = get_file_contents(keys_folder, 'eq-secret-key.txt', True)

secrets['EQ_RABBITMQ_USERNAME'] = get_file_contents(keys_folder, 'eq-rabbitmq-username.txt', True)
secrets['EQ_RABBITMQ_PASSWORD'] = get_file_contents(keys_folder, 'eq-rabbitmq-password.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_DATABASE_USERNAME'] = get_file_contents(keys_folder, 'eq-server-side-storage-database-username.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_DATABASE_PASSWORD'] = get_file_contents(keys_folder, 'eq-server-side-storage-database-password.txt', True)

with open('secrets.yml', 'w') as f:
    yaml.dump({"keys": keys, "secrets": secrets}, f, default_flow_style=False)
