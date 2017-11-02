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
  6=Carbon...).
- Minor Version numbers that increment with each Service Release (5.0=Boron,
  5.1=Boron SR1...).
- Patch Version is unused currently, but may start being used as OpenDaylight
  moves towards SimVer and CR (5.0.0=Boron, 5.1.0=Boron SR1...).
- Package Version numbers that increment for each new package build of the same
  ODL build (5.0.0-1=Boron, 5.0.0-2=Boron with RPM update).
- Snapshot/autorelease versions with timestamps and incrementing build numbers
  for pre-release builds (5.0.0-0.1.20160912rel1495=Boron pre-release
  autorelease build, 5.1.0-0.1.20161019snap499=Boron SR1 pre-release snapshot
  build).

See the `OpenDaylight builds on the CentOS Community Build System`_ for
examples.

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
updates can be batch into patch version bumps. See the `git tags`_ for
examples.

Puppet Module
-------------

The Puppet module follows `Semantic Versioning`_. Version bumps are based on
API changes. Backwards incompatible API changes cause Major Version bumps,
backwards compatible API changes cause minor version bumps, bugfixes and minor
updates can be batch into patch version bumps. See the `git tags`_ for
examples.

.. _Fedora Packaging Guidelines: http://fedoraproject.org/wiki/Packaging:Versioning
.. _OpenDaylight builds on the CentOS Community Build System: http://cbs.centos.org/koji/packageinfo?packageID=755
.. _tags of the opendaylight/odl image: https://hub.docker.com/r/opendaylight/odl/tags/
.. _Rubygems versioning: http://guides.rubygems.org/patterns/#semantic-versioning
.. _versions of the opendaylight/odl base box: https://atlas.hashicorp.com/opendaylight/boxes/odl
.. _Semantic Versioning: http://semver.org/
.. _git tags: https://github.com/dfarrell07/ansible-opendaylight/releases
