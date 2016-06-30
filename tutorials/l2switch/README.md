# Vagrant Tutorial Environment

Vagrant is a tool for managing virtual machines. As compare to binary VM blobs, Vagrant has the
advantage that all configuration is clearly defined in a lightweight Vagrantfile. Feel encouraged to
browse the included L2Switch tutorial Vagrantfile to understand the tutorial environment.

To use Vagrant to stand up the tutorial environment, you'll need to install a virtualization
provider like [VirtualBox][1] or [LibVirt][2], and then [install Vagrant][3].

TODO: Docs about cloning the repo and getting to Vagrantfile

To start the tutorial VM and do all provisioning:

    vagrant up

If you'd like to connect to the VM and explore, SSH into it via:

    vagrant ssh

TODO: Docs about `vagrant destroy` and `vagarnt provision`

# Accessing the DLUX GUI

All OpenDaylight configuration is handled by the tutorial's Vagrantfile, so after starting
the tutorial VM with `vagrant up` you can access ODL's web GUI, called DLUX.

Open `http://127.0.0.1:8181/index.html` on the browser of your host machine to access DLUX.

Login to DLUX with username `admin` and password `admin`.

TODO: Picture

Note that after starting ODL via `vagrant up`, it may take a few minutes for the DLUX Karaf
features to load and start serving up the GUI.

# Mininet

Mininet is a network testing tool that is often used by network architects to emulate network
topologies and test them virtually before real-world deployment.

## Sample Mininet Topology

By default, the Vagrantfile builds a sample topology consisting of 4 switches, each connected to
a single host.

    sudo mn --mac --topo=linear,4 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13

## Custom Mininet Typologies

Let us take a look at a command with basic parameters that builds a customized Mininet network
topology.

    sudo mn --mac --topo=single,3 --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13`

The parameters mentioned in the above command are used for the following functions:

* `sudo mn`: Initializes the Mininet console.
* `--mac`: Allocates host MAC addresses equivalent(TODO??) to their respective IP addresses.
* `--topo`: Initializes the topology. TODO: Not so helpful/true
* `--controller`: Initializes the remote controller. TODO: Not so helpful/true
* `--switch`: Initializes the OpenVSwitch. TODO: Not so helpful
* `protocols`: Defines the protocol version for the switch to use.

## Generating Traffic on Mininet

Ping command can be used to generate traffic between hosts.

TODO: where do they get this mininet shell?

    mininet> h1 ping h2

For each host to be able to ping every other host in the network, use the following command:

    mininet> pingall

After playing around with the default topology and the tutorial, you can create complex topologies
and perform [advanced tasks][4]. TODO: Examples of advanced tasks? Move to Mininet Topos section?


[1]: https://www.virtualbox.org/ "TODO text description of all links here"
[2]: http://libvirt.org/
[3]: https://www.vagrantup.com/
[4]: http://mininet.org/walkthrough/
