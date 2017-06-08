#!/bin/bash

##############################################################################
# Copyright (c) 2017 Alexis de Talhouët.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

# This is the main script; it basically ensures you have an available OpenDaylight
# distribution to deploy on the nodes, or will download it, and it will
# trigger vagrant or docker to build the cluster.

# shellcheck disable=SC2039
SCRIPTS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT="$( cd "$SCRIPTS" && cd .. && pwd)"

setup_env() {
    # shellcheck disable=SC1090
    . $SCRIPTS/config.properties
    export NUM_OF_NODES=$NUM_OF_NODES
    echo "Cluster will be deployed using $ODL_VERSION."
    echo "The cluster will have $NUM_OF_NODES nodes."
}

dowload_odl() {
    if [ ! -d "$ROOT/opendaylight" ]; then
        echo "Download OpenDaylight distribution"
        mkdir opendaylight
        curl $DISTRO_URL | tar xvz -C opendaylight --strip-components=1
    else
        echo "OpenDaylight distribution $ODL_VERSION already dowloaded."
    fi
}

setup_odl() {
    env_banner
    cd $ROOT/opendaylight || exit

    # for the OSX users, know that BSD-sed doesn't work the same as GNU-sed, hence this command won't work.
    # see http://stackoverflow.com/a/27834828/6937994
    # this command is intended to work with GNU-sed binary
    sed -i "/^featuresBoot[ ]*=/ s/management.*/management,$USER_FEATURES/" etc/org.apache.karaf.features.cfg
    echo "Those features will be installed: $USER_FEATURES"

    # to configure (add/modify/remove) shards that will be
    # spwaned and shared within the cluster, please refer to
    # the custom_shard_config.txt located under /bin
}

spwan_vms() {
    env_banner
    cd $ROOT || exit
    vagrant destroy -f
    vagrant up
}

spwan_containers() {
    env_banner
    # create docker network specific to ODL cluster
    if [ "`docker network ls | grep -w odl-cluster-network | wc -l | xargs echo `" = 0 ]; then
        echo "Docker network for OpenDaylight don't exist - creating ..."
        docker network create -o com.docker.network.bridge.enable_icc=true -o com.docker.network.bridge.enable_ip_masquerade=true --subnet 192.168.50.0/24 --gateway 192.168.50.1  odl-cluster-network
    fi

    # create all the containers
    MAX=$NUM_OF_NODES
    # noqa ShellCheckBear
    for ((i=1; i<=MAX; i++))
    do
        export NODE_NUMBER=$i
        docker rm -f odl-$i
        docker-compose -p odl-$i up -d
    done
}

prerequisites() {
    cat <<EOF
################################################
##              Setup environment             ##
################################################
EOF
    setup_env

    cat <<EOF
################################################
##                 Download ODL               ##
################################################
EOF
    dowload_odl

    cat <<EOF
################################################
##              Configure cluster             ##
################################################
EOF
    setup_odl
}

env_banner() {
cat <<EOF
################################################
##             Spawn cluster nodes            ##
################################################
EOF
}

end_banner() {
cat <<EOF
################################################
##          Your environment is setup         ##
################################################
EOF
}

usage() { echo "Usage: $0 -p <docker|vagrant>" 1>&2; exit 1; }

while getopts ":p:" opt; do
    case $opt in
        p)
            p=$OPTARG
            ;;
        \?)
            echo "Invalid option -$OPTARG" >&2
            usage
            exit 1
            ;;
    esac
done
shift $((OPTIND-1))

if [ -z $p ]; then
    echo "Option -p requires an argument." >&2
    usage
fi

if [ $p = "docker" ]; then
    prerequisites
    spwan_containers
elif [ $p = "vagrant" ]; then
    prerequisites
    spwan_vms
else
    echo "Invalid argument $p for option -p"
    usage
fi

end_banner

