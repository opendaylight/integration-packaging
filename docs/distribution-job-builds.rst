Distribution Job Builds
=======================

Unlike autorelease builds, which build every project from source, distribution
jobs only build a few Karaf features. The other artifacts are pulled pre-built
from OpenDaylight's Nexus repository and packaged into the Karaf distribution.
This makes them much quicker (minutes instead of ~4 hours).

The other major difference between autorelease and distribution job builds is
that distribution jobs use the -SNAPSHOT artifact version suffixes that are
actually stored in version control, whereas autorelease builds rewrite versions
to use the suffix for the next release, like -Carbon-SR1 or -Nitrogen. Because
of this, distribution builds are sometimes called "snapshot builds".

For each active branch, builds created by distribution jobs can be found in the
subdirectories at `opendaylight.snapshot/org/opendaylight/integration
/distribution-karaf/`_. Each build artifact is versioned with a timestamp and
unique, incrementing build number.

Distribution Builds Triggered by Merge Jobs
-------------------------------------------

Distribution job builds are typically kicked off when a patch is merged into
a project. Projects define `<project>`-merge-<branch> Jenkins jobs, which are
kicked off by Gerrit merge event. To find the merge job for a Gerrit, look
for comments from the jenkins-releng user like "Build Started
https://jenkins.opendaylight.org/releng/job/netvirt-merge-boron/216/".

Alternatively, browse a project's Jenkins tab and look at the recent runs.
For example, go to https://jenkins.opendaylight.org/releng/, select
Merge-Carbon and you'll find the list of all project merge jobs in the format
`<project>`-merge-carbon. Click any to view the recent build job details and
logs.

Custom Distributions
--------------------

Distributions can be built with an additional set of unmerged patches. The
`integration-multipatch-test-<branch>`_ jobs allow users to specify a set of
patches to cherry-pick onto a project's source code before building. This is
very useful for testing complex changes that impact multiple projects.

To build a custom distribution that includes a set of unmerged patches, first
make sure you have permission to trigger Jenkins jobs. Send an email to the
OpenDaylight Helpdesk (helpdesk@opendaylight.org) to request access. Be sure
to include your Linux Foundation user ID in the request.

Once you can trigger Jenkins jobs, navigate to the Jenkins web UI for the
multipatch-test job of the branch you're interested in. Make sure you're
logged in, then click on the "Build with Parameters" link in the sidebar.
The only parameter that requires configuration is PATCHES_TO_BUILD. This is
a CSV list of patches in project[=checkout][:cherry-pick]* format. For each
given project, the job will checkout 0 or 1 specified patches, then cherry-pick
0 or more additional patches on top of that checkout. If no checkout is
specified, cherry-picks will be done on top of the tip of the branch of the
multipatch-test job you're using.

For example, to build with a single unmerged patch from NetVirt:

    netvirt:59/50259/47

Because of the colon, this would cherry-pick the change on top of the tip
of the multipatch-test job branch.

To build with the same NetVirt patch, but by directly checking it out, use
an equals sign.

    netvirt=59/50259/47

This will be the same thing if the patch has recently been rebased on top
of the tip of the branch, but may be different if the patch is based on a
different set of patches.

To build with checked-out patches from Genius and NetVirt:

    genius=32/53632/9,netvirt=59/50259/47

To checkout a patch from controller, then cherry-pick another on top of it:

    controller=61/29761/5:45/29645/6

The numbers in the changeset are the Gerrit change ID of the patch (middle
number) and the patchset of the Gerrit (last number). The first number is
just the last two digits of the Gerrit change ID (I'm not sure why this is
necessary). I belive it's required that patches be listed in the order the
projects are built (NetVirt depends on Genius, so Genius is listed first).

For the definitive explination of how the multipatch job works, see the `JJB
source that defines it`_.

.. _opendaylight.snapshot/org/opendaylight/integration /distribution-karaf/: https://nexus.opendaylight.org/content/repositories/opendaylight.snapshot/org/opendaylight/integration/karaf/
.. _integration-multipatch-test-<branch>: https://jenkins.opendaylight.org/releng/search/?q=integration-multipatch-test
.. _JJB source that defines it: https://github.com/opendaylight/releng-builder/blob/master/jjb/integration/multipatch-distribution.sh
