#!/bin/bash -e

mv Keys $Keys

echo $Password | gpg -o secure-data.tar --passphrase-fd 0 --batch $Keys
tar xvf secure-data.tar

python scripts/generate_secrets.py secure-data/
python -m sdc.crypto.scripts.generate_keys secure-data/
