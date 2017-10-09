#!/bin/bash -e

echo  $Password | gpg -o secure-data.tar --passphrase-fd 0 --batch /opt/keys/secure-data.tar.gpg
tar xvf secure-data.tar

python scripts/generate_secrets.py secure-data/
python -m sdc.crypto.scripts.generate_keys secure-data/
