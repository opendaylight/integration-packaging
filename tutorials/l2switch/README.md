# Vagrant Tutorial Environment

Vagrant is a tool for managing virtual machines. As compared to binary VM blobs, Vagrant has the
advantage that all configuration is clearly defined in a lightweight Vagrantfile. Feel encouraged to
browse the included L2Switch tutorial Vagrantfile to understand the tutorial environment.

To use Vagrant to stand up the tutorial environment, you'll need to install a virtualization
provider like [VirtualBox][1] or [LibVirt][2], and then [install Vagrant][3].

The following command is used to clone the repository.

`git clone https://git.opendaylight.org/gerrit/integration/packaging`

To start the tutorial VM and do all provisioning:

    vagrant up

If you'd like to connect to the VM and explore, SSH into it via:

    vagrant ssh

Modifications to the provisioning scripts can be checked by:

    vagrant provision

To stop a running Vagrant machine and destroy created machine resources:

    vagrant destroy

# Accessing the DLUX GUI

All OpenDaylight configuration is handled by the tutorial's Vagrantfile, so after starting
the tutorial VM with `vagrant up` you can access ODL's web GUI, called DLUX.

Open `http://127.0.0.1:8181/index.html` on the browser of your host machine to access DLUX.

Login to DLUX with username `admin` and password `admin`.

![alt text](https://s31.postimg.org/6gdu7vnq3/imageedit_4_7787538837.png)

Note that after starting ODL via `vagrant up`, it may take a few minutes for the DLUX Karaf
features to load and start serving up the GUI.

# Mininet

Mininet is a network testing tool that is often used by network architects to emulate network
topologies and test them virtually before real-world deployment.

## Sample Mininet Topology

By default, the Vagrantfile builds a sample topology consisting of 4 switches, each connected to
a single host.

    sudo mn --mac --topo=linear,4 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13

## Custom Mininet Topologies

Let us take a look at a command with basic parameters that builds a customized Mininet network
topology.

    sudo mn --mac --topo=single,3 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13`

The parameters mentioned in the above command are used for the following functions:

* `sudo mn`: Initializes the Mininet console.
* `--mac`: Allocates host MAC addresses equivalent to their IP addresses.
* `--topo`: Tells Mininet to start using the specified topology.
* `--controller`: Specifies that each switch must talk to the controller that is located at a remote
location.
* `--switch`: Tells Mininet that the switches are of type OVSK.
* `protocols`: Defines the protocol version for the switch to use.

Mininet supports the creation of Single, linear, Tree and 2-D Torus topologies.

## Generating Traffic on Mininet

Ping command can be used to generate traffic between hosts.

TODO: where do they get this mininet shell? (We are still working to get this part of the code running)

    mininet> h1 ping h2

For each host to be able to ping every other host in the network, use the following command:

    mininet> pingall

After playing around with the default topology and the tutorial, you can create complex topologies
and perform [advanced tasks][4].


# The OpenDaylight DLUX Web User Interface

The OpenDaylight controller makes use of the OpenDaylight User Experience (DLUX) application in the
implementation of its user interface. DLUX is an openflow network management application for the 
OpenDaylight controller.

The GUI of OpenDaylight displays information about the topology of the network, flow statistics and
host locations. The GUI draws information from the topology and the host databases to display the
above mentioned information. The DLUX Karaf feature has to be enabled so as to integrate the GUI with
OpenDaylight. Each feature within Karaf can be separately enabled or disabled.

Topology information cannot be added using the DLUX UI. Topology information is collected by
OpenDaylight's southbound plugins and stored in the MD-SAL (Model Driven Service Abstraction Layer).
Northbound applications like DLUX are provided access to this information.

Let us take a look at the DLUX UI page using a Tree topology with depth=2 and fanout=3:

`sudo mn --mac --topo=tree,depth=2,fanout=3 --controller=remote,ip=127.0.0.1 --switch=ovsk,
protocols=OpenFlow13`

![alt text](https://s32.postimg.org/kt33ock8l/imageedit_2_5298056244.png)


[1]: https://www.virtualbox.org/ "Homepage of Oracle's general-purpose virtualization product"
[2]: http://libvirt.org/ "Homepage of libvirt vitualization API"
[3]: https://www.vagrantup.com/ "Homepage of HashiCorp's development environement buildng tool Vagrant"
[4]: http://mininet.org/walkthrough/ "Webpage that offers a walkthrough of all Mininet commands"
