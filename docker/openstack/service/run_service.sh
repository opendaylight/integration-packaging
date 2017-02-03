#!/bin/bash
# file: run_service.sh
# info: spawns a docker service image
# dependencies: assumes proxy variables are defined in the local environment

# image selection
IMAGE_REPO="s3p/service"
IMAGE_VERSION="v0.1"
IMAGE_NAME="${IMAGE_REPO}:${IMAGE_VERSION}"

# image configuration
ODL_NETWORK=false
CAPABILITIES="--privileged --cap-add ALL --cap-add NET_ADMIN --cap-add NET_RAW"
SERV_HOST=172.17.0.4
STACK_PASS=stack
# define _no_proxy based on the cluster topology
_no_proxy=localhost,10.0.0.0/8,192.168.0.0/16,172.17.0.0/16,127.0.0.0/8

CONF_FILE="$(pwd)/service.odl.local.conf"
if [ "$ODL_NETWORK" = "false" ] ; then
#    CONF_FILE="$(pwd)/service.neutron.local.conf"
    echo "Using no-ODL (Neutron) local.conf ($CONF_FILE}"
    NAME=service-node-neutron
else
    echo "Using OpenDaylight for local.conf ($CONF_FILE})"
    NAME=service-node-odl
fi
if [ -n "$1" ] ; then
    # if a command is specified as an argument to the script, use it,
    # else, default to the CMD defined in the Dockerfile
    echo "Command argument supplied, running \"$1\" in $NAME..."
    COMMAND="$1"
fi

echo "Starting up docker container from image ${IMAGE_NAME}"
echo "name: $NAME"
docker run -it --name ${NAME} --hostname ${NAME} --env TZ=America/Los_Angeles \
    --env JAVA_HOME=/usr/lib/jvm/java-8-oracle --env JAVA_MAX_MEM=16g \
    --env http_proxy=$http_proxy --env https_proxy=$https_proxy \
    --env no_proxy=$_no_proxy \
    --env ODL_NETWORK=$ODL_NETWORK \
    --env STACK_PASS=$STACK_PASS \
    -v /dev:/dev -v /lib/modules:/lib/modules \
    -v $(pwd)/logs:/opt/stack/logs \
    $CAPABILITIES \
    $IMAGE_NAME \
    $COMMAND

