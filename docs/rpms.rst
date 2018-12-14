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
to the `RPM build logic in Integration/Packaging's repo`_. The job produces
both a noarch RPM and source RPM. The noarch RPM can be passed to test jobs for
validation. The source RPM can be downloaded to a system with the required
credentials and then pushed to the CentOS Community Build system to be built
into a noarch RPM on their servers and hosted in their repos.

The RPM and SRPM artifacts of the job are handled differently depending on the
Jenkins silo the job is executing in.

When running in production (releng silo), artifacts are hosted on Nexus. There
are RPM repos for each active branch (`oxygen-devel`_, `fluorine-devel`_,
`neon-devel`_). New builds are automatically added to the appropriate devel for
their branch.

When running in the sandbox, artifacts are thrown away by default. To keep an
artifact for further testing, either:

* Set the DEPLOY_TO_REPO parameter to opendaylight-epel-7-x86_64-devel. This is
  a scratch repo that sandbox packaging jobs have permission to push to.
  Packages will land in the `scratch repo on Nexus`_.
* Add a path regex that matches it to the Archive Artifacts param of the job
  (`ARCHIVE_ARTIFACTS=/home/jenkins/rpmbuild/RPMS/ noarch/opendaylight*.rpm`).
  The files matched will be stored in OpenDaylight's log archive along with the
  other job logs.

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

.. _intpak-rpm-repos:

Repositories
------------

OpenDaylight Nexus
^^^^^^^^^^^^^^^^^^

Packages resulting from build jobs running on OpenDaylight's infrastructure are
automatically hosted on OpenDaylight's Nexus repositories.

Continious Delivery Repositories
................................

OpenDaylight provides fully-automated Continuous Delivery pipelines for RPMs.

Every RPM built in the production RelEng Jenkins silo is pushed to the devel
repo appropriate for its branch. Builds are triggered for every successful
autorelase job, as well as daily using the latest available snapshot build.


Continuous Delivery repos for Oxygen and Fluorine:

- `opendaylight-oxygen-epel-7-x86_64-devel`_
- `opendaylight-fluorine-epel-7-x86_64-devel`_
- `opendaylight-neon-epel-7-x86_64-devel`_

CentOS Community Build System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While most RPM builds are triggered automatically in OpenDaylight's Jenkins,
some RPMs are promoted to be hosted in OpenDaylight's CentOS repositories.
There are a series of repos that are updated at varying frequencies, from
testing repos that are updated with pre-release versions very frequently to
release repos that are the permanent home of official OpenDaylight releases.

Release Repositories
....................

Repositories with the -release suffix host official OpenDaylight releases. They
are updated infrequently to never, and will host their release artifacts
forever. Release repos are subdivided into two groups based version numbers.
Repositories with both a major and minor version number (80, 83) are pinned to
a specific OpenDaylight release or service release (Oxygen 8.0.0, Oxygen SR3
8.3.0). Repositories with only a major version (8, 9) will always host the
latest service release from that major release. If a new SR comes out, the repo
will get the update (Oxygen SR4 will replace Oxygen SR3).

Release repo for the latest Oxygen and Fluorine service releases:

- `nfv7-opendaylight-8-release`_
- `nfv7-opendaylight-9-release`_

Release repos that will permanently host specific Oxygen and Fluorine releases:

- `nfv7-opendaylight-80-release`_
- `nfv7-opendaylight-81-release`_
- `nfv7-opendaylight-82-release`_
- `nfv7-opendaylight-83-release`_
- `nfv7-opendaylight-84-release`_
- `nfv7-opendaylight-90-release`_
- `nfv7-opendaylight-91-release`_

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

    sudo curl -o /etc/yum.repos.d/opendaylight-10-devel.repo \
      "https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=blob_plain;f=packages/rpm/example_repo_configs/opendaylight-10-devel.repo"

Standard install commands will now find the repository as expected.

    sudo dnf install -y opendaylight

The latest RPM in the repo will be installed.

Custom RPMs
-----------

It's possible for developers to build custom RPMs, typically with unmerged
patches that need system testing.

Most developers will want to run these jobs in the ODL Jenkins sandbox
instance, as only a few community members have permission to manually trigger
jobs on the releng Jenkins instance. See the `Jenkins sandbox`_ docs for
details about how to get permissions to trigger sandbox jobs, required
configuration and normal usage.

To build an custom distribution with unmerged code, first use the
`integration-multipatch-test`_ job to create distribution that includes the set
of unmerged patches.  See the `Custom Distributions
<distribution-job-builds.html#custom- distributions>`_ section for extensive
docs.

Once you have the distribution you want to package as an RPM, pass it to the
`packaging-build-rpm job`_ to do the build. Use the See the `packaging-build-rpm`_
section for docs.

.. _packaging-build-rpm job: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/
.. _parameters: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-master/build
.. _RPM build logic in Integration/Packaging's repo: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;f=packages/rpm
.. _packaging-build-rpm-snap job: https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-snap-master/
.. _packaging-test-rpm job: https://jenkins.opendaylight.org/releng/job/packaging-test-rpm-master/
.. _opendaylight-oxygen-epel-7-x86_64-devel: https://nexus.opendaylight.org/content/repositories/opendaylight-oxygen-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/
.. _opendaylight-fluorine-epel-7-x86_64-devel: https://nexus.opendaylight.org/content/repositories/opendaylight-fluorine-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/
.. _opendaylight-neon-epel-7-x86_64-devel: https://nexus.opendaylight.org/content/repositories/opendaylight-neon-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/
.. _oxygen-devel: https://nexus.opendaylight.org/content/repositories/opendaylight-oxygen-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/
.. _fluorine-devel: https://nexus.opendaylight.org/content/repositories/opendaylight-fluorine-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/
.. _neon-devel: https://nexus.opendaylight.org/content/repositories/opendaylight-fluorine-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/
.. _nfv7-opendaylight-80-release: http://cbs.centos.org/repos/nfv7-opendaylight-80-release/x86_64/os/Packages/
.. _nfv7-opendaylight-81-release: http://cbs.centos.org/repos/nfv7-opendaylight-81-release/x86_64/os/Packages/
.. _nfv7-opendaylight-82-release: http://cbs.centos.org/repos/nfv7-opendaylight-82-release/x86_64/os/Packages/
.. _nfv7-opendaylight-83-release: http://cbs.centos.org/repos/nfv7-opendaylight-83-release/x86_64/os/Packages/
.. _nfv7-opendaylight-84-release: http://cbs.centos.org/repos/nfv7-opendaylight-84-release/x86_64/os/Packages/
.. _nfv7-opendaylight-90-release: http://cbs.centos.org/repos/nfv7-opendaylight-90-release/x86_64/os/Packages/
.. _nfv7-opendaylight-91-release: http://cbs.centos.org/repos/nfv7-opendaylight-91-release/x86_64/os/Packages/
.. _nfv7-opendaylight-8-release: http://cbs.centos.org/repos/nfv7-opendaylight-8-release/x86_64/os/Packages/
.. _nfv7-opendaylight-9-release: http://cbs.centos.org/repos/nfv7-opendaylight-9-release/x86_64/os/Packages/
.. _example repo config files for each official repository: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;f=packages/rpm/example_repo_configs
.. _integration-multipatch-test: https://jenkins.opendaylight.org/releng/search/?q=integration-multipatch-test
.. _Jenkins sandbox: https://docs.opendaylight.org/en/stable-carbon/submodules/releng/builder/docs/jenkins.html#jenkins-sandbox
.. _scratch repo on Nexus: https://docs.opendaylight.org/en/stable-carbon/submodules/releng/builder/docs/jenkins.html#jenkins-sandbox
