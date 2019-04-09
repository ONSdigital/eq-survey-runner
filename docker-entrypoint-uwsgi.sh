#!/bin/bash

if [ -n "$SECRETS_S3_BUCKET" ]; then
    echo "Load Secrets from S3 Bucket [$SECRETS_S3_BUCKET]"
    aws s3 sync s3://$SECRETS_S3_BUCKET/ /secrets
fi

uwsgi --gevent $GUNICORN_WORKERS --http 0.0.0.0:5000 --buffer-size=32768 --protocol uwsgi --plugins python3 --module application:application
