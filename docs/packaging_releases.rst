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

https://nexus.opendaylight.org/content/repositories/opendaylight-oxygen-epel-7-x86_64-devel/org/opendaylight/integration-packaging/opendaylight/8.1.0-1.el7.src/opendaylight-8.1.0-1.el7.src.rpm

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

Also add example repository configuration files for any repositories that do
not already have them.

https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;f=packages/rpm/example_repo_configs

