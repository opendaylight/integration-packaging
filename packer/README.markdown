# OpenDaylight Packer

[Packer][1] is a tool for automatically creating VM and container images,
configuring them and post-processing them into standard output formats.

We build OpenDaylight's Vagrant base boxes and Docker images via Packer.

## Building

You'll need to [install Packer][2], of course.

OpenDaylight's Packer configuration is divided into build-specific variables,
output-specific templates and a set of shared provisioning scripts. To do a
specific build, combine the template for the desired output artifact type with
a variable file. For example, to build a LibVirt-based Vagrant base box with
ODL Beryllium and CentOS 7.2.1511:

```
packer build -var-file=vars/opendaylight-4.0.0.json -var-file=vars/centos-7.2.1511.json templates/libvirt.json
```

To build the same box with VirtualBox as the virtualization provider:

```
packer build -var-file=vars/opendaylight-4.0.0.json -var-file=vars/centos-7.2.1511.json templates/virtualbox.json
```

To build a Beryllium SR1 Docker container:

```
packer build -var-file=vars/opendaylight-4.1.0.json -var-file=vars/centos-7.2.1511.json templates/docker.json
```

Note that LibVirt, VirtualBox and Docker will need to work on your local system
to run Packer builds that use them. You may need to disable LibVirt/VBox when
enabling the other.

From a high level, the builds:

- Download and verify the CentOS ISO specified in the variables file.
- Boot the ISO and do low-level configuration via a Kickstart template.
- Run a set of shell scripts, listed in the template's shell provisioner
  section, to do any configuration required by the builder (VBox, Docker),
  other provisioners (Ansible) or post-processors (Vagrant, Docker).
- Install and configure the version of OpenDaylight specified in the variables
  file using the [ansible-opendaylight role][3].
- Export, compress and package the VM as a Vagrant base box or Docker image.

## Running

This section documents how to run OpenDaylight's Vagrant base boxes and Docker
images.

### Pre-Built

This section documents how to run OpenDaylight Vagrant base boxes and Docker
images. That have been built by the Integration/Packaging project and pushed
to hosting services for easy consumption.

#### Vagrant Base Boxes

OpenDaylight uses the official Atlas Vagrant base box hosting service.

The [opendaylight/odl][4] repository contains built versions of every box
defined here.

To use the latest version, simply specify `opendaylight/odl` as the base
box in your Vagrantfile.

```
$ vagrant init -m opendaylight/odl
$ cat Vagrantfile
Vagrant.configure(2) do |config|
  config.vm.box = "opendaylight/odl"
end
```

Boot the box (will download from Atlas if not cached locally) and connect:

```
$ vagrant up
$ vagrant ssh
```

OpenDaylight will already be installed and running:

```
$ sudo systemctl is-active opendaylight
active
```

To connect to the Karaf shell:

```
$ ssh -p 8101 karaf@localhost
# password: karaf
```

To use a version other than latest, specify it in your Vagrantfile.

```
Vagrant.configure(2) do |config|
  config.vm.box = "opendaylight/odl"
  config.vm.box_version = "= 3.4.0"
end
```

#### Docker Images

Up-to-date Docker images can be pulled from [OpenDaylight's DockerHub][5].

Download the latest image and start a container with ODL running:

```
$ docker run -ti opendaylight/odl /opt/opendaylight/bin/karaf
```

To run a specific version, include a tag:

```
$ docker run -ti opendaylight/odl:4.1.0 /opt/opendaylight/bin/karaf
```

### Locally Built

This section documents how to run locally-built OpenDaylight Vagrant base boxes
and Docker images. Users not interested in building their own artifacts should
see the Pre-Built section above.

#### Vagrant Base Boxes

The `vagrant` post-processor outputs built .box files into the current
working directory.

```
<snip>
Build 'qemu' finished.

==> Builds finished. The artifacts of successful builds are:
--> qemu: 'qemu' provider box: opendaylight-4.1.0-centos-7.2.1511-libvirt.box
$ ls -rc | tail -n 1
opendaylight-4.1.0-centos-7.2.1511-libvirt.box
```

Import the local box into Vagrant with:

```
$ vagrant box add --name "odl" opendaylight-4.1.0-centos-1511.box --force
==> box: Adding box 'odl' (v0) for provider:
    box: Downloading: file:///home/daniel/packaging/packer/opendaylight-4.1.0-centos-1511.box
==> box: Successfully added box 'odl' (v0) for 'virtualbox'!
```

To connect to your new box, you'll need a trivial Vagrantfile:

```
$ vagrant init -m odl
$ cat Vagrantfile
Vagrant.configure(2) do |config|
  config.vm.box = "odl"
end
```

Boot the box and connect:

```
$ vagrant up
$ vagrant ssh
```

OpenDaylight will already be installed and running:

```
$ sudo systemctl is-active opendaylight
active
```

To connect to the Karaf shell:

```
$ ssh -p 8101 karaf@localhost
# password: karaf
```

#### Docker Images

The `docker-tag` post-processor imports the built Docker image into your local
image repository.

```
$ docker images
REPOSITORY          TAG         IMAGE ID        CREATED         SIZE
opendaylight/odl    4.1.0       8c9e8c24081e    2 days ago      1.408 GB
```

Use `docker run` to start a container. Point it at the Karaf executable
to run OpenDaylight as the container's process.

```
$ docker run -ti opendaylight/odl:4.1.0 /opt/opendaylight/bin/karaf
```

[1]: https://www.packer.io/

[2]: https://www.packer.io/intro/getting-started/setup.html

[3]: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging/ansible-opendaylight.git

[4]: https://atlas.hashicorp.com/opendaylight/boxes/odl

[5]: https://hub.docker.com/r/opendaylight/
