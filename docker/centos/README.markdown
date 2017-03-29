# Example OpenDaylight CentOS Dockerfile

Example Dockerfile of OpenDaylight installed from an RPM on CentOS.

## Using

```
docker build -t <tag> .
docker run <tag>
# Karaf shell
```

Replace the tag name with one of your own choosing.

## Other OpenDaylight Containers

The OpenDaylight Integration/Packaging project maintains a Packer build
pipeline to build offical containers and VMs. The source can be found in
[Int/Pack's repo][1], the VMs packaged as [Vagrant boxes on Atlas][2], and
the [containers on DockerHub][3].

[1]: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;f=packer;hb=refs/heads/master "ODL Int/Pack repo"

[2]: https://atlas.hashicorp.com/opendaylight/boxes/odl "ODL Vagrant-based VMs"

[3]: https://hub.docker.com/r/opendaylight/odl/ "ODL containers"
