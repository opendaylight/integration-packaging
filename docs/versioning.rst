Versioning
==========

Documentation about OpenDaylight's upstream versioning.

Overview
--------

Opendaylight has a variety of types of version numbers. Internal ODL features
have versions, but they are not visible to external consumers of OpenDaylight.
OpenDaylight, built into a distribution of many features, has a version number.
OpenDaylight is repackaged in a variety of formats (RPMs, .debs, Docker images,
Vagrant base boxes, etc) and follows the guidelines for each. OpenDaylight
packages are consumed by configuration management tooling (Ansible, Puppet),
which also have their own types of versioning.

RPMs
----

The RPM versioning follows the `Fedora Packaging Guidelines`_.

- Major Version numbers that increment with each Simultaneous Release (5=Boron,
  6=Carbon, 7=Nitrogen, 8=Oxygen...).
- Minor Version numbers that increment with each Service Release (5.0=Boron,
  5.1=Boron SR1, 5.2=Boron SR2...).
- Patch Version is currently unused.
- Package Version numbers that increment for each new package build of the same
  ODL build (5.0.0-1=Boron, 5.0.0-2=Boron with RPM update).
- Snapshot/autorelease versions with timestamps and incrementing build numbers
  for pre-release builds (8.0.0-0.1.20171020rel2011=Oxygen pre-release
  autorelease build, 8.0.0-0.1.20171101snap835=Oxygen pre-release snapshot
  build...).

See the OpenDaylight builds on the `Nexus`_ or the `CentOS`_ Community Build
System for examples.

Debs
----

Mostly the same as RPMs, slightly different way of denoting pre-release builds.

Docker Images
-------------

Docker uses Major, Minor and Patch versions. It doesn't support pre-release
version numbers, which is okay since we don't currently build Docker images for
pre-release versions. See the `tags of the opendaylight/odl image`_ for
examples.

Vagrant Base Boxes
------------------

Vagrant follows `Rubygems versioning`_, which uses Major, Minor and Patch
versions for semver. It doesn't support pre-release version numbers, which is
okay since we don't currently build Vagrant base boxes for pre-release
versions. See the `versions of the opendaylight/odl base box`_ for examples.

Ansible Role
------------

The Ansible role follows `Semantic Versioning`_. Version bumps are based on API
changes. Backwards incompatible API changes cause Major Version bumps,
backwards compatible API changes cause minor version bumps, bugfixes and minor
updates can be batched into patch version bumps.

Puppet Module
-------------

The Puppet module follows `Semantic Versioning`_. Version bumps are based on
API changes. Backwards incompatible API changes cause Major Version bumps,
backwards compatible API changes cause minor version bumps, bugfixes and minor
updates can be batched into patch version bumps. See the `changelog`_ and
`metadata`_ for examples of correctly bumping versions.

.. _Fedora Packaging Guidelines: http://fedoraproject.org/wiki/Packaging:Versioning
.. _Nexus: https://nexus.opendaylight.org/content/repositories/opendaylight-oxygen-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/
.. _CentOS: http://cbs.centos.org/koji/packageinfo?packageID=755
.. _tags of the opendaylight/odl image: https://hub.docker.com/r/opendaylight/odl/tags/
.. _Rubygems versioning: http://guides.rubygems.org/patterns/#semantic-versioning
.. _versions of the opendaylight/odl base box: https://app.vagrantup.com/opendaylight/boxes/odl
.. _Semantic Versioning: http://semver.org/
.. _changelog: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging/puppet-opendaylight.git;a=blob;f=CHANGELOG
.. _metadata: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging/puppet-opendaylight.git;a=blob;f=metadata.json;h=713b3ef3f602ac5fdc4d11b655b8acf9f6908639;hb=HEAD#l3
