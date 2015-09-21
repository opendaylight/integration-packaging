#!/usr/bin/env python
# Reads YAML description of RPM builds and caches the required artifacts

import os
import urllib

import yaml

odl_tarball = "distribution-karaf-0.{version_major}.{version_minor}-{codename}.tar.gz"
odl_tarball_url = "https://nexus.opendaylight.org/content/groups/public/" \
                  "org/opendaylight/integration/distribution-karaf/0." \
                  "{version_major}.{version_minor}-{codename}/" + odl_tarball

# Path to the directory that contains this file is assumed to be the cache dir
cache_dir = os.path.dirname(os.path.abspath(__file__))

# Load RPM build variables from a YAML config file
with open(os.path.join(cache_dir, "../build_vars.yaml")) as var_file:
  rpm_vars = yaml.load(var_file)

for build in rpm_vars["builds"]:
  odl_tarball_path = os.path.join(cache_dir, odl_tarball.format(**build))
  if not os.path.isfile(odl_tarball_path):
    urllib.urlretrieve(odl_tarball_url.format(**build), odl_tarball_path)
    print("Cached: {}".format(odl_tarball_path))
  else:
    print("Already cached: {}".format(odl_tarball_path))

  # TODO: Cache systemd file or use local in .spec
