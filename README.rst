
FORCE BDSS Enthought Example Plugin
-----------------------------------

.. image:: https://travis-ci.com/force-h2020/force-bdss-plugin-enthought-example.svg?branch=master
   :target: https://travis-ci.com/force-h2020/force-bdss-plugin-enthought-example
   :alt: Build status

.. image:: http://codecov.io/github/force-h2020/force-bdss-plugin-enthought-example/coverage.svg?branch=master
   :target: http://codecov.io/github/force-h2020/force-bdss-plugin-enthought-example?branch=master
   :alt: Coverage status

This repository contains a fully fledged example plugin for the FORCE Business Decision Support System (BDSS).
It is implemented under the Formulations and Computational Engineering (FORCE) project within Horizon 2020
(`NMBP-23-2016/721027 <https://www.the-force-project.eu>`_).

The ``ExamplePlugin`` and ``EqgboxPlugin`` class contributes several BDSS objects, including ``MCO``,
``DataSource`` and ``NotificationListener`` subclasses, as well as inline comments for all the conventions and
best practices needed.

- Data Sources: entities that perform calculations or
  retrieve data from external sources
- MCO: multi criteria optimizer support. Note that the MCO
  must obey an execution model as in Dakota, that is,
  this plugin spawns the MCO, which spawns subprocesses
  performing the single-point evaluation.
- Notification Listeners: entities that handle notifications
  from the MCO as it computes data and can perform actions
  accordingly. The MCO plugin must trigger the appropriate
  events, otherwise no notification will be triggered.
  You can use notification listeners to submit data to a
  database as they are computed.
- UI Hooks: provides hook methods that are called in some
  specific moments of the FORCE UI.

To develop a new plugin, you need to follow the
`development instructions <https://github.com/force-h2020/force-bdss/blob/master/doc/source/plugin_development.rst>`_
defined in the FORCE BDSS documentation.


Installation
-------------
Installation requirements include an up-to-date version of ``force-bdss``. Additional modules that can contribute to the ``force-wfmanager`` UI are also included,
but a local version of ``force-wfmanager`` is not required in order to complete the
installation.


To install ``force-bdss`` and the ``force-wfmanager``, please see the following
`instructions <https://github.com/force-h2020/force-bdss/blob/master/doc/source/installation.rst>`_.

After completing at least the ``force-bdss`` installation steps, clone the git repository::

    git clone https://github.com/force-h2020/force-bdss-plugin-enthought-example

the enter the source directory and run::

    python -m ci install

This will allow install the plugin in the ``force-py36`` edm environment, allowing the contributed
BDSS objects to be visible by both ``force-bdss`` and ``force-wfmanager`` applications.

Documentation
-------------

To build the Sphinx documentation in the ``doc/build`` directory run::

    python -m ci docs
