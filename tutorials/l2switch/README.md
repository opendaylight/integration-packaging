# Vagrant Tutorial Environment

Vagrant is a tool for managing virtual machines. As compared to binary VM blobs, Vagrant has the
advantage that all configuration is clearly defined in a lightweight Vagrantfile. Feel encouraged to
browse the included L2Switch tutorial Vagrantfile to understand the tutorial environment.

To use Vagrant to stand up the tutorial environment, you'll need to install a virtualization
provider like [VirtualBox][1] or [LibVirt][2], and then [install Vagrant][3].

Once you have Vagrant installed, clone the tutorials:

    git clone https://git.opendaylight.org/gerrit/integration/packaging
    cd packaging/tutorials/l2switch

From the directory with the tutorial Vagrantfile, start the VM and do all provisioning:

    vagrant up

After the VM boots, you can optionally connect via SSH and explore:

    vagrant ssh
    sudo systemctl status opendaylight
    ssh -p 8101 karaf@localhost

You can always destroy the VM and start from a clean slate:

    vagrant destroy -f
    vagrant up

# Accessing the DLUX GUI

All OpenDaylight configuration is handled by the tutorial's Vagrantfile, so after starting
the tutorial VM with `vagrant up` you can access ODL's web GUI, called DLUX.

Open `http://127.0.0.1:8181/index.html` in a browser of your host machine to access DLUX.

Login to DLUX with username `admin` and password `admin`.

![DLUX GUI login page](https://s31.postimg.org/6gdu7vnq3/imageedit_4_7787538837.png)

Note that after starting ODL via `vagrant up`, it may take a few minutes for the DLUX Karaf
features to load and start serving up the GUI.

# Mininet

Mininet is a network testing tool that is often used by network architects to emulate network
topologies and test them virtually before real-world deployment.

## Sample Mininet Topology

By default, the Vagrantfile builds a sample topology consisting of 4 switches, each connected to
a single host.

    sudo mn --mac --topo=linear,4 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13

TODO: Screenshot of this topo

## Custom Mininet Topologies

Let us take a look at a command with basic parameters that builds a customized Mininet network
topology.

    sudo mn --mac --topo=single,3 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13`

The parameters mentioned in the above command are used for the following functions:

* `sudo mn`: Initializes the Mininet console.
* `--mac`: Allocates host MAC addresses equivalent to their IP addresses.
* `--topo`: Tells Mininet to start using the specified topology.
* `--controller`: Specifies that each switch must talk to the controller that is located at a remote location.
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

# OpenDaylight DLUX GUI

The Open**D**ay**l**ight **U**ser **E**xperience (DLUX) project provides a web-based GUI for
OpenDaylight, including the ability to visualize network typologies managed by the L2Switch
project.

As will all OpenDaylight projects, DLUX is installed by loading its Karaf feature. In the tutorial
Vagrantfile, note the line that connects to ODL's Karaf shell and runs:

    feature:install odl-l2switch-switch-ui

This installs DLUX, as well as the Karaf bundles required by L2Switch.

DLUX used ODL's northbound REST API to pull and display information from ODL's MD-SAL database,
which is populated by southbound protocol plugins like OpenFlow.

Let us take a look at the DLUX UI page using a tree topology with depth=2 and fanout=3:

`sudo mn --mac --topo=tree,depth=2,fanout=3 --controller=remote,ip=127.0.0.1 --switch=ovsk,
protocols=OpenFlow13`

![alt text](https://s32.postimg.org/kt33ock8l/imageedit_2_5298056244.png)


[1]: https://www.virtualbox.org/ "Homepage of Oracle's general-purpose virtualization product"
[2]: http://libvirt.org/ "Homepage of libvirt vitualization API"
[3]: https://www.vagrantup.com/ "Homepage of HashiCorp's development environement buildng tool Vagrant"
[4]: http://mininet.org/walkthrough/ "Webpage that offers a walkthrough of all Mininet commands"

