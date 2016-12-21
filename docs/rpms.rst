RPMs
====


Automated RPMs
--------------

OpenDaylight Integration/Packaging is `working <https://git.opendaylight.org/gerrit/#/c/42083/>`_
on adding support for fully automated RPM builds].

Getting Latest Snapshot RPM
---------------------------
For a given major version, you can find the latest snapshot and build its .rpm
by passing `--build-latest-snap` to build.py. It extracts ODL version info from
URL to build artifact. Example,

.. code-block:: bash

     ./build.py --build-latest-snap --major 5

A complete command may look like,

.. code-block:: bash

     ./build.py --build-latest-snap --major 5 --minor 2 --patch 0 --rpm 0.1.20161212snap531 --sysd_commit 07f7c83b0ef46ad3809e5be03e09a77fe554eeae --changelog_name "Daniel Farrell" --changelog_email "dfarrell@redhat.com


CentOS CBS RPMs
---------------

OpenDaylight's RPMs are built and hosted on the CentOS Community Build System's
Koji build servers.

All OpenDaylight RPMs, and the SRPMs with tarballs from the builds described
above, are `permanently available for download <http://cbs.centos.org/koji/packageinfo?packageID=755>`_.

See the `Deployment#RPM <https://wiki.opendaylight.org/view/Deployment#RPM>`_
wiki for more information about RPMs.


Jenkins Job builds
------------------

build_rpm job
^^^^^^^^^^^^^
`This Jenkins job <https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/>`_
builds a RPM described by the given build description, typically from
build_vars.yaml using build.py script.

build_rpm_snap job
^^^^^^^^^^^^^^^^^^

`Jenkins job <https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-snap-master/>`_
to build the latest snapshot into RPM. This job uses the new flag
'--build-latest-snap' and calls build.py after removing unnecessary parameters
and extracting info from URL.
