#!/bin/bash
# this will
# 1) create a pair of veth interfaces
# 2) add one to a physical bridge (assumed to exist)
# 3) add the peer to a docker container netns
# 4) set its IP address

set -e

fn_usage() {
    echo "Usage:"
    echo "connect_container_to_networks.sh <physical host name> <container ID> <container_type>"
    echo
}

fn_get_host_index() {
    # TODO: this will need modification for cperf or other clusters
    local PHYS_HOST_NAME=${1}
    [ -z "$1" ] && echo "ERROR: a host ID number must be supplied" && exit
    local __hix=${PHYS_HOST_NAME##"an11-"} # trim leading rack ID from hostname (e.g. an11-31-odl -> 31-odl-perf)
    local H_IXd=${__hix%%-*} # trim trailing characters after rack position (e.g. 31-odl-perf -> 31)
    H_IXd=${H_IXd##"0"} # trim leading zeroes
    echo "$H_IXd"
}

fn_link_container_netns() {
    echo "INFO: linking net namespace of container $CONTAINER_NAME"
    mkdir -p $HOST_NETNS_ROOT
    # derived variables
    SANDBOX_KEY=$(docker inspect -f '{{.NetworkSettings.SandboxKey}}' $CONTAINER_NAME)
    NETNS_NAME="netns-$CONTAINER_NAME"

    ln -s $SANDBOX_KEY $HOST_NETNS_ROOT/$NETNS_NAME
    ls -al $HOST_NETNS_ROOT
}

fn_attach_veth_to_container() {
    ## Attach veth to container
    CONTAINER_VETH_NAME="ethphys${A_IX}"
    ip link set $VETH_CONT netns $NETNS_NAME
    ip netns exec $NETNS_NAME ip link set dev $VETH_CONT name $CONTAINER_VETH_NAME
    # set the device mac address
    ip netns exec $NETNS_NAME ip link set dev $CONTAINER_VETH_NAME address $CONTAINER_MAC
    # set the adapter IP address
    ip netns exec $NETNS_NAME ip address add $CONTAINER_IP dev $CONTAINER_VETH_NAME
    echo "Container net-namespace contents:"
    ip netns exec $NETNS_NAME ip link set dev $CONTAINER_VETH_NAME up
    ip netns exec $NETNS_NAME ip a s
    echo
}

fn_create_and_link_veth() {
    ## Create veth pair (peers)
    VETH_BASE="ve${H_IXx}${C_IXx}${A_IX}"
    VETH_HOST=${VETH_BASE}h
    VETH_CONT=${VETH_BASE}c
    ip link add $VETH_HOST type veth peer name $VETH_CONT
    ip link set dev $VETH_HOST up
    ## attach veth in host netns to PHYS_BRIDGE
    brctl addif $PHYS_BRIDGE_NAME $VETH_HOST

    fn_attach_veth_to_container
}


fn_display_link_status() {
    # if all goes well, we've linked the container to the bridge, update the counter
    if [ $? -eq 0 ] ; then
        # display status info
        echo "Successfully linked container $CONTAINER_NAME to bridge $PHYS_BRIDGE_NAME"
        echo "H_IX:   ${H_IXd} (0x${H_IXx})"
        echo "C_IX:   ${C_IXd} (0x${C_IXx})"
        echo "C_MAC:  ${CONTAINER_MAC}"
        echo "C_IP4:  ${CONTAINER_IP}"
        echo "C_veth: ${CONTAINER_VETH_NAME} (${VETH_CONT})"
        echo "H_veth: ${VETH_HOST}"
        echo
    fi
}

# main:
# lab constants
MAC_PREFIX="fe:53:00"
HOST_NETNS_ROOT=/var/run/netns
NETMASK_LEN=16

# parse input arguments
PHYS_HOST_NAME="$1"

CONTAINER_ID_NUMBER="${2}"
# container name can be constructed from ID num: compute-<hostID>-<CONTAINER_ID_NUMBER>
CONTAINER_TYPE=${3}

# this is deterministic where each container gets an index which is used
# + to create the IP address, MAC address, VETH numbering, etc
H_IXd=$(fn_get_host_index $PHYS_HOST_NAME  )

# host index (rack position), convert to 2 hex digits
# H_IXx (hex representation of host id) can be passed as an input argument or used from the environment
H_IXx=${H_IXx:-$(printf "%.2x" $H_IXd)}
SUBNET_SEGMENT="${H_IXd}"


# For last octet of IP address:
# host=1, service=2, network=3, compute=11-200, floatingIP=201-254
case "$CONTAINER_TYPE" in
    host)
        echo "Host is already attached to network bridge:"
        exit
        ;;
    service)
        echo "CONTAINER_TYPE = service"
        CONTAINER_NAME=service-node
        CONTAINER_ID_NUMBER=2
        ;;
    network)
        echo "CONTAINER_TYPE = network"
        CONTAINER_NAME=network-node
        CONTAINER_ID_NUMBER=3
        ;;
    measure)
        echo "CONTAINER_TYPE = measure"
        CONTAINER_NAME=measure-node
        CONTAINER_ID_NUMBER=4
        ;;
    compute)  echo "CONTAINER_TYPE = compute"
        CONTAINER_NAME="compute-${H_IXd}-${CONTAINER_ID_NUMBER}"
        echo "Compute node # = $CONTAINER_ID_NUMBER"
        ;;
    *)  echo "ERROR: Invalid CONTAINER_TYPE \"$CONTAINER_TYPE\" specified"
        exit
esac

# description:
# input: container type (string), "ID"  (int, 11-200) supplied on the command line
#   this script will:
# 1) link the container to both br_mgmt and br_data
# 2) modify their MAC addresses accordingly
# 3) supply IP addresse

DEBUG=off
if [[ "$DEBUG" != "on" ]] ; then
    fn_link_container_netns
fi

C_IXd=$CONTAINER_ID_NUMBER
C_IXx=$(printf "%.2x" $C_IXd)

# connect the adapter
for ADAPTER_IX in {1..2}; do
    A_IX="$(printf "%.2x" $ADAPTER_IX)"
    case "$ADAPTER_IX" in
        1)
            # create links to the management bridge
            PHYS_BRIDGE_NAME=br_mgmt
            SUBNET_BASE="10.129"
            ;;
        2)
            # create links to the tenant/data bridge
            PHYS_BRIDGE_NAME=br_data
            SUBNET_BASE="10.130"
            ;;
        *)  echo "ERROR: Invalid ADAPTER_IX \"$ADAPTER_IX\" specified"
            exit
    esac
    SUBNET_PREFIX="${SUBNET_BASE}.${SUBNET_SEGMENT}"
    # container index (container id per host), convert to 2 hex digits
    CONTAINER_IP="${SUBNET_PREFIX}.${C_IXd}/${NETMASK_LEN}"
    CONTAINER_MAC="${MAC_PREFIX}:${H_IXx}:${C_IXx}:${A_IX}"

    # make links
    fn_create_and_link_veth
    fn_display_link_status
done

echo "You can remove the links created just now by simply removing the veth peer from the root netns with:"
echo "    ip link delete $VETH_HOST"

unlink $HOST_NETNS_ROOT/$NETNS_NAME
