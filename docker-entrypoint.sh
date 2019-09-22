#!/bin/bash

if [ -n "$SECRETS_S3_BUCKET" ]; then
    echo "Load Secrets from S3 Bucket [$SECRETS_S3_BUCKET]"
    aws s3 sync s3://$SECRETS_S3_BUCKET/ /secrets
fi

gunicorn -w $GUNICORN_WORKERS --keep-alive $GUNICORN_KEEP_ALIVE --worker-class gevent -b 0.0.0.0:5000 application:application
