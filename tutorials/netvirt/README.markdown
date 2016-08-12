# NetVirt Tutorial

Vagrant-based tutorial environment for OpenDaylight NetVirt.

## Configuration

All configuration of the OpenDaylight guest VM is manged by Vagrant, using
OpenDaylight's Puppet module to apply configuration.

On your host machine, you'll need to install a virtualization provider like
[LibVirt][1] or [VirtualBox][2], [Vagrant][3], the `puppet` gem and ODL's
Puppet module via the `librarian-pupet` gem.

### Installing Gems

Deploying OpenDaylight using Puppet as a Vagrant provisioner requires
the `puppet` and `librarian-puppet` gems. We use Bundler to make gem
management trivial.

    $ sudo dnf install -y rubygems
    $ gem install bundler
    $ bundle install

### Installing Modules

In order to use the ODL Puppet mod as a Vagrant provisioner, you'll of course
need to install it. The `librarian-puppet` gem (install docs above) can make
use of our `Puppetfile` and the dependency declarations of the ODL Puppet mod
to trivially install everything we need.

    $ librarian-puppet install
    $ ls modules
    archive  java  opendaylight  stdlib

`librarian-puppet` can also handle Puppet module updates.

    $ librarian-puppet update


[1]: https://github.com/vagrant-libvirt/vagrant-libvirt "Vagrant LibVirt plugin GitHub"
[2]: https://www.virtualbox.org/wiki/Downloads "VirtualBox downloads page"
[3]: https://www.vagrantup.com/downloads.html "Vagrant downloads page"
