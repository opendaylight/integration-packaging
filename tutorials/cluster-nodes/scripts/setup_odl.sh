#!/bin/bash

##############################################################################
# Copyright (c) 2017 Alexis de Talhouët.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

# That script provisions the nodes by installing JDK-8. It installs the OpenDaylight distribution
# under `$HOME/OpenDaylight`. It also configure the Shards of the OpenDaylight instance:
# Shard configuration:
# see (configure-cluster-ipdetect.sh)[https://github.com/opendaylight/integration-distribution/blob/release/boron-sr2/distribution-karaf/src/main/assembly/bin/configure-cluster-ipdetect.sh]

# shellcheck disable=SC2039
SCRIPTS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# shellcheck disable=SC1090
. $SCRIPTS/config.properties

install_packages() {
    # required if using Docker, else could be commented-out
    sudo apt-get update -y
    sudo apt-get -y install software-properties-common
    #install java8
    echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections
    sudo add-apt-repository ppa:webupd8team/java -y
    sudo apt-get update
    sudo apt-get install oracle-java8-installer -y
    sudo update-java-alternatives -s java-8-oracle
    sudo apt-get install oracle-java8-set-default -y
    export JAVA_HOME=/usr/lib/jvm/java-8-oracle
}

start_odl() {
    cd $HOME/opendaylight || exit

    seed_nodes=""
    for i in $(seq $NUM_OF_NODES)
    do
        seed_nodes+="192.168.50.15$i "
    done

    # setup the cluster with all the nodes' IP address
    ./bin/configure-cluster-ipdetect.sh $seed_nodes

    rm -rf journal snapshots
    JAVA_MAX_MEM=4G JAVA_MAX_PERM_MEM=512m bin/karaf clean
}

echo "Install required packages" > $HOME/setup.prog
install_packages

echo "Starting OpenDaylight" > $HOME/setup.prog
start_odl

# For the docker container, we have to let the container
# live else it will stop once the setup is ready
# noqa ShellCheckBear
while [ 1 ];
do
  sleep 10
done
