#!/bin/bash
# file: build_compute.sh
# info: builds a docker compute image
IMAGE_BASE=s3p/compute
IMAGE_TAG=v0.2
if [ -n "$1" ] ; then
    # use arg as image tag if supplied
    IMAGE_TAG="$1"
fi
IMAGE_NAME=$IMAGE_BASE:$IMAGE_TAG
DOCKERFILE=Dockerfile

echo "Building $IMAGE_NAME from Dockerfile=$DOCKERFILE at $(date) ... "
docker build -t ${IMAGE_NAME} -f ${DOCKERFILE} \
# noqa ShellCheckBear
    --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy .

if [ $? = 0 ] ; then
    PROXIES=""
    if [ -n "$http_proxy" ] ; then
        # noqa ShellCheckBear
        PROXIES="--env http_proxy=$http_proxy --env https_proxy=$https_proxy --env no_proxy=$no_proxy"
    fi
    echo "Docker image $IMAGE_NAME built successfully."
    docker images $IMAGE_NAME
    echo "You can launch it with the following example command:"
    echo "  docker run -it --rm $PROXIES $IMAGE_NAME bash"
else
    echo "An error occurred during the build of $IMAGE_NAME"
fi

