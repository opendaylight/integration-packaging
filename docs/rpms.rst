RPMs
====

OpenDaylight has a mature RPM Continuous Delivery pipeline. Every autorelease
build is automatically packaged as an RPM, and even if autorelease is broken
a daily job builds the latest distribution snapshot build into an RPM.

RPMs can be passed to test jobs that install them, start OpenDaylight with it's
systemd service, connect to the Karaf shell and verify basic functionality.

RPMs are hosted on the CentOS Community Build system repositories. Some repos
are updated very frequently with the latest builds, while others are permeate
homes of official releases.

Developers can build custom RPMs with pre-merge patches for testing by first
creating a custom distribution with the integration-multipatch-test job and
then feeding the resulting artifact to the packaging-build-rpm job.

Build Jobs
----------

OpenDaylight Integration/Packaging has added support for many variations of
fully automated RPM builds.

packaging-build-rpm
^^^^^^^^^^^^^^^^^^^

The `packaging-build-rpm`_ job is the primary way to build an RPM from an
OpenDaylight distribution (built by autorelease or the snapshot distribution
job). It accepts a set of `parameters`_ that can be used to configure the build
and passes them to the `RPM build logic in Integration/Packaging's repo`_. The
resulting artifacts are hosted on Jenkins for up to a week. The job actually
produces both a noarch RPM and source RPM. The noarch RPM can be passed to test
jobs for validation. The source RPM can be downloaded to a system with the
required credentials and then pushed to the CentOS Community Build system to
be built into a noarch RPM on their servers and hosted in their repos.

packaging-build-latest-rpm-snap
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



For a given major version, you can build an RPM from the latest snapshot by
passing `- -build-latest-snap` to build.py.

The Jenkins `build_rpm_snap job`_ builds the latest snapshot into RPM. It
extracts ODL version info from the artifact's URL to build artifacts. The
necessary JJB params to pass are OpenDaylight's major and minor version to
build, sysd_commit (version of ODL systemd unitfile to download and package
in RPM), changelog name and email.

Test Jobs
---------

packaging-test-rpm
------------------

TODO

Repositories
------------

OpenDaylight's RPMs are built and hosted on the CentOS Community Build System's
Koji build servers.

All OpenDaylight RPMs, and the SRPMs with tarballs from the builds described
previously, are permanently available for download `here`_.

See the `Deployment#RPM`_ wiki for more information about RPMs.

Custom RPMs
-----------

TODO

.. _packaging-build-rpm: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/
.. _parameters: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/build
.. _RPM build logic in Integration/Packaging's repo: https://github.com/opendaylight/integration-packaging/blob/master/rpm/build.py
.. _build_rpm_snap job: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-snap-master/
.. _here: http://cbs.centos.org/koji/packageinfo?packageID=755
.. _Deployment#RPM: https://wiki.opendaylight.org/view/Deployment#RPM
