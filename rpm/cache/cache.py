#!/usr/bin/env python
"""Read YAML description of RPM builds and cache the required artifacts."""

import sys
import os
import urllib
import tarfile
from string import Template

try:
  import yaml
except ImportError:
  sys.stderr.write("We recommned using our included Vagrant env.\n")
  sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
  raise

# Path to the directory that contains this file is assumed to be the cache dir
cache_dir = os.path.dirname(os.path.abspath(__file__))

# Later paths are assumed to be relative to the cache dir
# TODO: Don't do this
# FIXME: This is breaking build.py
#os.chdir(cache_dir)

# Templates that can be specialized into artifact names/paths per-build
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


def cache_build(build):
  """Cache the artifacts required for the given RPM build.

  :param build: Description of an RPM build, typically from rpm_vars.yaml
  :type build: dict

  """
  # Specialize a series of name/URL templates for the given build
  odl_tarball = odl_template.substitute(build)
  odl_tarball_url = odl_url_template.substitute(build)
  unitfile = unitfile_template.substitute(build)
  unitfile_url = unitfile_url_template.substitute(build)
  unitfile_tarball = unitfile_tb_template.substitute(build)

  # After building strings from the name templates, build their full path
  odl_tarball_path = os.path.join(cache_dir, odl_tarball)
  unitfile_path = os.path.join(cache_dir, unitfile)
  unitfile_tarball_path = os.path.join(cache_dir, unitfile_tarball)

  # Cache appropriate version of OpenDaylight's release tarball
  if not os.path.isfile(odl_tarball_path):
    urllib.urlretrieve(odl_tarball_url, odl_tarball_path)
    print("Cached: {}".format(odl_tarball))
  else:
    print("Already cached: {}".format(odl_tarball))

  # Cache appropriate version of OpenDaylight's systemd unitfile as a tarball
  if not os.path.isfile(unitfile_tarball_path):
    urllib.urlretrieve(unitfile_url, unitfile_path)
    with tarfile.open(unitfile_tarball_path, "w:gz") as tb:
      tb.add(unitfile_path)
    os.remove(unitfile_path)
    print("Cached: {}".format(unitfile_tarball))
  else:
    print("Already cached: {}".format(unitfile_tarball))


# If run as a script, cache artifacts required for all builds
if __name__ == "__main__":
  # Load RPM build variables from a YAML config file
  with open(os.path.join(cache_dir, os.pardir, "build_vars.yaml")) as var_file:
    build_vars = yaml.load(var_file)

  for build in build_vars["builds"]:
    cache_build(build)
