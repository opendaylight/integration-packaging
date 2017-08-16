# OpenDaylight Debian Packages

Logic for building OpenDaylight's upstream Debian packages.

#### Table of Contents

1. [Overview](#overview)
2. [Vagrant Build Environment](#vagrant-build-environment)
3. [Docker provider](#docker-provider)
4. [Building Debs](#building-debs)
5. [Defining New Debs](#defining-new-debs)
6. [Deb Build Variables](#deb-build-variables)
7. [Using Debs](#using-debs)
8. [Installing](#installing)
9. [Uninstalling](#uninstalling)
10. [Using systemd](#using-systemd)
11. [Starting](#starting)
12. [Stopping](#stopping)
13. [Karaf shell](#karaf-)
14. [Using OpenSUSE Build Service](#using-obs)

## Overview

TODO: Overview of Debian pkg builds, plans

## Vagrant Build Environment

The included Vagrantfile defines a consistent, known-working and easily
shared environment. It supports both VM and container-based providers.

```
[~/packaging/deb]$ vagrant status
Current machine states:

default                   not created (libvirt)
[~/packaging/deb]$ vagrant up
[~/packaging/deb]$ vagrant ssh
[vagrant@localhost ~]$ ls /vagrant/
opendaylight  README.markdown  Vagrantfile
```

### Docker provider

The Vagrantfile defines a Docker provider, enabling easy access to build.py
in a container. The general command format is:

```
$ vagrant docker-run -- <flags to build.py>
```

To pass 5.0 (Boron) as the version to build:

```
$ vagrant docker-run -- -v 5 0
```

Dockerfile can be also used directly to build container image:

```
$ docker build -t "odl_deb" .
$ docker run -v $(pwd):/build odl_deb -v 5 0
```

## Building Debs

The `build.py` helper script is used for building OpenDaylight .debs.

The `build.py` helper script can build a set of .debs based on provided
version arguments.

```
[vagrant@localhost ~]$ /vagrant/build.py -h
usage: build.py [-h] [-v [major minor patch deb [major minor patch deb ...]]]
....

optional arguments:
  -h, --help            show this help message and exit

Existing build:
  -v [major minor patch deb [major minor patch deb ...]], --version [major minor patch deb [major minor patch deb ...]]
                    Deb version(s) to build
....
```

The `-v`/`--version` flag accepts a version number. Any build that matches
the portions provided will be built. If more than one build matches the
portions provided, all matching builds will be executed.

For example, `build.py -v 3` would execute the builds that match the regex
`3.*.*-*`. OpenDaylight 3.0.0-1 and 3.1.0-1, for example.

To only build a single debian package, provide enough version info to make
the match unique. For example, `build.py -v 2 4 0 1` could only match one
definition (Helium SR4, 2.4.0-1).

The `build.py` script uses `templates/build_debianfiles.py` to generate debian files for
ODL .deb packages using JinJa2 templates and dynamic build data provided in `build_vars.yaml`.

## Defining New Debs

The dynamic aspects of a build, such as ODL and Deb version info, have all
been extracted to a single YAML configuration file. For most Deb updates,
only that configuration file should need to be updated by humans.

The variables available for configuration are documented below. A build
definition should define all supported variables.

### Deb Build Variables

#### `version_major`

The OpenDaylight major (element) version number of the release to build.

For example, Hydrogen is 1.x.x, Helium is 2.x.x, Lithium is 3.x.x and so on
down the periodic table.

#### `version_minor`

The OpenDaylight minor (SR) version number of the release to build.

#### `version_patch`

The OpenDaylight patch version of the release to build.

#### `pkg_version`

Debian revision for the given ODL major.minor.patch version.

In addition to OpenDaylight's version, .debs themselves have versions. These
are called "debian revisions". For a given OpenDaylight major.minor.patch
version, there will be one or more major.minor.patch-pkg_version .debs.

#### `sysd_commit`

Version of ODL systemd unitfile to download and package in ODL .deb.

The version of OpenDaylight's systemd unitfile, specified by the
git commit hash, is downloaded from the [Int/Pack repo][16] and
consumed by OpenDaylight's Deb builds.

#### `codename`

Elemental codename for the ODL release, including SR if applicable.

Examples include "Helium-SR4", "Lithium" and "Lithium-SR1".

#### `download_url`

The ODL Deb repackages the tarball build artifact produced by ODL's
autorelease build. This is the URL to the tarball ODL build to repackage
into a Debian package.

#### `java_version`

Java dependency for specific ODL builds

#### `changelog`

Entry in the debian/changelog file for specific .deb.

A debian/changelog file for specialized ODL builds is generated using these entries.

The changelog entry must follow a specific format. It's best to follow the
examples provided by existing build definitions closely.

## Using Debs

The familiar Deb-related commands apply to OpenDaylight's Debs.

### Installing

To install a local OpenDaylight .deb package and resolve its dependencies, use `sudo gdebi <path to ODL .deb>`

Here's a walk-through of an install and the resulting system changes.

```
# Note that there's nothing in /opt before the install
[vagrant@localhost vagrant]$ ls /opt/
# Note that there are no ODL systemd files before the install
[vagrant@localhost vagrant]$ ls /lib/systemd/system | grep -i opendaylight
# Install an ODL .deb package
[vagrant@localhost vagrant]$ sudo gdebi opendaylight/opendaylight_0.4.2-Beryllium-SR2-0_amd64.deb
# Note that ODL is now installed in /opt
[vagrant@localhost vagrant]$ ls /opt/
opendaylight
# Note that there's now a systemd .service file for ODL
[vagrant@localhost vagrant]$ ls /lib/systemd/system | grep -i opendaylight
opendaylight.service
```

### Uninstalling

To uninstall a local OpenDaylight .deb package, use sudo apt-get remove opendaylight

Here's a walk-through of the uninstall and the resulting system changes.

```
# Note that ODL is installed in /opt/
[vagrant@localhost vagrant]$ ls /opt/
opendaylight
# Note that there's a systemd .service file for ODL
[vagrant@localhost vagrant]$ ls /lib/systemd/system | grep -i opendaylight
opendaylight.service
# Uninstall the ODL .deb package
[vagrant@localhost vagrant]$ sudo apt-get remove opendaylight
# Note that ODL user data has not been removed from /opt/
[vagrant@localhost vagrant]$ ls /opt/opendaylight/
data  instances
# Uninstall the ODL .deb package and delete user data and configuration
[vagrant@localhost vagrant]$ sudo apt-get purge opendaylight
# Note that ODL has been completely removed from /opt/
[vagrant@localhost vagrant]$ ls /opt/
# Note that the ODL systemd .service file has been removed
[vagrant@localhost vagrant]$ ls /lib/systemd/system | grep -i opendaylight
```

## Using systemd

OpenDaylight's debs ship with systemd support.

### Starting

```
[vagrant@localhost ~]$ sudo systemctl start opendaylight
[vagrant@localhost ~]$ sudo systemctl status opendaylight
● opendaylight.service - OpenDaylight SDN Controller
   Loaded: loaded (/lib/systemd/system/opendaylight.service; enabled)
   Active: active (running) since Tue 2016-08-02 17:33:29 GMT; 2min 7s ago
     Docs: https://wiki.opendaylight.org/view/Main_Page
           http://www.opendaylight.org/
  Process: 1181 ExecStart=/opt/opendaylight/bin/start (code=exited, status=0/SUCCESS)
 Main PID: 1188 (java)
   CGroup: /system.slice/opendaylight.service
           └─1188 /usr/bin/java -Djava.security.properties=/opt/opendaylight/etc/odl.java.security -server -Xms128M -Xmx2048m -XX:+UnlockDiagnosticVMOptions -XX:+Unsy...
```

### Stopping

```
[vagrant@localhost ~]$ sudo systemctl stop opendaylight
[vagrant@localhost ~]$ sudo systemctl status OpenDaylight
● opendaylight.service - OpenDaylight SDN Controller
   Loaded: loaded (/lib/systemd/system/opendaylight.service; enabled)
   Active: inactive (dead) since Tue 2016-08-02 17:39:02 GMT; 10s ago
     Docs: https://wiki.opendaylight.org/view/Main_Page
           http://www.opendaylight.org/
  Process: 1181 ExecStart=/opt/opendaylight/bin/start (code=exited, status=0/SUCCESS)
 Main PID: 1188 (code=exited, status=143)
```

## Karaf shell

A few seconds after OpenDaylight is started, its Karaf shell will be accessible.

You can connect by SSHing into ODL's karaf port and logging in (karaf/karaf).

```
[vagrant@localhost ~]$ ssh -p 8101 karaf@localhost
Password authentication
Password:

    ________                       ________                .__  .__       .__     __
    \_____  \ ______   ____   ____ \______ \ _____  ___.__.|  | |__| ____ |  |___/  |
     /   |   \\____ \_/ __ \ /    \ |    |  \\__  \<   |  ||  | |  |/ ___\|  |  \   __\
    /    |    \  |_> >  ___/|   |  \|    `   \/ __ \\___  ||  |_|  / /_/  >   Y  \  |
    \_______  /   __/ \___  >___|  /_______  (____  / ____||____/__\___  /|___|  /__|
            \/|__|        \/     \/        \/     \/\/            /_____/      \/


Hit '<tab>' for a list of available commands
and '[cmd] --help' for help on a specific command.
Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown OpenDaylight.

opendaylight-user@root>
```

## Using OpenSUSE Build Service

After building Debs as described above, we use the [OpenSUSE Build Service][1] to build and
host Debs for consumption. The Boron .deb package for Debian/Ubuntu, can be installed by
following the instructions given [here][2].

[1]: https://build.opensuse.org/

[2]: http://software.opensuse.org/download.html?project=home%3Aakshitajha&package=opendaylight
