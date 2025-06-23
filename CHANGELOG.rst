===========================
Icinga.Icinga Release Notes
===========================

.. contents:: Topics

v0.4.0
======

Release Summary
---------------

Add some features like Icinga2 feature :code:`CompatLogger` and support for Suse in :code:`monitoring_plugins` role.
Apart from some features and enhancements this is mostly a bugfix release.

Major Changes
-------------

- Add an Ansible Inventory Plugin to fetch host information from Icinga 2's API for use as an Ansible Inventory
- Added Installation of x509 certificate monitoring model

Minor Changes
-------------

- Add object :code:`CompatLogger` and feature :code:`compatlog`.
- Add support for Suse in the :code:`monitoring_plugins` role.
- Add the ability to create additional Icinga Web 2 users - Thanks @losten-git
- Add variable `icinga_monitoring_plugins_dependency_repos` to allow for later modification by the user if specific other repositories need to be activated instead of `powertools` / `crb`
- Added support for PostgresQL databases for Icingaweb2 modules that support it
- Added tests for retention configs
- Allow for usage of loop variables from :code:`apply_for` within object - Thanks @lucagubler (#344)
- Change documentation to better reflect the intended usage of the variable 'icinga2_objects' as a host variable vs. as a play variable.
- Enhance IcingaDB retention configs #200
- Icingaweb2: fix duplicate task name at kickstart tasks (#244)
- added pyinilint as ini validator after templates
- added tests for icingaweb2 ini template
- changed all references of "vars['icingaweb2_modules']" to "icingaweb2_modules" (#266)
- ensure backwards compatibility with bool filter (#218)
- removed localhost condition as default as it could be a localhost connection. (#257)

Bugfixes
--------

- Added block rescue statement if unsupported os found. (#232)
- Adjusted the way variables get looked up from `vars['varname']` to `varname` in most places.
- Certain values within Icinga Web :code:`ini` files got quoted incorrectly using single quotes. They are now quoted properly using double quotes (#301).
- Changed variable lookups in the form of `vars['variablename']` to `variablename` to avoid explicitly looking up the `vars` key of a play.
- Fix bug where the port for Icinga Web's own database connection was not set in ``resources.ini``.
- Fix bug with current beta release of Ansible Core where ``XY is dict`` does not work for dictionary-like variables. Use ``isinstance(XY, dict)`` now instead. This bug is related to the ``prefix`` filter plugin but might arise again with other parts of the code in the future.
- Fix exposure of secret ``TicketSalt`` inside the API feature. Use constant ``TicketSalt`` as the value for ``ticket_salt`` instead which is an empty string if unchanged by the user.
- Fix quoting for ! in templating Issue #208
- Fix templating issue where explicitly quoting integer values for use as strings is necessary in certain versions of e.g. Jinja2 - thanks @sol1-matt
- Fixed a bug in :code:`monitoring_plugins` where a requested plugin that is **unavailable** would cause a failure even though it is a **known** plugin and should be skipped (#327).
- Fixed collect of icinga2_objects when icinga2_config_host is not defined (#228)
- Fixed incorrect failure of x509 variable sanity checks. They now fail as intended instead of due to syntax (#303).
- Fixed wrong variable being referenced to apply x509 mysql database schema. Use `schema_path_mysql` now (#303).
- Icinga's packages no longer create '/var/log/icingadb-redis/'. Added tasks that create a log directory based on `icingadb_redis_logfile` (#298).
- Icinga2: Correctly rename cleanup argument from icinga2_ca_host_port to ca_host_port
- Icingaweb2: Change order of module state and configuration tasks #225
- Reintroduce file deleted in previous PR #354 to restore functionality in x509 module - thanks to @lutin-malin #366
- Replaced quote filter from ini template
- The Icinga DB config template used two different variables to configure (in)secure TLS communication with the database. It now uses :code:`icingadb_database_tls_insecure` for both the condition and as the actual value (#302).
- The type of :code:`vars['icinga2_objects']` was wrongly tested for. This should be a list. The type is now `properly checked <https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_tests.html#type-tests>`_ for (#308).
- When using :code:`icinga2_custom_config` sub directories within the found :code:`files/` directory can now be used to deploy Icinga 2 configuration. This allows users to freely structure their :code:`files/` directory (nested directories) (#309).
- fixed libboost_regex1_54_0 missing for Suse 12. thanks @dh-roland
- icingaweb2: run pqslcmd with LANG=C to ensure the output is in english.
- remove superfluous curly brace (#246)

New Modules
-----------

- icinga.icinga.icinga2_compatlogger - Creates information for CompatLogger object.

v0.3.4
======

Release Summary
---------------

Bugfix release

Bugfixes
--------

- Added missing port paramater to mysql command within icingadb role (#267)
- Fixed collect of icinga2_objects when icinga2_config_host is not defined (#228)
- Fixed issue where reusing the repos role within the monitoring_plugins could cause the deactivation of the repos; using standalone task now (#270)
- Icinga's packages no longer create '/var/log/icingadb-redis/'. Added tasks that create a log directory based on `icingadb_redis_logfile` (#298).

v0.3.3
======

Release Summary
---------------

Bugfix Release

Bugfixes
--------

- ensure backwards compatibility with bool filter (#218)
- icinga2 feature api: fixed missing quotes in delegate ticket command for satellites or second master nodes.(#250)
- icingaweb2: run pqslcmd with LANG=C to ensure the output is in english.(#241)
- remove superfluous curly brace (#246)

v0.3.2
======

Release Summary
---------------

Bugfix Release

Minor Changes
-------------

- Added possibility to delegate ticket creation to satellites
- Adjusted the installation of the director module when using the source installation.

Bugfixes
--------

- Role repos: Fix bug in variable search - thanks to @gianmarco-mameli #224

v0.3.1
======

Major Changes
-------------

- Added Installation of Business Process Modeling Module

Minor Changes
-------------

- Adds password capabilities to icingadb-redis configuration (#202)
- support Raspbian armhf repos (#203)

Bugfixes
--------

- Fix incorrect behaviour within `monitoring_plugins` that lead to a cycle of installation and removal of the same packages within one play
- Fix incorrect templating when passing integers in some parts of the Icinga Web 2 configuration.
- Fix to use correct URL for Debian Ubuntu (#195)
- Fixed typo in api.yml file (exits to exists)
- Role Icingaweb2: Adjust preferences setting to store preferences in database

v0.3.0
======

Major Changes
-------------

- Add Installation on Suse Systems
- Add TLS support to import schema for mysql and psql features
- Add a role for the installation and configuration of icingadb.
- Add a role for the installation and configuration of icingadb_redis.
- Add a role for the installation and configuration of icingaweb2.
- Add a role for the installation of the monitoring plugins as listed in the Icinga Template Library
- Add the ability to use the Icinga Repository Subscription on RedHat based distributions
- Manage Module Icinga Director
- Manage Module IcingaDB

Minor Changes
-------------

- Role Repos: Change manual epel handling to package #151
- The icinga2 role wrongly include parent vars file instead of its own #148

Bugfixes
--------

- Changed parameter enable_notification to enable_notifications
- Fix variable usage in icingaweb2_modules dict thx @Alpha041087
- Fixed usage of pgsql commands and imports thx @Alpha041087
- Prevent empty config directories to always be recreated
- Use lookup plugin to load icinga2_objects to support existing variables

v0.2.1
======

Release Summary
---------------

This is a bugfix release

Bugfixes
--------

- Fix bug in default filter for icinga2_ca_host
- Fix non-idenpotence during feature disabling

v0.2.0
======

Release Summary
---------------

This is the second major release

Major Changes
-------------

- Add custom config files
- Add icinga2_config_host var
- Add management of CA Host port
- Add object and feature Influxdb2Writer
- Add object and feature LiveStatusListener
- Add object and feature for ElasticsearchWriter
- Add object and feature for GelfWriter
- Add object and feature for IcingaDB
- Add object and feature for OpenTsdbWriter
- Add object and feature for PerfdataWriter
- Add support for Fedora
- Add support for icinga2_objects var outside of hostvars
- Add validation of CA fingerprint during certificate requests

Minor Changes
-------------

- Add CONTRIBUTING.md
- Add bullseye to supported OS and fix license in role metadata
- Add pylint to CI Workflows
- Added documentation for custom config
- Rework documentation structure
- Update documentation

Bugfixes
--------

- Fix Date type error
- Fix empty custom config
- Use correct version number into examples

v0.1.0
======

Release Summary
---------------

This is the initial release
