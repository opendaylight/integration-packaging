RPMs
====


Automated RPM Builds
--------------------

OpenDaylight Integration/Packaging has added support for many variations of
fully automated RPM builds.


Build RPM Job
^^^^^^^^^^^^^

The Jenkins `build_rpm job <https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/>`_
builds an ODL RPM described by the given build description, typically from
build_vars.yaml using build.py script.


Build Latest Snapshot Job
^^^^^^^^^^^^^^^^^^^^^^^^^

For a given major version, you can find the latest snapshot and build its .rpm
by passing `--build-latest-snap` to build.py. It extracts ODL version info from
URL to build artifact. Example,

.. code-block:: bash

     ./build.py --build-latest-snap --major 5

A complete command may look like,

.. code-block:: bash

     ./build.py --build-latest-snap --major 5 --minor 2 --patch 0 --sysd_commit 07f7c83b0ef46ad3809e5be03e09a77fe554eeae --changelog_name "Daniel Farrell" --changelog_email "dfarrell@redhat.com

The Jenkins `build_rpm_snap job <https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-snap-master/>`_
builds the latest snapshot into RPM. This job uses the new flag
'--build-latest-snap' and calls build.py and extracts required info from URL.


CentOS CBS RPMs
---------------

OpenDaylight's RPMs are built and hosted on the CentOS Community Build System's
Koji build servers.

All OpenDaylight RPMs, and the SRPMs with tarballs from the builds described
previously, are `permanently available for download <http://cbs.centos.org/koji/packageinfo?packageID=755>`_.

See the `Deployment#RPM <https://wiki.opendaylight.org/view/Deployment#RPM>`_
wiki for more information about RPMs.
