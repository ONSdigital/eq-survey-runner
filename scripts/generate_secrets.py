#!/usr/bin/env python

import argparse
import os
import yaml


# This script generates a yml file in the following format.
# It is made up of string secrets (passwords). Keys are generated and stored elsewhere.
# secrets:
#   PASSWORD: 'secret_value'


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate Survey Runner secrets file.')
    parser.add_argument('folder', type=str, help='The folder that contains the secrets')

    args = parser.parse_args()

    keys_folder = args.folder


def get_file_contents(folder, filename, trim=False):
    with open(os.path.join(folder, filename), 'r') as f:
        data = f.read()
        if trim:
            data = data.rstrip('\r\n')
    return data


secrets = {}

secrets['EQ_SERVER_SIDE_STORAGE_USER_ID_SALT'] = get_file_contents(
    keys_folder, 'eq-server-side-storage-user-id-salt.txt', True
)
secrets['EQ_SERVER_SIDE_STORAGE_USER_IK_SALT'] = get_file_contents(
    keys_folder, 'eq-server-side-storage-user-ik-salt.txt', True
)
secrets['EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER'] = get_file_contents(
    keys_folder, 'eq-server-side-storage-encryption-user-pepper.txt', True
)
secrets['EQ_SECRET_KEY'] = get_file_contents(keys_folder, 'eq-secret-key.txt', True)

secrets['EQ_RABBITMQ_USERNAME'] = get_file_contents(
    keys_folder, 'eq-rabbitmq-username.txt', True
)
secrets['EQ_RABBITMQ_PASSWORD'] = get_file_contents(
    keys_folder, 'eq-rabbitmq-password.txt', True
)

with open('secrets.yml', 'w') as f:
    yaml.dump({"secrets": secrets}, f, default_flow_style=False)
