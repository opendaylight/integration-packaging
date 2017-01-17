#!/bin/bash
# file: ./run_compute.sh
# info: spawns a docker compute image
# dependencies: assumes proxy variables are defined in the local environment

# image selection
IMAGE_REPO="s3p/compute"
IMAGE_VERSION="v0.1" # v0.1==Ubuntu 14.04
IMAGE_NAME="${IMAGE_REPO}:${IMAGE_VERSION}"

# image configuration
HOST_ID=01
COMP_ID=04
NAME=compute-${HOST_ID}-${COMP_ID}
ODL_NETWORK=false
# when running on a RHEL-derivative host, use "--security-opt seccomp=unconfined"
CAPABILITIES="--privileged --cap-add ALL --security-opt apparmor=docker-unconfined "
CGROUP_MOUNT=""
MOUNTS="-v /dev:/dev -v /lib/modules:/lib/modules $CGROUP_MOUNT "
STACK_PASS=stack
SERV_HOST=10.20.0.2
# TODO dynamically configure SERV_HOST
# define _no_proxy based on the cluster topology
_no_proxy=localhost,10.0.0.0/8,192.168.0.0/16,172.17.0.0/16,127.0.0.1,127.0.0.0/8,$SERV_HOST

#if [ -n "$1" ] ; then
#    echo "Command argument supplied, running \"$1\" in $NAME..."
#    COMMAND="$1"
#fi

SERVICE_NODE_NAME="service-node"
# check to see that service-node is running first and get its IP from Docker
SERVICE_NODE_IP=$(docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" service-node)
if [ -z "$SERVICE_NODE_IP" ] ; then
    echo NO service node is available on overlay-net
else
    SERV_HOST=$SERVICE_NODE_IP
    docker run -dit --name ${NAME} --hostname ${NAME} \
        --env http_proxy=$http_proxy --env https_proxy=$https_proxy \
        --env no_proxy=$_no_proxy \
        --env ODL_NETWORK=$ODL_NETWORK \
        --env STACK_PASS=$STACK_PASS \
        --env SERV_HOST=$SERV_HOST \
        --env container=docker \
        --net=overlay-net \
        $MOUNTS \
        $CAPABILITIES $IMAGE_NAME \
        /bin/bash

    CONTAINER_SHORT_ID=$(docker ps -aqf "name=${NAME}")
    docker exec -it $CONTAINER_SHORT_ID /bin/bash
fi

