#!/bin/bash

# Options:
#   -x: Echo commands
#   -e: Fail on errors
#   -o pipefail: Fail on errors in scripts this calls, give stacktrace
set -ex -o pipefail

ODL_IP="10.0.0.2"

cid=$(docker run -idt --cap-add NET_ADMIN vpickard/openvswitch:2.5.0)
sleep 2
docker exec $cid ovs-vsctl set-manager tcp:$ODL_IP:6640
sleep 2
docker exec $cid ovs-vsctl show
