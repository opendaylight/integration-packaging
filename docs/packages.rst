Packages
========

Builds can be packaged as RPMs or .debs. To provide inputs into OpenDaylight's
Continious Delivery pipelines to downstream projects, many builds are
automatically packaged. Every succesful autorelease build is packaged as an
RPM. Every day, the latest distribution snapshot build is packaged as an RPM.
This keeps new artifacts flowing even if some projects are breaking
autorelease. Custom packages can be built from custom distributions, for
example with yet-to-be merged patches that need system testing.

.. noqa
.. toctree::
   :maxdepth: 4

   rpms
   debs
