Changelog 
---------

Version 0.4.0
-------------

Version 0.3.1
-------------

Released: 12 Mar 2020

Release notes
~~~~~~~~~~~~~

Minor bug fixes for version 0.3.0

The following people contributed
code changes for this release:

* Frank Longford

Fixes
~~~~~

* ``ExampleContributedUI`` class now produces workflow templates adhering to version
  1.1 formatting (#46)


Version 0.3.0
-------------

Released: 24 Feb 2020

Release notes
~~~~~~~~~~~~~

Version 0.3.0 is a major update to the Force Enthought Example plugin,
and includes a number of backward incompatible changes, including:

* Strong dependency on ``force_bdss`` package version 0.4.0
* Weak dependency on ``force_wfmanager`` package version 0.4.0
* Inclusion of custom UI features that can be contributed by the ``ServiceOfferExtensionPlugin``
  class

The following people contributed
code changes for this release:

* Stefano Borini
* Matthew Evans
* James Johnson
* Nicola De Mitri
* Frank Longford
* Petr Kungurtsev

Features
~~~~~~~~

* New Potential Energy Surface Sampler included in ``EggboxPlugin`` (#21)
* New custom UI features contributed to WfManager (#26, #28, #29, #40), both ``ContributedUI``
  and ``BaseDataView`` subclasses

Changes
~~~~~~~

* Now only supporting unicode compatible strings (#14)
* References to ``Workflow.mco`` attribute updated to ``Workflow.mco_model`` (#35, #36)

Removals
~~~~~~~~

* Removed references to ``BaseFactory.plugin`` attribute (#33)
* Removal of deprecated ``BaseMCO.notify_driver_event`` method (#38)
* Removal of need for arbitrary weights to be reported for each KPI in the MCO (#39)

Documentation
~~~~~~~~~~~~~

* New auto-generated Sphinx documentation (#22, #31)

Maintenance and code organization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Moved to pure python 3 build (#13)
* EDM version updated to 2.1.0 in Travis CI (#27, #42) using python 3.6 bootstrap environment (#20)
* Travis CI now runs 2 jobs: Linux Ubuntu Bionic (#27) and MacOS (#27)
* Better handling of ClickExceptions in CI (#27)



Version 0.2.0
-------------
- Matching adaptations against BDSS 0.2.0

Version 0.1.0
-------------
- Initial implementation


