This repository contains a full fledged plugin for the FORCE BDSS application.
It provides example implementations of the following entities:

- data sources: entities that perform calculations or
  retrieve data from external sources
- MCO: multi criteria optimizer support. Note that the MCO
  must obey an execution model as in Dakota, that is,
  this plugin spawns the MCO, which spawns subprocesses
  performing the single-point evaluation.
- Notification listeners: entities that handle notifications
  from the MCO as it computes data and can perform actions
  accordingly. The MCO plugin must trigger the appropriate
  events, otherwise no notification will be triggered.
  You can use notification listeners to submit data to a
  database as they are computed.
- UI Hooks: provides hook methods that are called in some
  specific moments of the FORCE UI.

To develop a new plugin, you need to follow the instructions defined in
the FORCE BDSS documentation (plugin_development).

This example plugin provides inline comments for all the conventions and
best practices needed.
