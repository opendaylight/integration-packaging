#!/bin/bash
# file: ./run_compute.sh
# info: spawns a docker compute image
# dependencies: consumes proxy variables if defined in the local environment
# + To connect to an OpenStack service node, it must first be running.
# + Compute host image must also be available locally or in a registry.

# image selection
IMAGE_REPO="s3p/compute"
IMAGE_VERSION="v0.2" # v0.2==Ubuntu 14.04
IMAGE_NAME="${IMAGE_REPO}:${IMAGE_VERSION}"

# image configuration
HOST_ID=01
COMP_ID=04
NAME="compute-${HOST_ID}-${COMP_ID}"
ODL_NETWORK=false
# when running on a RHEL-derivative host, use "--security-opt seccomp=unconfined"
CAPABILITIES="--privileged --cap-add ALL --security-opt apparmor=docker-unconfined "
CGROUP_MOUNT=""
MOUNTS="-v /dev:/dev -v /lib/modules:/lib/modules $CGROUP_MOUNT "
STACK_PASS=${STACK_PASS:-stack}
# default SERVICE_HOST, based on openstack. This may be overridden.
SERV_HOST=${SERV_HOST:-10.20.0.2}
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
    echo "WARNING: no service node is available on overlay-net."
    echo "You can launch the compute container, but it may not be able to connect to a service node."
fi
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

