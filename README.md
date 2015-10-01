Welcome to the OpenDaylight Integration Packaging project.

This project uses a combination of [Packer][1], [Vagrant][2], [Docker][3], [Virtual Box][4] and [Ansible][5] to create VMs that can be used for testing, developing, learning and teaching on the [OpenDaylight platform][6].

#About the Tools Being Used

Before you can use this project to build a VM, you need to install the tools listed below.

##Virtual Box

[Docker][3], when running on Mac OSX, installs [Virtual Box][4] when it is installed. Why that is explained in the Docker Mac OSX [install instructions][11], but the essence of it is that Docker needs a Linux environment within which to run the Docker daemon.

TODO: Test what happen on Linux.

##Packer

Packer is used to drive the overall VM build process. The Packer installation instructions are [here][7].

##Docker

[Docker][3] is invoked by [Packer][1] to create a Docker image. The Docker installation instructions are [here][8].

Note, on Mac OSX you need to use the "Docker Quickstart Terminal window" to run the build.

##Vagrant

[Packer][1] will create a [Vagrant][2] box as one of the build targets. You will need to have Vagrant installed to be able to use that box. The Vagrant installation instructions are [here][9].

#How to Use

Read all the way through this section before attempting any commands.

Clone this project locally, on either a Linux or Mac OS X platform, then (assuming your git directory is in your home directory):

```bash
cd ~/git/integration-packaging/packer/
packer build -var-file=packer_vars.json centos.json
```

The details of what is happening in the Packer build are explained [here][packer/README.md]

Note that these instructions *may* be workable on Windows also, but that has not been tested yet.

On Mac OSX, if you want to build the Docker image, you will need to use the "Docker Quickstart Terminal window" as explained in these [Doscker on OSX instructions](http://docs.docker.com/mac/step_one/). If you try to run the `packer` command above in a "normal" terminal shell, the Docker part of the build will fail. At the time of writing, on Mac OSX though, the build running in the Docker terminal fails to terminate, whereas a build run in a "normal" OSX terminal does build the Vagrant box.

[1]: https://www.packer.io
[2]: https://www.vagrantup.com
[3]: https://www.docker.com
[4]: https://www.virtualbox.org
[5]: http://www.ansible.com
[6]: https://www.opendaylight.org
[7]: https://www.packer.io/intro/getting-started/setup.html
[8]: https://docs.docker.com/installation/
[9]: https://docs.vagrantup.com/v2/installation/
[10]: https://www.virtualbox.org/wiki/Downloads
[11]: https://docs.docker.com/installation/mac/