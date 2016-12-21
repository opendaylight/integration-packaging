Distribution Job Builds
=======================

Unlike autorelease builds, which build every project from source, distribution
jobs only build a few Karaf features. This makes them much quicker (minutes
instead of ~11 hours), and therefore suitable for CI testing. End-users like
OPNFV should stick with autorelease jobs.


Snapshot Builds
---------------

Distribution job builds are typically kicked off when a patch is merged into
a project. Projects define `<project>`-merge-<branch> Jenkins jobs, which are
kicked off by a Gerrit merge events. To find the merge job for a Gerrit, look
for comments from the jenkins-releng user like "Build Started
https://jenkins.opendaylight.org/releng/job/netvirt-merge-boron/216/".

Alternatively, browse a project's Jenkins tab and look at the recent runs.
Example, go to https://jenkins.opendaylight.org/releng/, select Merge-Boron,
you'll find the list of all projects merge jobs in the format
`<project>`-merge-boron. Click any to view the recent build job details and
the logs.

For each active branch, snapshot builds created by distribution jobs can be
found in the subdirs at `opendaylight.snapshot/org/opendaylight/integration/distribution-karaf/
<https://nexus.opendaylight.org/content/repositories/opendaylight.snapshot/org/opendaylight/integration/distribution-karaf/>`_.
The maven-metadata.xml tells about the different versions and the latest one.
The different subdirectories (say, 0.5.2-SNAPSHOT) contain all the
corresponding version (0.5.2 here) builds stored by time (time included in
the artifact name).

Recent build artifacts info for a given branch can be found in the following
XML's `<content-item>` at `opendaylight.snapshot/content/org/opendaylight/integration/distribution-karaf/0.5.2-SNAPSHOT/ <https://nexus.opendaylight.org/service/local/repositories/opendaylight.snapshot/content/org/opendaylight/integration/distribution-karaf/0.5.2-SNAPSHOT/>`_ for 0.5.2 version.


Custom Distributions
--------------------

Distributions can be built with an additional set of unmerged patches. `See
this wiki <https://wiki.opendaylight.org/view/Integration/Test/Running_System_Tests#Running_System_Tests_Using_Custom_Distribution_Built_From_Multiple_Patches>`_.
