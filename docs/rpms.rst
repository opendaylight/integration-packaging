RPMs
====

OpenDaylight has a mature RPM Continuous Delivery pipeline. Every autorelease
build is automatically packaged as an RPM, and even if autorelease is broken
a daily job builds the latest distribution snapshot build into an RPM.

RPMs can be passed to test jobs that install them, start OpenDaylight with its
systemd service, connect to the Karaf shell and verify basic functionality.

RPMs are hosted on the CentOS Community Build system repositories. Some repos
are updated very frequently with the latest builds, while others are permanent
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

The `packaging-build-rpm job`_ is the primary way to build an RPM from an
OpenDaylight distribution (built by `autorelease <autorelease-builds.html>`_
or the `snapshot distribution <distribution-job-builds.html>` job). It accepts
a set of `parameters`_ that can be used to configure the build and passes them
to the `RPM build logic in Integration/Packaging's repo`_. The resulting
artifacts are hosted on Jenkins for up to a week. The job actually produces
both a noarch RPM and source RPM. The noarch RPM can be passed to test jobs for
validation. The source RPM can be downloaded to a system with the required
credentials and then pushed to the CentOS Community Build system to be built
into a noarch RPM on their servers and hosted in their repos.

packaging-build-rpm-snap
^^^^^^^^^^^^^^^^^^^^^^^^

The `packaging-build-rpm-snap job`_ packages the most recent `snapshot
distribution <distribution-job-builds.html>` build from a given branch as an
RPM. This could be used by a developer to test code that was just merged, but
which has not been included in an `autorelease build
<autorelease-builds.html>`_ yet. The job is also triggered daily, to ensure
that OpenDaylight's Continuous Delivery pipeline is fed new builds even if
autorelease is broken.

Test Jobs
---------

packaging-test-rpm
^^^^^^^^^^^^^^^^^^

The `packaging-test-rpm job`_ accepts a link to an RPM and validates it. It
installs the package with the system's package manager, starts OpenDaylight's
systemd service, verifies that it's reported as active, connects to the Karaf
shell and checks that some key bundles are present.

Repositories
------------

CentOS
^^^^^^

While most RPM builds are triggered automatically in OpenDaylight's Jenkins,
some RPMs are promoted to be hosted in OpenDaylight's CentOS repositories.
There are a series of repos that are updated at varying frequencies, from
testing repos that are updated with pre-release versions very frequently to
release repos that are the permanent home of official OpenDaylight releases.

Testing Repositories
....................

Repositories with the -testing suffix are updated very frequently with
pre-release versions of OpenDaylight from the appropriate branch. New RPMs
replace the old ones, so installing from these repos will always provide the
most recent versions.

Testing repos for Boron, Carbon and Nitrogen:

- `nfv7-opendaylight-5-testing`_
- `nfv7-opendaylight-6-testing`_
- `nfv7-opendaylight-7-testing`_

Release Repositories
....................

Repositories with the -release suffix host official OpenDaylight releases. They
are updated infrequently to never, and will host their release artifacts
forever. Release repos are subdivided into two groups based version numbers.
Repositories with both a major and minor version number (52, 53, 60) are pinned
to a specific OpenDaylight release or service release (Boron SR2 5.2.0, Boron
SR3 5.3.0, Carbon 6.0.0). Repositories with only a major version (5, 6) will
always host the latest service release from that major release. If a new SR
comes out, the repo will get the update (Boron SR4 will replace Boron SR3).

Release repos for the latest Boron and Carbon service releases:

- `nfv7-opendaylight-5-release`_
- `nfv7-opendaylight-6-release`_

Release repos that will permanently host specific Boron and Carbon releases:

- `nfv7-opendaylight-50-release`_
- `nfv7-opendaylight-51-release`_
- `nfv7-opendaylight-52-release`_
- `nfv7-opendaylight-53-release`_
- `nfv7-opendaylight-60-release`_

Repository Configuration Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While it's possible to install RPMs directly (`dnf install -y <URL>`), it's
often easier to use a repository configuration file to install whatever the
latest RPM is in a given repo.

The OpenDaylight Integration/Packaging project provides `example repo config
files for each official repository`_.

Package managers like Yum and DNF will automatically find repo configuration
files placed in the /etc/yum.repos.d/ directory. Curl them into place with
something like:

    sudo curl -o /etc/yum.repos.d/opendaylight-7-testing.repo \
      "https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=blob_plain;f=packages/rpm/example_repo_configs/opendaylight-7-testing.repo"

Standard install commands will now find the repository as expected.

    sudo dnf install -y opendaylight

Custom RPMs
-----------

It's possible for developers to build custom RPMs, typically with unmerged
patches that need system testing. First, use the `integration-multipatch-test`_
job to create a custom distribution that includes the set of unmerged patches.
See the `Custom Distributions <distribution-job-builds.html#custom-
distributions>`_ section for extensive docs. Once you have a custom
distribution artifact, pass it to the `packaging-build-rpm job`_ to package it
as an RPM. See the `packaging-build-rpm`_ section for docs.

.. _packaging-build-rpm job: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/
.. _parameters: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/build
.. _RPM build logic in Integration/Packaging's repo: https://github.com/opendaylight/integration-packaging/blob/master/rpm/build.py
.. _packaging-build-rpm-snap job: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-snap-master/
.. _packaging-test-rpm job: https://jenkins.opendaylight.org/releng/job/packaging-test-rpm-master/
.. _nfv7-opendaylight-5-testing: http://cbs.centos.org/repos/nfv7-opendaylight-5-testing/x86_64/os/Packages/
.. _nfv7-opendaylight-6-testing: http://cbs.centos.org/repos/nfv7-opendaylight-6-testing/x86_64/os/Packages/
.. _nfv7-opendaylight-7-testing: http://cbs.centos.org/repos/nfv7-opendaylight-7-testing/x86_64/os/Packages/
.. _nfv7-opendaylight-5-release: http://cbs.centos.org/repos/nfv7-opendaylight-5-release/x86_64/os/Packages/
.. _nfv7-opendaylight-6-release: http://cbs.centos.org/repos/nfv7-opendaylight-6-release/x86_64/os/Packages/
.. _nfv7-opendaylight-50-release: http://cbs.centos.org/repos/nfv7-opendaylight-50-release/x86_64/os/Packages/
.. _nfv7-opendaylight-51-release: http://cbs.centos.org/repos/nfv7-opendaylight-51-release/x86_64/os/Packages/
.. _nfv7-opendaylight-52-release: http://cbs.centos.org/repos/nfv7-opendaylight-52-release/x86_64/os/Packages/
.. _nfv7-opendaylight-53-release: http://cbs.centos.org/repos/nfv7-opendaylight-53-release/x86_64/os/Packages/
.. _nfv7-opendaylight-60-release: http://cbs.centos.org/repos/nfv7-opendaylight-60-release/x86_64/os/Packages/
.. _example repo config files for each official repository: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;f=packages/rpm/example_repo_configs;hb=refs/heads/master
.. _integration-multipatch-test: https://jenkins.opendaylight.org/releng/search/?q=integration-multipatch-test
