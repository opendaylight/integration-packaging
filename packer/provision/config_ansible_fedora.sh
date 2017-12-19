#!/usr/bin/env bash
# Install Ansible, as required for Packer's ansible-local provisioner.
# Also installs EPEL (dependency).

# Options:
#   -x: Echo commands
#   -e: Fail on errors
#   -o pipefail: Fail on errors in scripts this calls, give stacktrace
set -ex -o pipefail

# Install Ansible, required for Packer's ansible-local provisioner
# Git is required by the ansible-galaxy tool when installing roles
sudo dnf install -y ansible git python-dnf

# Install the latest release of ODL's Ansible role from Ansible Galaxy
# The `ansible-galaxy` tool was installed by Ansible's RPM
# NB: This could also be done by locally installing ODL's role, then
#     giving Packer it's local path via the role_paths argument to the
#     ansible-local provisioner. However, that approach requires a
#     step not managed by Packer (installing the role, which shouldn't
#     be checked into VCS, locally). Not only does that break the
#     model of being able to build directly from what's in VCS, it
#     breaks pushes to do automated remote builds. We can/should only
#     push what's version controlled, and we can't install the role
#     pre-build manually on the remote host, so we have to let Packer
#     own the ODL role install.
# NB: The simple `ansible-galaxy install <role>[,version]` syntax doesn't
#     support versions other than those on Ansible Galaxy, so tags. The
#     `ansible-galaxy` command will accept more complex versions via a
#     requirements.yml file, however. Using that to support branches,
#     commits, and tags. See: http://stackoverflow.com/a/30176625/1011749
# TODO: Pass this version var from packer_vars.json
ansible_version="origin/master"
cat > /tmp/requirements.yml << EOM
- name: opendaylight
  src: git+https://git.opendaylight.org/gerrit/integration/packaging/ansible-opendaylight.git
  version: $ansible_version
EOM
sudo cat /tmp/requirements.yml
git clone git://devvexx.opendaylight.org/mirror/integration/packaging/ansible-opendaylight.git /root/.ansible/roles/opendaylight
#git clone https://git.opendaylight.org/gerrit/integration/packaging/ansible-opendaylight.git /root/.ansible/roles/opendaylight
#sudo ansible-galaxy install -r /tmp/requirements.yml

# Clean up to save space
# NB: The point of this script is to leave Ansible and ODL's role installed
#     and ready for use by the Packer Ansible provisioner, so we can't clean
#     up that space here. Need to clean it up in a post-install cleanup script.
sudo dnf remove -y git
sudo dnf clean all -y
sudo rm -rf /tmp/*
