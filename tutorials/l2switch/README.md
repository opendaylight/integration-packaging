# Installing Vagrant

Vagrant is a command line utility tool that is used to create and manage virtual development
environments. To begin the L2Switch Tutorial, you can either install VirtualBox[1] or LibVirt[2].
Along with these, you must also install Vagrant[3].

After importing the Vagrantfile, you can build and configure the virtual machine:

`vagrant  up`

To SSH into the virtual machine:

`vagrant  ssh`

# Logging into the OpenDaylight Controller

* You can access the OpenDaylight controller through SSH.

`ssh  -p  8101  karaf@localhost`

Password: karaf

The above operation need not be performed manually since it has been provisioned within the
Vagrantfile. Open `http://127.0.0.1:8181/index.html` on the browser of your host machine to access
the DLUX Web GUI.

Login to the web GUI of OpenDaylight.

Username: admin
Password: admin

The time taken to gain access into the DLUX web user interface depends on the hardware capability of
your machine. It usually takes about a minute or even less than that to install the Karaf features.

# Mininet

Mininet is a network testing tool that is often used by network architects to emulate network
topologies and test them virtually before real-world deployment.

## Sample Mininet Topology

The Vagrantfile has been provisioned to build a sample topology consisting of 4 switches, each of
which is connected to a single host.

`sudo mn  --mac  --topo=linear,4  --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13`

## Building Topologies on Mininet

Let us take a look at a command with basic parameters that builds a customized Mininet network
topology.

`sudo  mn  --mac  --topo=single,3  --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13`

The parameters mentioned in the above command are used for the following functions:

* sudo mn: 	Initializes the Mininet console.

* --mac: 		Allocates host MAC addresses equivalent to their respective IP addresses.

* --topo: 		Initializes the topology.

* --controller: 	Initializes the remote controller.

* --switch: 	Initializes the OpenVSwitch.

* protocols: Defines the protocol version for the switch to use.

## Generating Traffic on Mininet

Ping command can be used to generate traffic between hosts.

`mininet>   h1  ping  h2`

For each host to be able to ping every other host in the network, use the following command:

`mininet>   pingall`

After playing around with the default topology and the tutorial, you can create complex topologies
and perform advanced tasks[4].


[1]: https://www.virtualbox.org/
[2]: http://libvirt.org/
[3]: https://www.vagrantup.com/
[4]: http://mininet.org/walkthrough/
