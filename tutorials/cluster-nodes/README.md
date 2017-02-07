# Deploy an OpenDaylight Cluster
This repo provide a Vagrant file and a docker-compose.yml file so one can deploy an OpenDaylight cluster using VMs or containers.
## Configuration
The VMs / Containers are configured through the _config.properties_ file.
### config.properties
* How many nodes to deploy? 
    Default is `3`.
* What OpenDaylight release to use?
    Default is `Boron-SR2`.
* What features to install on startup? 
    Default are `odl-jolokia, odl-restconf, odl-mdsal-clustering`.

### Vagrant
Virtual Machines are configured as follow:
* Image: Trusty
* RAM: 4096
* CPUs: 4
* Network: 
    * Bridge "en0: Wi-Fi (AirPort)"
    * Static IP address: 192.168.50.15#{node_index}

To change the network configuration edit the Vagrantfile.

Useful commands:
```
# from the root folder containing the Vagranfile access the virtual machine
vagrant ssh odl-1

# if you can't access odl-2 or odl-3, export the configured number of nodes and retry
export NUM_OF_NODES=3

# destroy VMs (force)
vagrant destroy -f

```
### Docker
Containers are configured as follow:
* Image: Trusty
* Network: 
    * Static IP address: 192.168.50.15#{node_index}

A specific network is created to hold the cluster networking into its own subnet. Run the following command to see how it's configured:
```
docker network inspect odl-cluster-network
```

* name: odl-cluster-network
* com.docker.network.bridge.enable_icc=true
* com.docker.network.bridge.enable_ip_masquerade=true
* subnet 192.168.50.0/24
* gateway 192.168.50.1


To see where the setup is at, run the command bellow. If the OpenDaylight CLI is shown, it means the node is ready.
```
docker exec odl-1 tail -f nohup.out
```

Useful commands:
```
# list all running containers
docker ps

# remove all containers
docker rm -f $(docker ps -q)

# delete odl-cluster-network
docker network rm odl-cluster-network

# execute a command in a container
docker exec <container_id|container_name> <command>

# list odl image
docker images odl-node

# remove odl image
docker rmi odl-node

```
# Usage
Execute the `setup_cluster.sh` script, and all should be ready within the next half hour, depending on your network.

```
./scripts/setup_cluster.sh -p <docker|vagrant>
```
## Example
To create a cluster using containers, run the following:
```
./scripts/setup_cluster.sh -p docker
```
# Resources
A Postman collection is provided giving useful requests to ensure the cluster is correctly setup, and to gather info from it through Jolokia.
This Postman collection also provides requests to manage the cluster, leveraging the [cluster-admin.yang](https://github.com/opendaylight/controller/blob/master/opendaylight/md-sal/sal-cluster-admin-api/src/main/yang/cluster-admin.yang) RPCs.