Packaging OpenDaylight Releases
===============================

These docs are for Integration/Packaging committers to reference while they
package OpenDaylight releases and service releases. Users should not, and would
not be able to due to missing permissions, follow this guide. This process is
not needed for Continuous Delivery pipeline packages, just formal releases.

Building on CentOS Community Build System
-----------------------------------------

OpenDaylight builds and hosts formal releases and service releases on the
CentOS Community Build System (CBS). Building on the CBS requires human
intervention, as the required credentials can't be stored on our build
systems. Continuous Delivery builds are hosted on Nexus to remove this need
for a human.

Find the release tarball. Make sure it's the one that has been promoted to the
opendaylight.releases Nexus repository, not the same build as a Release
Candidate before promotion. The packaging logic will only give release version
numbers for builds of artifacts from this release repository.

https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.1/karaf-0.8.1.tar.gz

Use the packaging-build-rpm job, for the right stream, to package the tarball.

TODO: Document getting permission to run jobs on RelEng Jenkins.

https://jenkins.opendaylight.org/releng/job/packaging-build-rpm-oxygen/

If it builds and passes tests, download the resulting source RPM from Nexus.

https://nexus.opendaylight.org/content/repositories/opendaylight-oxygen-epel-7-x86_64-devel/

Build the SRPM on the CentOS CBS, using the build target for this release.

TODO: Document adding build targets to CBS, only needed for new major releases
TODO: Document getting CBS permissions

    cbs build nfv7-opendaylight-8-el7 opendaylight-8.1.0-1.el7.src.rpm

After the SRPM uploads and the noarch RPM builds, tag it to the appropriate
build tags for this release. If this is the first time tag has been used,
you'll also need to add the package to the tag.

Releases should typically be tagged to three related tags.

* Testing tag for this major version

    cbs tag-build nfv7-opendaylight-8-testing opendaylight-8.1.0-1.el7

* Release tag for this major.minor version

    cbs add-pkg nfv7-opendaylight-81-release opendaylight --owner=dfarrell07
    cbs tag-build nfv7-opendaylight-81-release opendaylight-8.1.0-1.el7

* Release tag for this major version

    cbs tag-build nfv7-opendaylight-8-release opendaylight-8.1.0-1.el7

It may be advisable to fully do the testing tag first, and only once everything
is verified working do the release tags.

Wait for the repository to regenerate and show the new package.

http://cbs.centos.org/repos/nfv7-opendaylight-8-testing/x86_64/os/Packages/

Once the RPM is available on the CBS, test it with the test-rpm-master job.

https://jenkins.opendaylight.org/releng/job/packaging-test-rpm-master/

If everything passes, link the main downloads documentation to the RPM in the
major.minor release repository. This is the permanent home for this version,
will not be overridden by later versions.

http://docs.opendaylight.org/en/latest/downloads.html

Updating Docs
-------------

Update the readthedocs downloads page to point at the new RPM.

https://git.opendaylight.org/gerrit/gitweb?p=docs.git;a=blob;f=docs/downloads.rst

Adding Example Configuration Files
----------------------------------

Add example configuration files for any new RPM repositories.

https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;f=packages/rpm/example_repo_configs

As a change that depends on the repository configuration file change, add a
Packer variables file for the ODL version and CBS repository URL.

https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;f=packer/vars

TODO: Document building/pushing VMs/containers after INTPAK-12 automation

Updating Tests for Release Events
---------------------------------

Various release-related events require changes in packaging test coverage.

Tests need to be updated when:

* New releases or service releases are cut
* Old releases or service releases go End-of-Life (EOL)
* New branches are added
* Branches go EOL
* Old temporary autorelease, snapshot or multipatch builds expire (every 30-60
  days)

Updating Unit Tests
+++++++++++++++++++

There are unit tests in Int/Pack that verify the Python build automation
scripts.

https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=blob;f=packages/test_lib.py

Update the unit tests by grepping around and copying examples.

Updating Functional Tests
+++++++++++++++++++++++++

There are functional tests in RelEng/Builder that build and test packages to
verify build jobs.

https://git.opendaylight.org/gerrit/gitweb?p=releng/builder.git;a=tree;f=jjb/packaging

Update the functional tests by grepping around and copying examples. Make sure
to update both the test cases and the default parameters.

Updating Puppet
---------------

The puppet-opendaylight Rakefile, which drives our functional Beaker tests,
needs to be updated when a new ODL major release comes out. It pulls the latest
from the <release>-devel Nexus repo (for a diffrent value for <release> on each
puppet-opendaylight branch), so it does not need to be updated for new SRs.

The default param in manafests/params.pp and rspec-puppet unit/acceptance tests
throughout the repo also need to be updated only for major versions, not SRs.

Updating Ansible
----------------

The default vars in vars/main.yml need to be updated for each major release and
SR. Grep around to find the places to update.

New example playbooks in the ansible-opendaylight/examples directory need to be
added for each new major release.

    rpm_<new devel branch major version>_devel.yml

    rpm_<just-released major version>_release.yml
