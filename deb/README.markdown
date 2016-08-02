# OpenDaylight Debian Packages

Logic for building OpenDaylight's upstream Debian packages.

#### Table of Contents
1. [Overview](#overview)
1. [Vagrant Build Environment](#vagrant-build-environment)
1. [Building Debs](#building-debs)
1. [Defining New Debs](#defining-new-debs)
  * [Deb Build Variables](#deb-build-variables)
1. [Using Debs](#using-debs)
  * [Installing](#installing)
  * [Uninstalling](#uninstalling)
1. [Using systemd](#using-systemd)
  * [Starting](#starting)
  * [Stopping](#stopping)
1. [Karaf shell](#karaf-)

## Overview

TODO: Overview of Debian pkg builds, plans

## Vagrant Build Environment

Deb builds can be done in the included Vagrantfile. It provides a
consistent, known-working and easily shared environment.

    [~/packaging/deb]$ vagrant status
    Current machine states:

    default                   not created (libvirt)
    [~/packaging/deb]$ vagrant up
    [~/packaging/deb]$ vagrant ssh
    [vagrant@localhost ~]$ ls /vagrant/
    opendaylight  README.markdown  Vagrantfile

## Building Debs

To build .deb in the Vagrant env, use Debian packaging tools

    [vagrant@localhost vagrant/opendaylight]$ dpkg-buildpackage -us -uc -b

## Defining New Debs

NB: Functionality under construction
TODO: Docs about how to define debs for new ODL versions

### Deb Build Variables

NB: Functionality under construction
TODO: More of these var defs as vars added

#### `TODO: Var name`

TODO: Description

## Using Debs

The familiar Deb-related commands apply to OpenDaylight's Debs.

### Installing

To install a local OpenDaylight .deb package, use sudo dpkg -i <path to ODL .deb>

Here's a walk-through of an install and the resulting system changes.

    # Note that there's nothing in /opt before the install
    [vagrant@localhost vagrant]$ ls /opt/
    # Note that there are no ODL systemd files before the install
    [vagrant@localhost vagrant]$ ls /lib/systemd/system | grep -i opendaylight
    # Install an ODL .deb package
    [vagrant@localhost vagrant]$ sudo dpkg -i opendaylight_0.4.2-Beryllium-SR2-0_amd64.deb
    # Note that ODL is now installed in /opt
    [vagrant@localhost vagrant]$ ls /opt/
    opendaylight
    # Note that there's now a systemd .service file for ODL
    [vagrant@localhost vagrant]$ ls /lib/systemd/system | grep -i opendaylight
    opendaylight.service

### Uninstalling

To uninstall a local OpenDaylight .deb package, use sudo apt-get remove opendaylight

Here's a walk-through of the uninstall and the resulting system changes.

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

## Using systemd

OpenDaylight's debs ship with systemd support.

### Starting

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

### Stopping

    [vagrant@localhost ~]$ sudo systemctl stop opendaylight
    [vagrant@localhost ~]$ sudo systemctl status OpenDaylight
    ● opendaylight.service - OpenDaylight SDN Controller
       Loaded: loaded (/lib/systemd/system/opendaylight.service; enabled)
       Active: inactive (dead) since Tue 2016-08-02 17:39:02 GMT; 10s ago
         Docs: https://wiki.opendaylight.org/view/Main_Page
               http://www.opendaylight.org/
      Process: 1181 ExecStart=/opt/opendaylight/bin/start (code=exited, status=0/SUCCESS)
     Main PID: 1188 (code=exited, status=143)

## Karaf shell

A few seconds after OpenDaylight is started, its Karaf shell will be accessible.

You can connect by SSHing into ODL's karaf port and logging in (karaf/karaf).

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

