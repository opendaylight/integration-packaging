#!/bin/bash
# file: build_service.sh
# info: builds a docker service image
IMAGE_BASE=s3p/service
IMAGE_TAG=v0.1

if [ -n "$1" ] ; then
    # use arg as image tag if supplied
    IMAGE_TAG="$1"
fi
IMAGE_NAME=${IMAGE_BASE}:${IMAGE_TAG}
DOCKERFILE="Dockerfile"

echo "Building $IMAGE_NAME from Dockerfile=$DOCKERFILE at $(date) ... "
docker build -t ${IMAGE_NAME} -f ${DOCKERFILE} \
    --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy .
