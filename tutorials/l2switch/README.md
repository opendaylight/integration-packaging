# Vagrant Tutorial Environment

Vagrant is a tool for managing virtual machines. As compared to binary VM blobs, Vagrant has the
advantage that all configuration is clearly defined in a lightweight Vagrantfile. Feel encouraged to
browse the included L2Switch tutorial Vagrantfile to understand the tutorial environment.

To use Vagrant to stand up the tutorial environment, you'll need to install a virtualization
provider like [VirtualBox][1] or [LibVirt][2], and then [install Vagrant][3].

Once you have Vagrant installed, clone the tutorials:

```
git clone https://git.opendaylight.org/gerrit/integration/packaging
cd packaging/tutorials/l2switch
```

From the directory with the tutorial Vagrantfile, start the VM and do all provisioning:

```
vagrant up
```

After the VM boots, you can optionally connect via SSH and explore:

```
vagrant ssh
sudo dnf info opendaylight
sudo systemctl status opendaylight
ssh -p 8101 karaf@localhost
```

You can always destroy the VM and start again:

```
vagrant destroy -f
vagrant up
```

# Accessing the DLUX GUI

All OpenDaylight configuration is handled by the tutorial's Vagrantfile, so after starting
the tutorial VM with `vagrant up` you can access ODL's web GUI, called DLUX.

Open `http://127.0.0.1:8181/index.html` in a browser on your host machine to access DLUX.

Login to DLUX with username `admin` and password `admin`.

![DLUX GUI login page][4]

Note that after starting ODL via `vagrant up`, it may take a few minutes for the DLUX Karaf
features to load and start serving up the GUI.

# Mininet

Mininet is a network testing tool that is often used by network architects to emulate network
topologies and test them virtually before real-world deployment.

## Sample Mininet Topology

By default, the Vagrantfile builds a sample topology consisting of 4 switches, each connected to
a single host.

```
sudo mn --mac --topo=linear,4 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13
```

![Linear Topology][5]

## Custom Mininet Topologies

Mininet supports the creation of Single, Tree and 2-D Torus topologies.

Let us take a look at some examples of mininet topologies built using basic mininet topology commands:

- Single Topology

A single topology consists of a single switch connected to a number of hosts as specified in the
topology build command. Here, we are using a single topology with 3 hosts connected to the switch.

```
sudo mn --mac --topo=single,3 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13
```

![Single Topology][6]

- Tree Topology

Let us take a look at the DLUX UI page using a tree topology with depth=2 and fanout=3. In a tree
topology, a fanout value corresponds to the number of switches the central switch gets connected to.
The fanout value also determines the number of hosts that get connected to every other edge switch.
The depth parameter allows the edge switches to further branch out with the same fanout value
as specified.

```
sudo mn --mac --topo=tree,depth=2,fanout=3 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13
```

![Tree Topology][7]

- Torus Topology

The Torus topology is a network topology used for connecting nodes in a parallel computer system.
This topology is used in supercomputers to decrease communication latency. The additional ‘3’ settings
in the Torus topology syntax refer to the size of the topology namely the size of the rectilinear
array with 3, 3 analogous to 3 rows and 3 columns.

```
sudo mn --mac --topo=torus,3,3 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13
```

![Torus Topology][8]

The parameters mentioned in the above commands are used for the following functions:

- `sudo mn`: Initializes the Mininet console.
- `--mac`: Allocates host MAC addresses equivalent to their IP addresses.
- `--topo`: Tells Mininet to start using the specified topology.
- `--controller`: Specifies that each switch must talk to the controller that is located at a remote location.
- `--switch`: Tells Mininet that the switches are of type OVSK.
- `protocols`: Defines the protocol version for the switch to use.

## Basic Mininet CLI Operations

One you build the topology, you will gain access into the Mininet CLI.

To Display Mininet CLI commands:

```
mininet> help
```

To Display all elements in the network:

```
mininet> nodes
```

To Display a list of links:

```
mininet> net
```

To dump information about all nodes:

```
mininet> dump
```

# OpenDaylight DLUX GUI

The Open**D**ay**l**ight **U**ser **E**xperience (DLUX) project provides a web-based GUI for
OpenDaylight, including the ability to visualize network typologies managed by the L2Switch
project.

As with all OpenDaylight projects, DLUX is installed by loading its Karaf feature. In the tutorial
Vagrantfile, note the line that connects to ODL's Karaf shell and runs:

```
feature:install odl-l2switch-switch-ui
```

This installs DLUX, as well as the Karaf bundles required by L2Switch.

DLUX uses ODL's northbound REST API to pull and display information from ODL's MD-SAL database,
which is populated by southbound protocol plugins like OpenFlow.

[1]: https://www.virtualbox.org/wiki/Downloads "VirtualBox downloads page"

[2]: https://github.com/vagrant-libvirt/vagrant-libvirt "Vagrant LibVirt plugin GitHub"

[3]: https://www.vagrantup.com/downloads.html "Vagrant downloads page"

[4]: https://s31.postimg.org/6gdu7vnq3/imageedit_4_7787538837.png "ODL DLUX GUI login page screenshot"

[5]: https://s32.postimg.org/jlw4hphzp/imageedit_2_3952319201.png "ODL DLUX GUI showing Mininet linear topo"

[6]: https://s32.postimg.org/w1subgbbp/imageedit_4_2391309779.png "ODL DLUX GUI showing Mininet single topo"

[7]: https://s32.postimg.org/kt33ock8l/imageedit_2_5298056244.png "ODL DLUX GUI showing Mininet tree topo"

[8]: https://s32.postimg.org/bvpcckfo5/imageedit_6_6305541411.png "ODL DLUX GUI showing Mininet torus topo"
