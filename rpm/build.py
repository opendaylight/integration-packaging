#!/usr/bin/env python
"""Build OpenDaylight's RPMs using YAML build configs and Jinja2 templates."""

import os
import sys
import argparse
from pprint import pprint
import shutil
import subprocess
from string import Template
from time import sleep

try:
  import yaml
except ImportError:
  sys.stderr.write("ERROR: Are you using our Vagrant env?")
  raise

import cache.cache as cache
import specs.build_specs as build_specs

# Common paths used in this script
# Path to the directory that contains this file is assumed contain the build vars
build_vars_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(build_vars_dir, "cache")
specs_dir = os.path.join(build_vars_dir, "specs")
rpmbuild_dir = os.path.join(os.path.expanduser("~"), "rpmbuild")
src_in_dir = os.path.join(rpmbuild_dir, "SOURCES/")
spec_in_dir = os.path.join(rpmbuild_dir, "SPECS")
srpm_out_dir = os.path.join(rpmbuild_dir, "SRPMS")
rpm_out_dir = os.path.join(rpmbuild_dir, "RPMS", "noarch")

# Load RPM build variables from a YAML config file
with open(os.path.join(build_vars_dir, "build_vars.yaml")) as rpm_var_file:
  build_vars = yaml.load(rpm_var_file)

# Accept the version(s) of the build(s) to perform as args
# TODO: More docs on ArgParser and argument
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="append",
                    metavar="major minor patch rpm", nargs="*", type=int,
                    help="RPM version(s) to build")
parser.add_argument("-a", "--all", action="store_true", help="Build all RPMs")

# Print help if no arguments are given
if len(sys.argv) == 1:
  parser.print_help()
  sys.exit(1)

# Parse the given args
args = parser.parse_args()

# Build list of RPM builds to perform
builds = []
if args.all:
  builds = build_vars["builds"]
else:
  # Build a list of requested versions represented as dicts of version components
  versions = []
  version_keys = ["version_major", "version_minor", "version_patch", "rpm_release"]
  # For each version arg, match all version components to their build_vars name
  for version in args.version:
    versions.append(dict(zip(version_keys, version)))

  # Find every RPM build that matches any version argument
  # A passed version "matches" a build when the provided version components
  # are a subset of the version components of a build. Any version components
  # that aren't passed are simply not checked, so they can't fail the match,
  # effectively wild-carding them.
  for build in build_vars["builds"]:
    for version in versions:
      # Converts both dicts' key:value pairs to lists of tuples and checks
      # that each tuple in the version list is present in the build list.
      if all(item in build.items() for item in version.items()):
        builds.append(build)

# Templates that can be specialized into artifact names per-build
odl_template = Template("distribution-karaf-0.$version_major."
  "$version_minor-$codename.tar.gz")
specfile_template = Template("opendaylight-$version_major.$version_minor."
  "$version_patch-$rpm_release.spec")
unitfile_tb_template = Template("opendaylight-$sysd_commit.service.tar.gz")
rpm_template = Template("opendaylight-$version_major.$version_minor."
  "$version_patch-$rpm_release.el7.noarch.rpm")
srpm_template = Template("opendaylight-$version_major.$version_minor."
  "$version_patch-$rpm_release.el7.src.rpm")

def build(build):
  """Build the RPMs described by the given build description.

  :param build: Description of an RPM build, typically from rpm_vars.yaml
  :type build: dict

  """
  # Specialize a series of name/URL templates for the given build
  odl_tarball = odl_template.substitute(build)
  odl_rpm = rpm_template.substitute(build)
  odl_srpm = srpm_template.substitute(build)
  odl_specfile = specfile_template.substitute(build)
  unitfile_tarball = unitfile_tb_template.substitute(build)

  # After building strings from the name templates, build their full path
  odl_tarball_path = os.path.join(cache_dir, odl_tarball)
  unitfile_tarball_path = os.path.join(cache_dir, unitfile_tarball)
  specfile_path = os.path.join(specs_dir, odl_specfile)
  spec_in_path = os.path.join(spec_in_dir, odl_specfile)
  rpm_out_path = os.path.join(rpm_out_dir, odl_rpm)
  srpm_out_path = os.path.join(srpm_out_dir, odl_srpm)

  # Call a helper function to cache the artifacts required for each build
  cache.cache_build(build)

  # Call helper script to build the required RPM .spec files
  build_specs.build_spec(build)

  # Clean up old rpmbuild dir structure if it exists
  if os.path.isdir(rpmbuild_dir):
    shutil.rmtree(rpmbuild_dir)

  # Create rpmbuild dir structure
  subprocess.call("rpmdev-setuptree")

  # Move unitfile, tarball and specfile to correct rpmbuild dirs
  shutil.copy(odl_tarball_path, src_in_dir)
  shutil.copy(unitfile_tarball_path, src_in_dir)
  shutil.copy(specfile_path, spec_in_dir)

  # Call rpmbuild, build both SRPMs/RPMs
  subprocess.call(["rpmbuild", "-ba", spec_in_path])

  # Copy the RPMs/SRPMs from their output dir to the cache dir
  shutil.copy(rpm_out_path, cache_dir)
  shutil.copy(srpm_out_path, cache_dir)

if __name__ == "__main__":
  for build_dict in builds:
    build(build_dict)
