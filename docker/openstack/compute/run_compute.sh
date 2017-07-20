#!/bin/bash
# file: ./run_compute.sh
# info: spawns a docker compute image
# dependencies: consumes proxy variables if defined in the local environment
# + To connect to an OpenStack service node, it must first be running.
# + Compute host image must also be available locally or in a registry.

# image selection
IMAGE_REGISTRY=${IMAGE_REGISTRY:-"odl-registry:4000"}
IMAGE_REPO=${IMAGE_REPO:-s3p/compute}
IMAGE_TAG=${IMAGE_TAG:-v0.5}
IMAGE_NAME="${IMAGE_REGISTRY}/${IMAGE_REPO}:${IMAGE_TAG}"

# image configuration
HOST_ID=${HOST_ID:-99} # HOST_ID represents physical host ID, should be in env
COMP_ID=${COMP_ID:-11} # COMP_ID represents compute node ID, should be in env
DEFAULT_NAME="compute-${HOST_ID}-${COMP_ID}"
NAME=${CONTAINER_NAME:-$DEFAULT_NAME}
CAPABILITIES="--privileged --cap-add ALL --security-opt apparmor=docker-unconfined "
SYSTEMD_ENABLING=" --stop-signal=SIGRTMIN+3 "
CGROUP_MOUNT=" -v /sys/fs/cgroup:/sys/fs/cgroup:ro "
MOUNTS="-v /dev:/dev -v /lib/modules:/lib/modules $CGROUP_MOUNT $SYSTEMD_ENABLING "

# Container environment and OpenStack Config
STACK_USER=${STACK_USER:-stack}
STACK_PASS=${STACK_PASS:-stack}
ODL_NETWORK=${ODL_NETWORK:-True}
SERVICE_HOST=${SERVICE_HOST:-10.129.19.2}
NO_PROXY=localhost,10.0.0.0/8,192.168.0.0/16,172.17.0.0/16,127.0.0.1,127.0.0.0/8,$SERVICE_HOST

# noqa ShellCheckBear
docker run -dit --name ${NAME} --hostname ${NAME} --env TZ=America/Los_Angeles \
    # noqa ShellCheckBear
    --env http_proxy=$http_proxy --env https_proxy=$https_proxy \
    # noqa ShellCheckBear
    --env no_proxy=$NO_PROXY \
    --env ODL_NETWORK=$ODL_NETWORK \
    --env STACK_PASS=$STACK_PASS \
    --env SERVICE_HOST=$SERVICE_HOST \
    --env container=docker \
    $MOUNTS \
    $CAPABILITIES \
    $IMAGE_NAME \
    /sbin/init

# connect containers to host bridges (assumes bridges named br_data and br_mgmt exist on the host
../network/connect_container_to_networks.sh $HOSTNAME $COMP_ID compute

CONTAINER_SHORT_ID=$(docker ps -aqf "name=${NAME}")
AUTO_STACK=no
if [[ "$AUTO_STACK" == "no" ]] ; then
    docker exec -it -u stack $CONTAINER_SHORT_ID /bin/bash
else
    docker exec -d -u stack $CONTAINER_SHORT_ID /bin/bash -c /home/stack/start.sh
fi
