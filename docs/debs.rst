Debs
====

The build.py helper script is used for building OpenDaylight .debs. It can
build a set of .debs based on provided version arguments. The dynamic aspects
of  build, such as ODL and deb version info, have all been extracted to single
YAML configuration file.

The variables available for configuration and instructions on how to install
are documented `here <https://github.com/opendaylight/integration-packaging/blob/master/deb/README.markdown>`_.


Build deb Job
--------------

Jenkins `build_deb job <https://jenkins.opendaylight.org/releng/job/packaging-build-deb-master/>`_
that builds the .deb package described by the given build description, from
build_vars.yaml inside deb directory.
