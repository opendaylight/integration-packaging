Autorelease Builds
==================

OpenDaylight's primary build pipeline is called "autorelease". It is managed by
the `RelEng/Autorelease`_ project, and primarily takes the form of
`Autorelease's Jenkins jobs`_.

Autorelease builds every project from source. There are jobs for each current
OpenDaylight release, as well as the version under development.


Daily Releases
--------------

`Autorelease's Jenkins jobs`_ run daily for every active branch, including
master.

- `Beryllium autorelease job`_
- `Boron autorelease job`_
- `Carbon autorelease job`_

Each of those jobs, when the build is successful, produces build artifacts that
include an OpenDaylight distribution. To download the distribution, pick an
autorelease job that completed successfully (yellow or blue dot) and access its
logged console output. Logs are hosted on logs.opendaylight.org, at URLs like
`https://logs.opendaylight.org/releng/jenkins092/autorelease-release-<stream>/
<build_number>/`, where stream could be "boron" build_number "228". There will
be a link at the top of build's Jenkins page. Open `console.log.gz` in browser
and search for "staging repository with ID". Find the repositoiry ID, which
will be of the form "autorelease-1432". Navigate to `OpenDaylight's Nexus`_ and
find the staging repository with the same name. Drill down into the directory
tree org/opendaylight/integration/distribution-karaf/ to find the `build
artifacts`_. Autorelease build artifacts are persevered for 60 days.

Autorelease jobs trigger OpenDaylight's distribution tests when they complete.
To see the test results, go to integration-distribution-test-<branch> job's
Jenkins page, find the job that started after the autorelease in question
finished. Open it and explore `Subprojects` section for test results of all
the jobs triggered. For example, in case of Boron, you can find the list and
the results of jobs triggered `here`_.

The OpenDaylight Integration/Test project recently audited all tests to remove
false negatives that were cluttering this report with failures that didn't
imply a problem with OpenDaylight, but with test logic. If there are failures,
especially new ones, pay attention to which OpenDaylight features they affect.
If you don't load that Karaf feature, it shouldn't be relevant to you.

The latest successful autorelease builds can also be easily found by using the
`staging/org/opendaylight/integration/distribution-karaf/`_
and look for 0.4.5-Beryllium-SR5, 0.5.3-Boron-SR3 or 0.6.0-Carbon or similar
staging repositories. However, the artifacts in these repositories are not
static - they are replaced each time new artifacts are generated. Use the
"autorelease-XXXX" repositories described above for semi-persistent URLs.


Official Releases
-----------------

As a part of the OpenDaylight community's efforts to move towards Continuous
Delivery, there is very little mechanical difference between the automated
daily releases documented above and official releases. The same autorelease
job runs, builds artifacts and kicks off distribution tests against them. When
doing official releases, the OpenDaylight community iterates through those
builds (calling them Release Candidate 1, RC2, ...) until no blocking bugs are
found. The OpenDaylight Technical Steering Committee then hears feedback from
the Release Engineering and Integration/Test teams, and if all's well blesses
the build as an official release. The build's Nexus staging repo is then
promoted to a release repo and publicized (example: `opendaylight.release/org
/opendaylight/integration/distribution-karaf/0.5.2-Boron-SR2`_). Official
releases are persevered forever.

For more information about OpenDaylight releases, including timelines, see the
`Release Plans`_.


.. _RelEng/Autorelease: https://git.opendaylight.org/gerrit/gitweb?p=releng/autorelease.git;a=tree;h=refs/heads/master;hb=refs/heads/master
.. _Autorelease's Jenkins jobs: https://jenkins.opendaylight.org/releng/view/autorelease/
.. _Beryllium autorelease job: https://jenkins.opendaylight.org/releng/view/autorelease/job/autorelease-release-beryllium/
.. _Boron autorelease job: https://jenkins.opendaylight.org/releng/view/autorelease/job/autorelease-release-boron/
.. _Carbon autorelease job: https://jenkins.opendaylight.org/releng/view/autorelease/job/autorelease-release-carbon/
.. _OpenDaylight's Nexus: https://nexus.opendaylight.org/content/repositories/
.. _build artifacts: https://nexus.opendaylight.org/content/repositories/autorelease-1432/org/opendaylight/integration/distribution-karaf/0.5.0-Boron-RC1/
.. _here: https://jenkins.opendaylight.org/releng/job/integration-distribution-test-boron/
.. _staging/org/opendaylight/integration/distribution-karaf/: https://nexus.opendaylight.org/content/repositories/staging/org/opendaylight/integration/distribution-karaf/
.. _opendaylight.release/org /opendaylight/integration/distribution-karaf/0.5.2-Boron-SR2: https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.5.2-Boron-SR2/
.. _Release Plans: https://wiki.opendaylight.org/view/Release_Plan
