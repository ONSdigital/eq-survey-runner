#!/usr/bin/env bash

set -e

if [[ -z "$1" ]]; then
  echo "SUBMISSION_BUCKET_NAME is mandatory"
  exit 1
fi

#PROJECT_ID=$1
SUBMISSION_BUCKET_NAME=$1
IMAGE_TAG="${2:-latest}"

helm tiller run \
    helm upgrade --install \
    survey-runner \
    k8s/helm \
    --set submissionBucket=${SUBMISSION_BUCKET_NAME} \
    --set image.tag=${IMAGE_TAG}
