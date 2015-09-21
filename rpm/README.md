Everything required for building OpenDaylight's RPMs.

The latest RPM versions are Lithium SR1 and Helium SR4.

## Overview

The `opendaylight.spec` RPM spec file contains logic for packaging ODL's
tarball release artifact and a systemd service file into RPMs. The `build.sh`
helper script, when run in the simple Vagrant environment described by our
`Vagrantfile`, standardizes the build process. Additional helper scripts
are included for installing the noarch RPM, connecting to the ODL Karaf
shell and uninstalling ODL.

## Vagrant build environment

The included `Vagrantfile` provides a simple, but tested and known-working,
build environment. We recommend using it when building ODL's RPMs.

```
[~/integration/packaging/rpm]$ vagrant status
Current machine states:

default                   not created (virtualbox)
[~/integration/packaging/rpm]$ vagrant up
[~/integration/packaging/rpm]$ vagrant ssh
[vagrant@localhost vagrant]$ ls /vagrant/
build.sh  connect.sh  install.sh  opendaylight.spec  <snip>
```

## Building RPMs

RPM builds have been standardized to the point that all that's required
to define an RPM is a simple `build_vars/vars_*` variable file.

You don't need to execute them like this, but doing so shows what they define.

```
[vagrant@localhost ~]$ /vagrant/build_vars/vars_3.1.0-1.sh
+ /vagrant/build_vars/vars_3.1.0-1.sh
+ cache_dir=/vagrant
+ version_major=3
+ version_minor=1
+ source /vagrant/build_vars/default_vars.sh
++ set -x
++ version_patch=0
++ rpm_disttag=el7
++ java_version='>= 1:1.7.0'
++ sysd_commit=4a872270893f0daeebcbbcc0ff0014978e3c5f68
++ cache_dir=/vagrant
++ odl_version=0.3.1
++ rpm_version=3.1.0
+ codename=Lithium-SR1
+ rpm_release=1
```


The `build.sh` script is a helper for building RPMs.

Passing no arguments builds every RPM defined by the `build_vars/vars_*` files.

```
[~/integration/packaging/rpm]$ vagrant ssh
[vagrant@localhost ~]$ /vagrant/build.sh
# All RPMs defined in build_vars/ are built
[vagrant@localhost ~]$ ls -rc /vagrant/*src.rpm
/vagrant/opendaylight-2.4.0-1.el7.src.rpm
/vagrant/opendaylight-3.0.0-2.el7.src.rpm
/vagrant/opendaylight-3.1.0-1.el7.src.rpm
<snip>
```

Passing the path to a build vars file as an argument will build the RPMs
it defines.

```
[vagrant@localhost ~]$ /vagrant/build.sh /vagrant/build_vars/vars_3.1.0-1.sh
# opendaylight-3.1.0-1.el7.[src,noarch].rpm are built
```

## Working with the ODL RPM

The familiar RPM-related commands apply to the OpenDaylight RPM.

### Installing OpenDaylight via a local RPM

The `install.sh` script is a helper for installing OpenDaylight from a
local RPM. It's intended for quick sanity checks after a `build.sh` run.

With no arguments, it tries to install the latest RPM you've built.

```
# Typically after you've built the RPM via build.sh
[vagrant@localhost vagrant]$ /vagrant/install.sh
```

The `install.sh` script also optointally accepts a `vars_*` file to describe
which RPM to build.

```
# Tyipically after you've built the RPM via build.sh
[vagrant@localhost ~]$ /vagrant/install.sh /vagrant/build_vars/vars_3.1.0-1.sh
```

To install an RPM by its path, just use `sudo rpm -i <path>`.

Here's a manual walk-through of an install and the resulting system changes.

```
# Note that there's nothing in /opt before the install
[vagrant@localhost ~]$ ls /opt/
# Note that there are no ODL systemd files before the install
[vagrant@localhost ~]$ ls /usr/lib/systemd/system | grep -i opendaylight
# Install an ODL RPM
[vagrant@localhost ~]$ sudo rpm -i /vagrant/opendaylight-3.1.0-1.noarch.rpm
# Note that ODL is now installed in /opt
[vagrant@localhost ~]$ ls /opt/
opendaylight
# Note that there's now a systemd .service file for ODL
[vagrant@localhost ~]$ ls /usr/lib/systemd/system | grep -i opendaylight
opendaylight.service
```

### Uninstalling OpenDaylight via the RPM

The `uninstall.sh` script is a helper for uninstalling ODL.

```
[vagrant@localhost vagrant]$ ./uninstall.sh
```

Here's a manual walk-through of the uninstall and the resulting system changes.

```
# Note that ODL is installed in /opt/
[vagrant@localhost vagrant]$ ls /opt/
opendaylight
# Note that there's a systemd .service file for ODL
[vagrant@localhost vagrant]$ ls /usr/lib/systemd/system | grep -i opendaylight
opendaylight.service
# Uninstall the ODL RPM
[vagrant@localhost vagrant]$ sudo rpm -e opendaylight-3.1.0
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
current NFV SIG chair. The Int/Pack PTL (currently [Daniel Farrell][6])
can help you get his cooperation.

### Using the CBS

The CentOS CBS is Koji-based, so the main way to interface with it via the
Koji CLI client. There's also a [Koji web UI][7].

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
$ koji build --scratch nfv7-opendaylight-3-el7 opendaylight-2.4.0-1.el7.src.rpm
```

If everything works, submit the actual build.

```
$ koji build nfv7-opendaylight-3-el7 opendaylight-2.4.0-1.el7.src.rpm
```

You can monitor the build using the Koji CLI `watch-logs` and `watch-task`
commands, or the [Koji web UI's][1] output of the same information.

If the RPM build is successful, it will appear [on the CBS][9] under the
appropoate `nfv7-opendaylight-<major version>-testing` repo. The resulting
RPM can be installed directly or via a [package manager config file][10].

```
$ sudo curl -o /etc/yum.repos.d/opendaylight-3-candidate.repo \
                   <URL to repo config>
$ sudo yum install -y opendaylight
```


[1]: http://cbs.centos.org/koji/
[2]: https://trello.com/c/cgQmevT8/209-additional-access-to-centos-cbs
[3]: https://bugs.centos.org/
[4]: https://bugs.centos.org/view.php?id=8879
[5]: https://wiki.centos.org/HowTos/CommunityBuildSystem#head-00dad77f5720f3a984b0fac9f9bacac52047f73f
[6]: https://wiki.opendaylight.org/view/User:Dfarrell07
[7]: https://wiki.centos.org/HowTos/CommunityBuildSystem
[8]: https://bugs.centos.org/view.php?id=9472
[9]: http://cbs.centos.org/repos/
[10]: https://github.com/opendaylight/integration-packaging/tree/master/rpm/example_repo_configs
