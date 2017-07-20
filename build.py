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

from rpm import build as build_rpm

if __name__ == "__main__":
    # Accept the version(s) of the build(s) to perform as args
    # TODO: More docs on ArgParser and argument
    parser = argparse.ArgumentParser(conflict_handler='resolve')

    new_build_group = parser.add_argument_group("New build")
    new_build_group.add_argument(
        "--download_url", help="Tarball to repackage into RPM")
    new_build_group.add_argument(
        "--sysd_commit", help="Version of ODL unitfile to package")
    new_build_group.add_argument(
        "--changelog_date", help="Date this RPM was defined")
    new_build_group.add_argument(
        "--changelog_name", help="Name of person who defined RPM")
    new_build_group.add_argument(
        "--changelog_email", help="Email of person who defined RPM")

    # Arguments needed to build RPM from latest snapshot
    # given a stable major branch
    latest_snap_group = parser.add_argument_group("Latest snapshot build")
    latest_snap_group.add_argument("--build-latest-snap", action='store_true',
                                   help="Build RPM from the latest snpashot")
    latest_snap_group.add_argument("--major", help="Stable branch from which "
                                   "to build the snapshot")
    latest_snap_group.add_argument("--minor", help="Minor version of the "
                                   "stable branch to build the snapshot")
    latest_snap_group.add_argument("--sysd_commit",
                                   help="Version of ODL unitfile to package")
    latest_snap_group.add_argument("--changelog_name",
                                   help="Name of person who defined RPM")
    latest_snap_group.add_argument("--changelog_email",
                                   help="Email of person who defined RPM")
    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the given args
    args = parser.parse_args()

    # A dictionary containing essential build variables
    build = {}
    # Check if `changelog_date` has been passed as an arg
    # The current datetime should be the default date for RPM changelog date
    # but can still accept optional `changelog_date` param
    # `changelog_date` is in the format: 'Sat Dec 10 2016'
    # Docs:
    #   https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    if not args.changelog_date:
        args.changelog_date = datetime.date.today().strftime("%a %b %d %Y")

    # Check if `sysd_commit` has been passed as an arg
    # Use latest Int/Pack repo commit hash as sysd_commit var
    # unless passed by param
    if not args.sysd_commit:
        args.sysd_commit = build_rpm.get_sysd_commit()

    # If download_url is given, update version info
    if args.download_url:
        build.update({"download_url": args.download_url})
        version = build_rpm.extract_version(args.download_url)
        build.update(version)

    # Common parameters for all new and snapshot builds
    build.update({"sysd_commit": args.sysd_commit,
                  "changelog_name": args.changelog_name,
                  "changelog_email": args.changelog_email,
                  "changelog_date": args.changelog_date,
                  })

    # If the flag `--build-latest-snap` is true, extract information
    # from the snapshot URL using major version and minor version(optional)
    # info, else proceed directly to build the RPM
    if args.build_latest_snap:
        if args.major:
            build.update({'version_major': args.major})
            if args.minor:
                build.update({'version_minor': args.minor})
            build_rpm.build_snapshot_rpm(build)
    else:
        build_rpm.build_rpm(build)
