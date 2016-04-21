#!/bin/bash -e

echo  $Password | gpg -o secure-data.tar --passphrase-fd 0 --batch /opt/keys/secure-data.tar.gpg
tar xvf secure-data.tar

mkdir -p key_mat

cp secure-data/sdc-user-authentication-signing-rrm-public-key.pem key_mat
cp secure-data/sdc-user-authentication-encryption-sr-private-key.pem key_mat
cp secure-data/sdc-submission-encryption-sdx-public-key.pem key_mat
cp secure-data/sdc-submission-signing-sr-private-key.pem key_mat
cp secure-data/sdc-user-authentication-signing-rrm-private-key.pem key_mat
cp secure-data/sdc-user-authentication-encryption-sr-public-key.pem key_mat

EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY="./key_mat/sdc-user-authentication-signing-rrm-public-key.pem"
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY="./key_mat/sdc-user-authentication-encryption-sr-private-key.pem"
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD=`cat secure-data/sdc-user-authentication-encryption-sr-private-key-password.txt`

# needed for DEV mode
EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY="./key_mat/sdc-user-authentication-signing-rrm-private-key.pem"
EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY="./key_mat/sdc-user-authentication-encryption-sr-public-key.pem"
EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD=`cat secure-data/sdc-user-authentication-signing-rrm-private-key-password.txt`

EQ_SUBMISSION_SDX_PUBLIC_KEY="./key_mat/sdc-submission-encryption-sdx-public-key.pem"
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY="./key_mat/sdc-submission-signing-sr-private-key.pem"
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD=`cat secure-data/sdc-submission-signing-sr-private-key-password.txt`


cat << EOF >> ./.ebextensions/secure.config
option_settings:
  - option_name: EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY
    value: ${EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY}

  - option_name: EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY
    value: ${EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY}

  - option_name: EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD
    value: ${EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD}

  - option_name: EQ_SUBMISSION_SDX_PUBLIC_KEY
    value: ${EQ_SUBMISSION_SDX_PUBLIC_KEY}

  - option_name: EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY
    value: ${EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY}

  - option_name: EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY
    value: ${EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY}

  - option_name: EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY
    value: ${EQ_USER_AUTHENTICATION_SR_PUBLIC_KEY}

  - option_name: EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD
    value: ${EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD}

  - option_name: EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD
    value: ${EQ_USER_AUTHENTICATION_RRM_PRIVATE_KEY_PASSWORD}

EOF


