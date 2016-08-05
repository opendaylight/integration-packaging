#!/usr/bin/env python
"""Build OpenDaylight's .debs using YAML build configs and Jinja2 templates."""

import os
import sys
import argparse
import subprocess
from string import Template

try:
    import yaml
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise

import templates.build_debianfiles as build_deb

# Common paths used in this script
# This file is assumed to be in the root of the .deb build logic's dir structure
project_root = os.path.dirname(os.path.abspath(__file__))

# Debian templates directory
templates_dir = os.path.join(project_root, "templates")

# Specialized opendaylight directory for each build
odl_dir_template = Template("opendaylight/opendaylight-$version_major.$version_minor."
                            "$version_patch-$pkg_version/")


def build_deb_files(build):
    """Build the .deb described by the given build description.

    :param build: Description of a debian build, typically from build_vars.yaml
    :type build: dict

    """
    odl_dir_name = odl_dir_template.substitute(build)
    odl_dir_path = os.path.join(templates_dir, os.pardir, odl_dir_name)

    # Call helper script to build the required debian files
    build_deb.build_deb(build)

    # Build debian package
    os.chdir(odl_dir_path)
    subprocess.call(["dpkg-buildpackage", "-us -uc -b", odl_dir_path], shell=True)

    # Install opendaylight's dependencies
    control_file_path = os.path.join(odl_dir_path, "debian/control")
    subprocess.call(["sudo mk-build-deps -i " + control_file_path], shell=True)

    os.chdir(project_root)


# When run as a script, accept a set of builds and execute them
if __name__ == "__main__":
    # Load .deb build variables from a YAML config file
    build_vars_path = os.path.join(project_root, "build_vars.yaml")
    with open(build_vars_path) as deb_var_file:
        build_vars = yaml.load(deb_var_file)

    # Accept the version(s) of the build(s) to perform as args
    parser = argparse.ArgumentParser()
    existing_build_group = parser.add_argument_group("Existing build")
    existing_build_group.add_argument(
        "-v", "--version", action="append", metavar="major minor patch deb",
        nargs="*", help="Deb version(s) to build"
    )
    new_build_group = parser.add_argument_group("New build")
    new_build_group.add_argument("--major", help="Major (element) version to build")
    new_build_group.add_argument("--minor", help="Minor (SR) version to build")
    new_build_group.add_argument("--patch", help="Patch version to build")
    new_build_group.add_argument("--deb",   help="Deb version to build")
    new_build_group.add_argument("--sysd_commit", help="Version of ODL unitfile to package")
    new_build_group.add_argument("--codename", help="Codename for ODL version")
    new_build_group.add_argument("--download_url", help="Tarball to repackage into .deb")
    new_build_group.add_argument("--java_version", help="Java dependency for the ODL release")
    new_build_group.add_argument("--changelog_date", help="Date this .deb was defined")
    new_build_group.add_argument("--changelog_time", help="Time this .deb was defined")
    new_build_group.add_argument("--changelog_name", help="Name of person who defined .deb")
    new_build_group.add_argument("--changelog_email", help="Email of person who defined .deb")

    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the given args
    args = parser.parse_args()

    # Build list of .deb builds to perform
    builds = []
    if args.version:
        # Build a list of requested versions as dicts of version components
        versions = []
        version_keys = ["version_major", "version_minor", "version_patch",
                        "pkg_version"]
        # For each version arg, match all version components to build_vars name
        for version in args.version:
            versions.append(dict(zip(version_keys, version)))

        # Find every .deb build that matches any version argument
        # A passed version "matches" a build when the provided version
        # components are a subset of the version components of a build. Any
        # version components that aren't passed are simply not checked, so
        # they can't fail the match, effectively wild-carding them.
        for build in build_vars["builds"]:
            for version in versions:
                # Converts both dicts' key:value pairs to lists of tuples and
                # checks that each tuple in the version list is present in the
                # build list.
                if all(item in build.items() for item in version.items()):
                    builds.append(build)
    else:
        builds.append({"version_major": args.major,
                       "version_minor": args.minor,
                       "version_patch": args.patch,
                       "pkg_version": args.deb,
                       "sysd_commit": args.sysd_commit,
                       "codename": args.codename,
                       "download_url": args.download_url,
                       "java_version": args.java_version,
                       "changelog_date": args.changelog_date,
                       "changelog_time": args.changelog_time,
                       "changelog_name": args.changelog_name,
                       "changelog_email": args.changelog_email})

    for build in builds:
        build_deb_files(build)
