Welcome to the OpenDaylight Integration Packaging project.

This project uses a combination of [Packer](https://www.packer.io), [Vagrant](https://www.vagrantup.com), [Docker](https://www.docker.com) and [Ansible](http://www.ansible.com) to create VMs that can be used for testing, developing, learning and teaching on the [OpenDaylight platform](https://www.opendaylight.org).

#Required Tools to Install

Install packer – 

Install Docker – 

Vagrant

#How to Use

Read all the way through this section before attempting any commands.

Clone this project locally, on either a Linux or Mac OS X platform, then:

```bash
cd integration-packaging/packer/
packer build -var-file=packer_vars.json centos.json
```

Note that these instructions *may* be workable on Windows also, but that has not been tested yet.

On Mac OSX, if you want to build the Docker image, you will need to use the "Docker Quickstart Terminal window" as explained in these [Doscker on OSX instructions](http://docs.docker.com/mac/step_one/). If you try to run the `packer` command above in a "normal" terminal shell, the Docker part of the build will fail.



