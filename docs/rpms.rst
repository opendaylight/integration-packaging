RPMs
====


Automated RPM Builds
--------------------

OpenDaylight Integration/Packaging has added support for many variations of
fully automated RPM builds.


Build RPM Job
^^^^^^^^^^^^^

The Jenkins `build_rpm job <https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/>`_
builds an ODL RPM described by the `given Jenkins build parameters <https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/build?delay=0sec>`_, using build.py script.


Build Latest Snapshot Job
^^^^^^^^^^^^^^^^^^^^^^^^^

For a given major version, you can find the latest snapshot and build its .rpm
by passing `--build-latest-snap` to build.py.

The Jenkins `build_rpm_snap job <https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-snap-master/>`_
builds the latest snapshot into RPM. It extracts ODL version info from URL to
build artifacts. The necessary JJB params to pass are OpenDaylight's major and
minor version to build, sysd_commit (version of ODL systemd unitfile to
download and package in RPM), changelog name and email.


CentOS CBS RPMs
---------------

OpenDaylight's RPMs are built and hosted on the CentOS Community Build System's
Koji build servers.

All OpenDaylight RPMs, and the SRPMs with tarballs from the builds described
previously, are `permanently available for download <http://cbs.centos.org/koji/packageinfo?packageID=755>`_.

See the `Deployment#RPM <https://wiki.opendaylight.org/view/Deployment#RPM>`_
wiki for more information about RPMs.
