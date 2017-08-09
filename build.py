#!/usr/bin/env python

##############################################################################
# Copyright (c) 2016 Daniel Farrell and Others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

import argparse
import datetime
import sys

from deb import build as build_deb
from rpm import build as build_rpm
import vars

try:
    from tzlocal import get_localzone
except ImportError:
    sys.stderr.write("we recommend using our include Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv")

if __name__ == "__main__":
    # Accept the version(s) of the build(s) to perform as args
    # TODO: More docs on ArgParser and argument
    parser = argparse.ArgumentParser(add_help=False,
                                     conflict_handler='resolve')
    parser._optionals.title = "Required Arguments"

    package_build_group = parser.add_mutually_exclusive_group(required=True)
    package_build_group.add_argument("--rpm", action="store_true",
                                     help="Builds RPM package")
    package_build_group.add_argument("--deb", action="store_true",
                                     help="Builds DEB package")

    new_build_group = parser.add_argument_group("New build")
    new_build_group.add_argument(
        "--download_url", help="Tarball to repackage into package")
    new_build_group.add_argument(
        "--sysd_commit", help="Version of ODL unitfile to package")
    new_build_group.add_argument(
        "--changelog_date", help="Date this package was defined")
    new_build_group.add_argument(
        "--changelog_name", help="Name of person who defined package")
    new_build_group.add_argument(
        "--changelog_email", help="Email of person who defined package")

    # Arguments needed to build RPM from latest snapshot
    # given a stable major branch
    latest_snap_group = parser.add_argument_group("Latest snapshot build")
    latest_snap_group.add_argument("--build-latest-snap", action='store_true',
                                   help="Build package from the latest snpashot")
    latest_snap_group.add_argument("--major", help="Stable branch from which "
                                   "to build the snapshot")
    latest_snap_group.add_argument("--minor", help="Minor version of the "
                                   "stable branch to build the snapshot")
    latest_snap_group.add_argument("--sysd_commit",
                                   help="Version of ODL unitfile to package")
    latest_snap_group.add_argument("--changelog_name",
                                   help="Name of person who defined package")
    latest_snap_group.add_argument("--changelog_email",
                                   help="Email of person who defined package")
    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the given args
    args = parser.parse_args()

    # A dictionary containing essential build variables
    build = {}

    # Check if the package to be created is rpm or deb and initialize timestamp
    # details with current time for packages accordingly. For details on
    # strftime please refer : https://docs.python.org/2/library/datetime.html#
    # strftime-and-strptime-behavior. For details on get_localzone refer :
    # https://pypi.python.org/pypi/tzlocal
    if args.rpm:
        # Building RPM only requires `changelog_date` in the format
        # "Day Month Date Year" For ex - Mon Jun 21 2017
        if not args.changelog_date:
            args.changelog_date = datetime.date.today().strftime("%a %b %d %Y")
    if args.deb:
        if not args.changelog_date:
            # Building Deb requires `changelog_date` and 'changelog_time' in
            # the format "Day, Date Month Year" For ex - Mon, 21 Jun 2017 and
            # time along with Time Zone information as UTC offset in format
            # HH:MM:SS +HHMM". For ex - 15:01:16 +0530
            args.changelog_date = datetime.date.today().\
                                                strftime("%a, %d %b %Y")
            local_tz = get_localzone()
            args.changelog_time = datetime.datetime.now(local_tz).\
                strftime("%H:%M:%S %z")
            # Add comment
            build.update({"changelog_time": args.changelog_time})

    # Check if `sysd_commit` has been passed as an arg
    # Use latest Int/Pack repo commit hash as sysd_commit var
    # unless passed by param
    if not args.sysd_commit:
        args.sysd_commit = vars.get_sysd_commit()

    # If the flag `--build-latest-snap` is true, extract information
    # from the snapshot URL using major version and minor version(optional)
    if args.build_latest_snap:
        if args.major:
            build.update({'version_major': args.major})
            if args.minor:
                build.update({'version_minor': args.minor})
            args.download_url = vars.get_snap_url(args.major, args.minor)

    # If download_url is given, update version info
    if args.download_url:
        build.update({"download_url": args.download_url})
        version = vars.extract_version(args.download_url)
        build.update(version)

    java_version_required = vars.get_java_version(build['version_major'])

    # Common parameters for all new and snapshot builds
    build.update({"download_url": args.download_url,
                  "sysd_commit": args.sysd_commit,
                  "java_version": java_version_required,
                  "changelog_name": args.changelog_name,
                  "changelog_email": args.changelog_email,
                  "changelog_date": args.changelog_date,
                  })
    if args.rpm:
        build_rpm.build_rpm(build)
    elif args.deb:
        build_deb.build_deb(build)
    else:
        raise ValueError("Unknown package type")
