#!/usr/bin/env bash

set -e

if [[ -z "$1" ]]; then
  echo "SUBMISSION_BUCKET_NAME is mandatory"
  exit 1
fi

SUBMISSION_BUCKET_NAME=$1
DOCKER_REGISTRY="${2:-eu.gcr.io/census-eq-ci}"
IMAGE_TAG="${3:-latest}"
MANAGED_CERTIFICATE_NAME="${4:-}"

helm tiller run \
    helm upgrade --install \
    survey-runner \
    k8s/helm \
    --set submissionBucket=${SUBMISSION_BUCKET_NAME} \
    --set image.repository=${DOCKER_REGISTRY}/eq-survey-runner \
    --set image.tag=${IMAGE_TAG} \
    --set ingress.managedCertificateName=${MANAGED_CERTIFICATE_NAME}
