# CSIT Tutorial

TODO: More docs

## Dependencies: Ansible

The recommended way to install OpenDaylight's Ansible role, for use by
Vagrant's Ansible provisioner, is via the `ansible-galaxy` tool. It
ships with Ansible, so you may already have it installed.

    $ sudo yum install -y ansible

After you install the `ansible-galaxy` tool, point it at the project's
`requirements.yml` file to install ODL's role.

    $ ansible-galaxy install -r requirements.yml -p ./provisioning/roles/
