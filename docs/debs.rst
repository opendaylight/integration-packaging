Debs
====

The `build.py`_ helper script is used for building OpenDaylight .debs. It can
build a set of .debs based on provided version arguments. The dynamic aspects
of builds, such as ODL and deb version info, have all been extracted to single
YAML configuration file.

The variables available for configuration and instructions on how to install
are documented `here`_.


Build Deb Job
--------------

The Jenkins `build_deb job`_ builds the .deb package described by the `given
build description`_, using build.py inside the deb directory.


.. _build.py: https://github.com/opendaylight/integration-packaging/blob/master/packages/build.py
.. _here: https://github.com/opendaylight/integration-packaging/blob/master/packages/deb/README.markdown
.. _build_deb job: https://jenkins.opendaylight.org/releng/job/packaging-build-deb-master/
.. _given build description: https://jenkins.opendaylight.org/releng/job/packaging-build-deb-master/
