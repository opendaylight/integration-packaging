#!/usr/bin/env python
# Reads YAML description of RPM builds and caches the required artifacts

import os
import urllib
import tarfile
from string import Template

import yaml

odl_template = Template("distribution-karaf-0.$version_major."
  "$version_minor-$codename.tar.gz")
odl_url_template = Template("https://nexus.opendaylight.org/content/"
  "groups/public/org/opendaylight/integration/distribution-karaf/0."
  "$version_major.$version_minor-$codename/distribution-karaf-0."
  "$version_major.$version_minor-$codename.tar.gz")
unitfile_template = Template("opendaylight-$sysd_commit.service")
unitfile_url_template = Template("https://git.opendaylight.org/gerrit/"
  "gitweb?p=integration/packaging.git;a=blob_plain;f=rpm/unitfiles/"
  "opendaylight.service;hb=$sysd_commit")
unitfile_tb_template = Template("opendaylight-$sysd_commit.service.tar.gz")

# Path to the directory that contains this file is assumed to be the cache dir
cache_dir = os.path.dirname(os.path.abspath(__file__))

# Later paths are assumed to be relative to the cache dir
os.chdir(cache_dir)

# Load RPM build variables from a YAML config file
with open("../build_vars.yaml") as var_file:
  rpm_vars = yaml.load(var_file)

for build in rpm_vars["builds"]:
  odl_tarball = odl_tarball_template.substitute(build)
  odl_tarball_url = odl_tarball_url_template.substitute(build)
  unitfile = unitfile_template.substitute(build)
  unitfile_tarball = unitfile_tarball_template.substitute(build)
  unitfile_url = unitfile_url_template.substitute(build)

  # Cache appropriate version of OpenDaylight's release tarball
  if not os.path.isfile(odl_tarball):
    urllib.urlretrieve(odl_tarball_url, odl_tarball)
    print("Cached: {}".format(odl_tarball))
  else:
    print("Already cached: {}".format(odl_tarball))

  # Cache appropriate version of OpenDaylight's systemd unitfile
  if not os.path.isfile(unitfile):
    urllib.urlretrieve(unitfile_url, unitfile)
    print("Cached: {}".format(unitfile))
  else:
    print("Already cached: {}".format(unitfile))

  # Also cache a tarball of each ODL systemd unitfile
  if not os.path.isfile(unitfile_tarball):
    with tarfile.open(unitfile_tarball, "w:gz") as tb:
      tb.add(unitfile)
    print("Cached: {}".format(unitfile_tarball))
  else:
    print("Already cached: {}".format(unitfile_tarball))
