#!/bin/bash
# file: build_systemd.sh
# info: builds a docker image with systemd as base for other containers
IMAGE_REGISTRY=${IMAGE_REGISTRY:-odl-registry:4000}
IMAGE_REPO=${IMAGE_REPO:-s3p/systemd}
IMAGE_TAG=${IMAGE_TAG:-v0.1}
IMAGE_NAME="${IMAGE_REGISTRY}/${IMAGE_REPO}:${IMAGE_TAG}"
DOCKERFILE=${DOCKERFILE:-Dockerfile}

echo "Building $IMAGE_NAME from Dockerfile=$DOCKERFILE at $(date) ... "
# shellcheck disable=SC2154
docker build -t ${IMAGE_NAME} -f ${DOCKERFILE} --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy .

if [ $? = 0 ] ; then
    docker images $IMAGE_NAME
    echo "Docker image $IMAGE_NAME built successfully."
    echo "To quickly test it, you can launch it with:"
    # shellcheck disable=SC2154
    echo "docker run -it --rm --env http_proxy=$http_proxy --env https_proxy=$https_proxy --env no_proxy=$no_proxy $IMAGE_NAME bash"
else
    echo "An error occurred during the build of $IMAGE_NAME"
    exit 1
fi

