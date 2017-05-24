import os

import yaml
import sys


def get_file_contents(folder, filename, trim=False):
    with open(os.path.join(folder, filename), 'r') as f:
        data = f.read()
        if trim:
            data = data.rstrip('\r\n')
    return data

if len(sys.argv) < 2:
    raise Exception("Please specify the directory containing the secrets")

keys_folder = sys.argv[1]

keys = {}

keys['EQ_SUBMISSION_SDX_PUBLIC_KEY'] = get_file_contents(keys_folder, 'sdc-submission-encryption-sdx-public-key.pem')
keys['EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY'] = get_file_contents(keys_folder, 'sdc-submission-signing-sr-private-key.pem')

keys['EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY'] = get_file_contents(keys_folder, 'sdc-user-authentication-signing-rrm-private-key.pem')
keys['EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY'] = get_file_contents(keys_folder, 'sdc-user-authentication-signing-rrm-public-key.pem')

keys['EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY'] = get_file_contents(keys_folder, 'sdc-user-authentication-encryption-sr-private-key.pem')
keys['EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY'] = get_file_contents(keys_folder, 'sdc-user-authentication-encryption-sr-public-key.pem')

with open('secrets.yml', 'w') as f:
    yaml.dump(keys, f, default_flow_style=False, default_style='|')

secrets = {}

secrets['EQ_SERVER_SIDE_STORAGE_USER_ID_SALT'] = get_file_contents(keys_folder, 'eq-server-side-storage-user-id-salt.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_USER_IK_SALT'] = get_file_contents(keys_folder, 'eq-server-side-storage-user-ik-salt.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_ENCRYPTION_USER_PEPPER'] = get_file_contents(keys_folder, 'eq-server-side-storage-encryption-user-pepper.txt', True)
secrets['EQ_SECRET_KEY'] = get_file_contents(keys_folder, 'eq-secret-key.txt', True)

secrets['EQ_RABBITMQ_USERNAME'] = get_file_contents(keys_folder, 'eq-rabbitmq-username.txt', True)
secrets['EQ_RABBITMQ_PASSWORD'] = get_file_contents(keys_folder, 'eq-rabbitmq-password.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_DATABASE_USERNAME'] = get_file_contents(keys_folder, 'eq-server-side-storage-database-username.txt', True)
secrets['EQ_SERVER_SIDE_STORAGE_DATABASE_PASSWORD'] = get_file_contents(keys_folder, 'eq-server-side-storage-database-password.txt', True)

secrets['EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD'] = get_file_contents(keys_folder, 'sdc-submission-signing-sr-private-key-password.txt', True)
secrets['EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD'] = \
    get_file_contents(keys_folder, 'sdc-user-authentication-signing-rrm-private-key-password.txt', True)
secrets['EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD'] = \
    get_file_contents(keys_folder, 'sdc-user-authentication-encryption-sr-private-key-password.txt', True)

with open('secrets.yml', 'a') as f:
    yaml.dump(secrets, f, default_flow_style=False)
