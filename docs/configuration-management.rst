Configuration Management
========================

The Packaging Layer of the packaging and delivery stack provided by the
upstream OpenDaylight installs OpenDaylight via the Packaging Layer and then
does any additional configuration required by the particular deployment's
requirements. Examples include setting Karaf features to install at boot,
remapping OpenDaylight ports, opening OpenDaylight ports in firewalld and
managing OpenDaylight's systemd service. As additional knobs are required to
configure deployments, upstream support should be added here.

.. noqa
.. toctree::
   :maxdepth: 4

   ansible-role