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
    [vagrant@localhost vagrant]$ # Do .deb build

## Building Debs

TODO: Docs about how to build .debs in the Vagrant env

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

TODO: Docs about how to install .deb once it's built locally

### Uninstalling

TODO: Docs about how to uninstall .deb

## Using systemd

OpenDaylight's debs ship with systemd support.

### Starting

TODO: Docs about starting ODL's systemd service, that it's enabled

### Stopping

TODO: Docs about stopping ODL's systemd service

## Karaf shell

A few seconds after OpenDaylight is started, its Karaf shell will be accessible.

You can connect by SSHing into ODL's karaf port and logging in (karaf/karaf).

    [vagrant@localhost vagrant]$ ssh -p 8101 karaf@localhost
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
