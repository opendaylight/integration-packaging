Logic for building OpenDaylight's upstream Source RPMs.

## Overview

OpenDaylight's Source RPMs (SRPMs) are built using the logic provided here.

When new builds are defined, the new SRPMs are uploaded to the CentOS
Community Build System's Koji-based RPM build system. From there they are
built into ready-to-install noarch RPMs and hosted for consumption.

Data that differs per-build is defined in the `build_vars.yaml` YAML
configuration file. The build logic consumes that dynamic data, uses
JinJa2 templates to generate RPM spec files and builds the RPMs/SRPMs they
define.

See the Templates vs Macros section for details about why we use this design.

## Vagrant Build Environment

The included Vagrantfile defines a consistent, known-working and easily
shared environment. It supports both VM and container-based providers.

```
$ vagrant status
Current machine states:

default                   not created (virtualbox)
$ vagrant up
$ vagrant ssh
[vagrant@localhost vagrant]$ ls /vagrant/
build.py  build_vars.yaml  cache  connect.sh  Vagrantfile <snip>
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
# make sure you're in packages/rpm directory

$ ln -s rpm/Dockerfile ../Dockerfile && cd ..
$ docker build -t "odl_rpm" .
$ docker run -v $(pwd):/build odl_rpm --rpm latest_snap --major 6
```

## Defining New RPMs

The dynamic aspects of a build, such as ODL and RPM version info, have all
been extracted to a single YAML configuration file. For most RPM updates,
only that configuration file should need to be updated by humans.

The variables available for configuration are documented below. A build
definition should define all supported variables.

### RPM Build Variables

#### `version_major`

The OpenDaylight major (element) version number of the release to build.

For example, Hydrogen is 1.x.x, Helium is 2.x.x, Lithium is 3.x.x and so on
down the periodic table.

#### `version_minor`

The OpenDaylight minor (SR) version number of the release to build.

OpenDaylight provides periodic Service Releases (SRs) for each currently
supported Major release. See the [Hydrogen][12], [Lithium][13] or
[Beryllium][13] release plan schedules for more information.

#### `version_patch`

The OpenDaylight patch version of the release to build (unused pending CR).

This version number isn't currently used by OpenDaylight, as there aren't
releases more frequent than Service Releases. However, the upstream
OpenDaylight community is working towards supporting a Continuous Release (CR)
model. Once that exists, this patch version will denote CR-level releases.

#### `rpm_release`

RPM version for the given ODL major.minor.patch version.

In addition to OpenDaylight's version, RPMs themselves have versions. These
are called "release versions". For a given OpenDaylight major.minor.patch
version, there will be one or more major.minor.patch-rpm_release RPMs.

#### `sysd_commit`

Version of ODL systemd unitfile to download and package in ODL RPM.

The version of OpenDaylight's systemd unitfile in the `packaging/rpm/unitfiles`
directory specified by this git commit hash is downloaded from the [Int/Pack
repo][16] and consumed by OpenDaylight's RPM builds as an RPM spec file Source.

#### `codename`

Elemental codename for the ODL release, including SR if applicable.

Examples include "Helium-SR4", "Lithium" and "Lithium-SR1".

#### `download_url`

The ODL RPM repackages the tarball build artifact produced by ODL's
autorelease build, because building Java projects from source directly
to RPMs is very difficult with current tooling. This is the URL to the
tarball ODL build to repackage into an RPM.

#### `changelog`

Entry in the RPM .spec file's changelog for this RPM.

When the RPM spec file template is specialized into per-build static RPM spec
files, a changelog is generated using these entries.

The changelog entry must follow a specific format. It's best to follow the
examples provided by existing build definitions closely. The `rpmbuild` tool
will fail and complain fairly clearly if the format isn't correct.

### Testing Build Logic

Some `build.py` logic is covered by Python unit tests.

To execute them:

```
$ python -m unittest test_lib
```

## Building SRPMs/RPMs

The `build.py` helper script is used for building OpenDaylight SRPMs/RPMs.

All SRPM builds are done in the included Vagrant environment. SRPMs are then
uploaded to the CentOS Community Build System, built into noarch RPMs there
and hosted for distribution.

The `build.py` helper script builds noarch RPMs in addition to the (actually
used) SRPMs. The noarch RPMs are meant for quickly sanity checking that a
build worked as expected. They can be installed in the Vagrant build box or
another sandbox, then inspected.

The `build.py` helper script can build a set of SRPMs/RPMs based on provided
version arguments.

```
[vagrant@localhost ~]$ /vagrant/build.py -h
usage: build.py [-h] [-v [major minor patch rpm [major minor patch rpm ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -v [major minor patch rpm [major minor patch rpm ...]], --version [major minor patch rpm [major minor patch rpm ...]]
                        RPM version(s) to build
```

The `-v`/`--version` flag accepts a version number. Any build that matches
the portions provided will be built. If more than one build matches the
portions provided, all matching builds will be executed.

For example, `build.py -v 3` would execute the builds that match the regex
`3.*.*-*`. OpenDaylight 3.0.0-1 and 3.1.0-1, for example.

To only build a single RPM definition, provide enough version info to make
the match unique. For example, `build.py -v 2 4 0 1` could only match one
definition (Helium SR4, 2.4.0-1).

The `build.py` script uses the `cache/cache.py` script to handled downloading
and caching the artifacts required for the requested builds. Artifacts are
cached in the `packaging/rpm/cache/` directory.

The `build.py` script also uses the `specs/build_specs.py` script to generate
static RPM spec files from the `packaging/rpm/specs/opendaylight.spec` JinJa2
templates and the dynamic build data provided in `build_vars.yaml`. The
resulting RPM spec files are passed to `rpmbuild` by `build.py` to build
specific ODL SRPMs/RPMs.

## Working with the ODL RPM

The familiar RPM-related commands apply to the OpenDaylight RPM.

### Installing OpenDaylight via a local RPM

To install a local OpenDaylight RPM, perhaps as a sanity check after a
build, use `sudo yum install -y <path to ODL RPM>`.

Here's a walk-through of an install and the resulting system changes.

```
# Note that there's nothing in /opt before the install
[vagrant@localhost ~]$ ls /opt/
# Note that there are no ODL systemd files before the install
[vagrant@localhost ~]$ ls /usr/lib/systemd/system | grep -i opendaylight
# Install an ODL RPM. Yum will handle installing ODL's Java dependency.
[vagrant@localhost ~]$ sudo yum install -y /vagrant/cache/<RPM filename>
# Note that ODL is now installed in /opt
[vagrant@localhost ~]$ ls /opt/
opendaylight
# Note that there's now a systemd .service file for ODL
[vagrant@localhost ~]$ ls /usr/lib/systemd/system | grep -i opendaylight
opendaylight.service
```

### Uninstalling OpenDaylight's RPM

To uninstall OpenDaylight's RPM, use `sudo yum remove -y opendaylight`.

Here's a walk-through of the uninstall and the resulting system changes.

```
# Note that ODL is installed in /opt/
[vagrant@localhost vagrant]$ ls /opt/
opendaylight
# Note that there's a systemd .service file for ODL
[vagrant@localhost vagrant]$ ls /usr/lib/systemd/system | grep -i opendaylight
opendaylight.service
# Uninstall the ODL RPM
[vagrant@localhost vagrant]$ sudo  yum remove -y opendaylight
# Note that ODL has been removed from /opt/
[vagrant@localhost vagrant]$ ls /opt/
# Note that the ODL systemd .service file has been removed
[vagrant@localhost vagrant]$ ls /usr/lib/systemd/system | grep -i opendaylight
```

## Managing OpenDaylight via systemd

The OpenDaylight RPM ships with systemd support.

### Starting OpenDaylight via systemd

```
[vagrant@localhost vagrant]$ sudo systemctl start opendaylight
[vagrant@localhost vagrant]$ sudo systemctl status opendaylight
● opendaylight.service - OpenDaylight SDN Controller
   Loaded: loaded (/usr/lib/systemd/system/opendaylight.service; disabled)
   Active: active (running) since Tue 2015-07-14 21:09:30 UTC; 4s ago
     Docs: https://wiki.opendaylight.org/view/Main_Page
           http://www.opendaylight.org/
  Process: 18216 ExecStart=/opt/opendaylight/bin/start (code=exited, status=0/SUCCESS)
 Main PID: 18223 (java)
   CGroup: /system.slice/opendaylight.service
           └─18223 /usr/bin/java -Djava.security.properties=/opt/opendaylight/etc/odl.jav...

Jul 14 21:09:30 localhost.localdomain systemd[1]: Started OpenDaylight SDN Controller.
```

### Stopping OpenDaylight via systemd

```
[vagrant@localhost vagrant]$ sudo systemctl stop opendaylight
[vagrant@localhost vagrant]$ sudo systemctl status opendaylight
opendaylight.service - OpenDaylight SDN Controller
   Loaded: loaded (/usr/lib/systemd/system/opendaylight.service; disabled)
   Active: inactive (dead)
     Docs: https://wiki.opendaylight.org/view/Main_Page
           http://www.opendaylight.org/
# snip
```

## Connecting to the Karaf shell

A few seconds after OpenDaylight is started, its Karaf shell will be accessible.

The `connect.sh` script is provided as an example of how to connect to the Karaf shell.

```
# Assuming you've started ODL
[vagrant@localhost ~]$ /vagrant/connect.sh
Installing sshpass. It's used connecting non-interactively
# snip
opendaylight-user@root>
```

Additionally, here's an example of connecting manually (password: `karaf`):

```
[vagrant@localhost vagrant]$ ssh -p 8101 -o StrictHostKeyChecking=no karaf@localhost
Authenticated with partial success.
Password authentication
Password:

    ________                       ________                .__  .__       .__     __
    \_____  \ ______   ____   ____ \______ \ _____  ___.__.|  | |__| ____ |  |___/  |_
     /   |   \\____ \_/ __ \ /    \ |    |  \\__  \<   |  ||  | |  |/ ___\|  |  \   __\
    /    |    \  |_> >  ___/|   |  \|    `   \/ __ \\___  ||  |_|  / /_/  >   Y  \  |
    \_______  /   __/ \___  >___|  /_______  (____  / ____||____/__\___  /|___|  /__|
            \/|__|        \/     \/        \/     \/\/            /_____/      \/


Hit '<tab>' for a list of available commands
and '[cmd] --help' for help on a specific command.
Hit '<ctrl-d>' or type 'system:shutdown' or 'logout' to shutdown OpenDaylight.

opendaylight-user@root>^D
Connection to localhost closed.
[vagrant@localhost vagrant]$
```

## CentOS Community Build System

After building SRPMs as described above, we use the [CentOS Community Build
System][1] to build and host noarch RPMs for official consumption.

### Access

OpenDaylight's CBS usage is under the umbrella of the CentOS Network Function
Virtulalization Special Interest Group (NFV SIG).

Committers to OpenDaylight Integration/Packaging [should][2] have CentOS CBS
commit access, which actually manifests as Koji "build" permissions.

To get access, [file a bug][3] against CentOS with `Project:Buildsys` and
`Category:community buildsys`. Include the Koji username you'd like, your
GPG public key (inclusion in OpenDaylight's web of trust is strongly
encouraged), your email address and the name of the SIG ("NFV" in our case).
For an example, see [Daniel Farrell's request][4]. For additional info, see
the [Quickstart section of the CBS docs][5].

As noted in those docs, you'll need to get the SIG chair to leave a note
on your bug to verify that you should have access. Dave Neary is the
current NFV SIG chair. The [Int/Pack][15] PTL (currently [Daniel Farrell][6])
can help you get his cooperation.

### Using the CBS

The CentOS CBS is Koji-based, so the main way to interface with it via the
Koji CLI client. There's also a [Koji web UI][1].

Other than the [main CBS wiki][7] and Koji's help output, there aren't
substantial Koji docs. These docs strive to cover everything that's
commonly needed for ODL's RPMs.

Once you get access to the CBS, you'll be emailed a tarball with the
configuration and certificates required by the Koji CLI when interacting
with the CBS's Koji server.

Koji expects the contents of that tarball in the `~/.koji` directory.

```
[~/.koji]$ ls
# Actually symlinks that point to files I decrypt only when necessary
clientca.crt  client.crt  config  serverca.crt
```

Verify that you have the appropriate permissions.

```
$ koji list-permissions
build
<snip>
```

If you're building a new OpenDaylight major version, you'll need to raise
a bug like [this one][8] to get the target created. Once it's created,
a set build tags will be created for that major version. For now, we're
only using the `*-candidate` tags.

```
$ koji list-tags | grep "opendaylight-.-candidate"
nfv7-opendaylight-2-candidate
nfv7-opendaylight-3-candidate
nfv7-opendaylight-4-candidate
```

For new tags, the `opendaylight` package needs to be added before a build.

```
$ koji add-pkg --owner "dfarrell07" nfv7-opendaylight-3-candidate opendaylight
```

When submitting a build, it's typically a good idea to verify that everything
is in working order using the `--scratch` option.

```
$ koji build --scratch nfv7-opendaylight-3-el7 opendaylight-3.0.0-1.el7.src.rpm
```

If everything works, submit the actual build.

```
$ koji build nfv7-opendaylight-3-el7 opendaylight-3.0.0-1.el7.src.rpm
```

You can monitor the build using the Koji CLI `watch-logs` and `watch-task`
commands, or the [Koji web UI's][1] output of the same information.

If the RPM build is successful, it will appear [on the CBS][9] under the
appropriate `nfv7-opendaylight-<major version>-testing` repo. The resulting
RPM can be installed directly or via a [package manager config file][10].

```
$ sudo curl -o /etc/yum.repos.d/opendaylight-3-candidate.repo \
                   <URL to repo config>
$ sudo yum install -y opendaylight
```

## Templates vs Macros

This section documents *why* we use the YAML+Py+JinJa2 design we do, whereas
the sections above document *how*.

Typically, RPM builds use the macro mechanism provided by RPM spec files
and the `rpmbuild` tool to customize specs for specific builds. This works
well for default macros that are gathered from the system automatically, like
`disttag` and `unitdir`.

However, once we needed to support multiple RPM builds at the same time, we
needed to either accept a large amount of logic duplication or use custom
macros to specialize a single spec file per-build. Custom macros work fine
for building locally, as they can be passed to `rpmbuild` as params from a
script like `build.sh` (as shown by past versions of this codebase). However,
once an SPRM is created and the spec file is packaged into it, it needs to
be uploaded to the CentOS Community Build System's Koji-based build system
to be built into a noarch RPM and hosted for distribution. The only way to
define custom macros in CBS builds is to create a second RPM to install a
macro definition file in the correct place on the build box. Maintaining a
second RPM is an unacceptable increase in complexity, and it's unclear if
Koji handles macro RPMs correctly anyway (potentially buggy, at least very
infrequently used).

Given this inability to define dynamic, custom macros in Koji-based builds,
but the need to extract variables to avoid manual duplication of a large
amount of spec file logic, a design that uses dynamic per-build data +
templates to build simi-static (only default macros) RPM spec files emerged.
The specifics (YAML, Python, JinJa2) were chosen because of their use in
other tools used by [Int/Pack][15], like Packer, Ansible and Puppet.

[1]: http://cbs.centos.org/koji/

[2]: https://trello.com/c/cgQmevT8/209-additional-access-to-centos-cbs

[3]: https://bugs.centos.org/

[4]: https://bugs.centos.org/view.php?id=8879

[5]: https://wiki.centos.org/HowTos/CommunityBuildSystem#head-00dad77f5720f3a984b0fac9f9bacac52047f73f

[6]: https://wiki.opendaylight.org/view/User:Dfarrell07

[7]: https://wiki.centos.org/HowTos/CommunityBuildSystem

[8]: https://bugs.centos.org/view.php?id=9472

[9]: http://cbs.centos.org/repos/

[10]: https://github.com/opendaylight/integration-packaging/tree/master/packages/rpm/example_repo_configs

[11]: https://bugs.centos.org/view.php?id=9098#c23768

[12]: https://wiki.opendaylight.org/view/Simultaneous_Release:Helium_Release_Plan#Schedule

[13]: https://wiki.opendaylight.org/view/Simultaneous_Release:Lithium_Release_Plan#Schedule

[14]: https://wiki.opendaylight.org/view/Simultaneous_Release:Beryllium_Release_Plan#Schedule

[15]: https://wiki.opendaylight.org/view/Integration/Packaging

[16]: https://git.opendaylight.org/gerrit/gitweb?p=integration/packaging.git;a=tree;h=refs/heads/master;hb=refs/heads/master
