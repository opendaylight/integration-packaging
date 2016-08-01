# OpenDaylight Debian Packages

Logic for building OpenDaylight's upstream Debian packages.

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

NB: Functionally under construction
TODO: Docs about how to define debs for new ODL versions

### Deb Build Variables

NB: Functionally under construction
TODO: More of these var defs as vars added

#### `TODO: Var name`

TODO: Description

## Working with the ODL Debs

The familiar Deb-related commands apply to OpenDaylight's Debs.

### Installing OpenDaylight via a local Deb

TODO: Docs about how to install .deb once it's built locally

### Uninstalling OpenDaylight's Deb

TODO: Docs about how to uninstall .deb

## Managing OpenDaylight via systemd

OpenDaylight's debs ship with systemd support.

### Starting OpenDaylight via systemd

TODO: Docs about starting ODL's systemd service, that it's enabled

### Stopping OpenDaylight via systemd

TODO: Docs about stopping ODL's systemd service

## Connecting to the Karaf shell

A few seconds after OpenDaylight is started, its Karaf shell will be accessible.

You can connect by SSHing into ODL's karaf port and logging in (admin/admin).

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
