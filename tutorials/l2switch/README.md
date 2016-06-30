<center><h1> Installing Vagrant</h1> </center>

Vagrant is a command line utility tool that is used to create and manage virtual development
environments.

To begin the L2Switch Tutorial, install [VirtualBox](https://www.virtualbox.org)  and
[Vagrant](http://www.vagrantup.com).

After importing the Vagrantfile, you can build and configure the Virtual Machine:

`vagrant  up`

To SSH into the Virtual Machine:

`vagrant  ssh`

<center><h1> Logging into the OpenDaylight Controller</h1> </center>

There are two different ways of logging into the OpenDaylight Controller:

* The first method requires that you move into the OpenDaylight working directory and executing the
./bin/karaf to start the controller.

`cd   /opt/opendaylight`

* You can also SSH into the Karaf console to start the OpenDaylight controller.

`sudo  ssh  -p  8101  karaf@localhost`

Password: karaf

The above operation need not be performed manually since it has been provisioned within the Vagrant
file. Open "http://127.0.0.1:8181/index.html" on the browser of your host machine to access the
DLUX Web GUI.

Login to the web GUI of OpenDaylight.

Username: admin
Password: admin

The time taken to gain access into the DLUX web user interface depends on the hardware capability
of your machine. It usually takes about a minute or even less than that to gain access into the DLUX
Web GUI.

<h1> <center>Mininet</h1> </center>

Mininet is a network testing tool that is often used by network architects to emulate network
topologies and test them virtually before real-world deployment.

## Sample Mininet Topology

The Vagrantfile has been provisioned to build a sample topology consisting of 4 switches, each of
which is connected to a single host.

`sudo mn  --mac  --topo=linear,4  --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13`

## Building Topologies on Mininet

Not defining any parameters builds a default topology with 1 switch connected to 2 hosts.

`sudo mn`

You can build several complex topologies using [Mininet](http://mininet.org/walkthrough/).
Let us take a look at a command with basic parameters that builds a customized Mininet network
topology.

`sudo  mn  --mac  --topo=single,3  --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13`

The parameters mentioned in the above command are used for the following functions:

* sudo mn: Initializes the Mininet console.

* --mac: Allocates host MAC addresses equivalent to their respective IP addresses.

* --topo: Initializes the topology.

* --controller: Initializes the remote controller.

* --switch: Initializes the OpenVSwitch.

* protocols: Defines the protocol version for the switch to use.

## Generating Traffic on Mininet

Ping command can be used to generate traffic between hosts.

`mininet>   h1  ping  h2`

For each host to be able to ping every other host in the network, use the following command:

`mininet>   pingall`

