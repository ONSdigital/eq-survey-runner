#!/usr/bin/env bash

set -e

if [[ -z "$SUBMISSION_BUCKET_NAME" ]]; then
  echo "SUBMISSION_BUCKET_NAME is mandatory"
  exit 1
fi

DOCKER_REGISTRY="${DOCKER_REGISTRY:-eu.gcr.io/census-eq-ci}"
IMAGE_TAG="${IMAGE_TAG:-latest}"

helm tiller run \
    helm upgrade --install \
    survey-runner \
    k8s/helm \
    --set submissionBucket=${SUBMISSION_BUCKET_NAME} \
    --set googleTagManagerId=${GOOGLE_TAG_MANAGER_ID} \
    --set googleTagManagerAuth=${GOOGLE_TAG_MANAGER_AUTH} \
    --set googleTagManagerPreview=${GOOGLE_TAG_MANAGER_PREVIEW} \
    --set image.repository=${DOCKER_REGISTRY}/eq-survey-runner \
    --set image.tag=${IMAGE_TAG} \
    --set cookieSettingsUrl=${COOKIE_SETTINGS_URL} \
