Installing Vagrant
------------------

Vagrant is a command line utility tool that is used to create and manage virtual development environments or VDE, as they are commonly referred to.
Vagrant aids in building VDE’s with the help of basic configurations that allow a user to create, manage and deploy a wide range of development environments.

Steps required to install Vagrant.

Step 1. Open the terminal on your machine.

Step 2. Install VirtualBox. Type in the following command.

						sudo dnf install virtualbox

For Ubuntu OS,

						sudo apt-get install virtualbox


Step 3. Install Vagrant using this command.
	
						sudo dnf install vagrant
				

For Ubuntu OS,

						sudo apt-get install vagrant
						
Step 4. To make sure you have successfully installed Vagrant on your machine, just run the following command to return the current version of Vagrant that is installed on your machine.

						vagrant   -v

Step 5.  Step 4 should return the current version of Vagrant installed on your machine. If the version is displayed, it indicates that Vagrant has been successfully installed on your machine.


Running the Vagrant Box
------------------------
	
Download the vagrant box using the command:

					vagrant  init  -m  ‘f23_rpm_be_sr2’

Once the box had been downloaded, you can get a look at the vagrant file by performing a ‘cat’ operation on the file named ‘Vagrantfile’.

						cat Vagrantfile

To create and compile the configurations put forth by the Vagrantfile, we make use of the ‘vagrant up’ command. Once the configuration has been compiled, use the ‘vagrant ssh’ command to ssh into the new vagrant build environment.


Setting Up the OpenDaylight Controller
--------------------------------------

There are two different ways of setting up the OpenDaylight Controller:

 1.The first method requires that you move into the OpenDaylight working directory from your terminal and run the ./bin/karaf in order to run the controller.

The OpenDaylight Working Directory:   cd   /opt/opendaylight

 2.This is the SSH method. You can ssh into the Karaf console with the help of the following command:

					sudo  ssh  -p  8101  karaf@localhost

The password being:  karaf

You will now be within the OpenDaylight controller console wherein you need to install the required features.

IMPORTANT: All features MUST be installed in the right order for the controller to function properly.

Install the required features:

		>feature:install odl-restconf odl-l2switch-switch-ui odl-openflowplugin-all odl-mdsal-apidocs 

Once the required features have been installed, the next step is to open http://<Controller Ip>:8181/index.html. 

The OpenDaylight user interface page will be displayed. Enter the following credentials to login to the web GUI of OpenDaylight:

Username: admin

Password: admin  	

The time taken to gain access into the DLUX web user interface depends on the hardware capability of your machine.


Mininet
------- 

Mininet is a network testing tool that is often used by network architects to create network topologies and test them virtually before real-world deployment. Mininet functions as a network emulator that aids  in building network topologies involving network entities like hosts, switches, links and controllers.

Working with Mininet

To be able to initialize mininet on your machine, type in the command   ‘sudo  mn’. This will initialize mininet with a default topology consisting of 1 switch and 2 hosts. This topology is referred to as the minimal topology.

Always prior to building mininet topologies, we need to make sure that there are no existing remnants of previous topologies. To clear a previous topology, we use the following command:

						sudo  mn  -c

Building Topologies on Mininet

Let us take a look at a sample mininet topology building command.

	sudo  mn  --mac  --topo=single,3  --controller=remote,ip=127.0.0.1  --switch=ovsk

sudo mn - Initializes the mininet console
--mac – To allocate easily understandable MAC addresses to hosts.
--topo – To initialize the topology (In this case, it is a single switch topology with 1 switch and 3 hosts).
--controller – To initialize the remote controller (In this case, the remote controller is allocated an IP address of 127.0.0.1).
--switch – To initialize the switch (In this case, an OpenvSwitch).


The L2Switch 
------------

The Layer 2 Switch is a networking entity that provides Layer 2 switching functionality. An essential parameter for the working of a Layer 2 Switch is the MAC address. Since MAC addresses correspond to the 2nd layer of the 7-Layer OSI model, we reference to this switch as a Layer 2 Switch.

Initialize the Topology on Mininet

Let us now build our mininet topology. We shall be using the linear topology wherein all the switches are connected in a line and each switch is connected to a host.

	sudo mn  --mac  --topo=linear,4  --controller=remote,ip=127.0.0.1 --switch=ovsk,protocols=OpenFlow13

The ‘protocols=OpenFlow13’ in the above command specifies the fact that the OpenVSwitch shall operate with version 1.3 of the OpenFlow protocol.

Generating Traffic on Mininet

As discussed earlier, the primary function of mininet is to act as a testing utility, prior to deploying the network in a real world environment.

Trying to establish pings between hosts can be the most useful way of generating traffic between them.

To allow host h1 to ping host h2, we use the following command:

							h1  ping  h2

To facilitate pings between each and every host connected in the network, we use the following command:

							pingall



