#!/bin/bash
# file: ./run_compute.sh
# info: spawns a docker compute image
# dependencies: assumes proxy variables are defined in the local environment

# image selection
IMAGE_REPO="s3p/compute"
IMAGE_VERSION="v0.1"
IMAGE_NAME="${IMAGE_REPO}:${IMAGE_VERSION}"

# image configuration
HOST_ID=01
COMP_ID=07
NAME=compute-${HOST_ID}-${COMP_ID}
ODL_NETWORK=false
CAPABILITIES="--privileged --cap-add ALL --security-opt apparmor=docker-unconfined "
MOUNTS="-v /dev:/dev -v /lib/modules:/lib/modules "
STACK_PASS=stack
SERV_HOST=172.17.0.3
# TODO dynamically configure SERV_HOST
# define _no_proxy based on the cluster topology
_no_proxy=localhost,10.0.0.0/8,192.168.0.0/16,172.17.0.0/16,127.0.0.0/8

if [ -n "$1" ] ; then
    echo "Command argument supplied, running \"$1\" in $NAME..."
    COMMAND="$1"
fi

docker run -it --rm --name ${NAME} --hostname ${NAME} \
    --env http_proxy=$http_proxy --env https_proxy=$https_proxy \
    --env no_proxy=$_no_proxy \
    --env ODL_NETWORK=$ODL_NETWORK \
    --env STACK_PASS=$STACK_PASS \
    --env SERV_HOST=$SERV_HOST \
    $MOUNTS \
    $CAPABILITIES $IMAGE_NAME \
    $COMMAND

