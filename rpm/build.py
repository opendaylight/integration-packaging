#!/usr/bin/env python
"""TODO"""

import os
import sys
import argparse
from pprint import pprint
import shutil
import subprocess

try:
  import yaml
except ImportError:
  sys.stderr.write("ERROR: Are you using our Vagrant env?")
  raise

import cache.cache as cache
import specs.build_specs as build_specs

# Path to the directory that contains this file is assumed contain the build vars
build_vars_dir = os.path.dirname(os.path.abspath(__file__))

# Load RPM build variables from a YAML config file
with open(os.path.join(build_vars_dir, "build_vars.yaml")) as rpm_var_file:
  build_vars = yaml.load(rpm_var_file)

# Accept the version(s) of the build(s) to perform as args
# TODO: More docs on ArgParser and argument
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="append",
                    metavar="major minor patch rpm", nargs="*", type=int,
                    help="RPM version(s) to build")
# TODO: Add a --all flag
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

# Call a helper function to cache the artifacts required for each build
for build in builds:
  cache.cache_build(build)

# Call helper script to build the required RPM .spec files
for build in builds:
  build_specs.build_spec(build)

# Clean up old rpmbuild dir structure if it exists
if os.path.isdir("/home/vagrant/rpmbuild"):
  shutil.rmtree("/home/vagrant/rpmbuild")

# Create rpmbuild dir structure
subprocess.Popen("rpmdev-setuptree")

# TODO: Move unitfile, tarball and specfile to correct rpmbuild dirs
# TODO: Call rpmbuild, build both SRPMs/RPMs
# TODO: Copy the RPMs/SRPMs from their output dir to the cache dir
