#!/bin/bash -e

mv Keys $Keys

echo $Password | gpg -o secure-data.tar --passphrase-fd 0 --batch $Keys
tar xvf secure-data.tar

mkdir -p key_mat

cp secure-data/rrm-public.pem key_mat
cp secure-data/sr-private.pem key_mat
cp secure-data/sdx-public.pem key_mat
cp secure-data/sr-private-encryption.pem key_mat

EQ_USER_AUTHENTICATION_RRM_PUBLIC_KEY="./key_mat/rrm-public.pem"
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY="./key_mat/sr-private.pem"
EQ_USER_AUTHENTICATION_SR_PRIVATE_KEY_PASSWORD=`cat secure-data/sr-private-password.txt`

EQ_SUBMISSION_SDX_PUBLIC_KEY="./key_mat/sdx-public.pem"
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY="./key_mat/sr-private-encryption.pem"
EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD=`cat secure-data/sr-private-encryption-password.txt`


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

  - option_name: EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD
    value: ${EQ_SUBMISSION_SR_PRIVATE_SIGNING_KEY_PASSWORD}

EOF


