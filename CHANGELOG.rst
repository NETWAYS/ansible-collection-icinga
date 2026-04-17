===========================
Icinga.Icinga Release Notes
===========================

.. contents:: Topics

v0.4.8
======

Release Summary
---------------

Quick version bump to have a working tag release.

Bugfixes
--------

- Remove use of :code:`pipefail` for now since it is not necessarily supported by the default shells.
  It might be reintroduced at a later point if the :code:`dash` shell widely supports it on systems also supported by Icinga.

v0.4.7
======

Release Summary
---------------

Small bugfix release, also brining in a few smaller features.

Minor Changes
-------------

- Add :code:`delegate_pki` option to the Icinga 2 API feature for reverse-connected environments where the agent cannot reach the parent / CA host but connections to the agent are possible. (#392) Thanks @lucagubler
- Add option :code:`environment_id` to the :code:`icingadb` feature (role :code:`icinga2`).
  This allows users to specify the content of :code:`/var/lib/icinga2/icingadb.env`.
  Messing with this option can lead to duplicate entries in the database, so be sure to first read the `documentation <https://icinga.com/docs/icinga-db/latest/doc/05-Distributed-Setups/#environment-id>`__ in case you really need to make use of this option.
- Add the `Cube module <https://icinga.com/docs/icinga-cube/latest/doc/01-About/>`__ to the :code:`icingaweb2` role.
- Add the `vSphereDB module <https://icinga.com/docs/icinga-vsphere-integration/latest/doc/01-Installation/>`__ to the :code:`icingaweb2` role.

Security Fixes
--------------

- Add :code:`no_log: true` to some tasks that previously leaked secrets to Ansible's log (e.g. the terminal output).
  Some of those tasks also leaked secrets to the target hosts' syslog if not disabled in the Ansible configuration.
  Even though the impact is expected to be low, you might sill want to rotate your passwords (mostly database passwords) to be on the safe side.
  Thanks @oxzi for the input and for testing

Bugfixes
--------

- Avoid warnings about the reserved variable name :code:`args` in the :code:`icinga2` role. (#449)
- Fix rendering of :code:`host.vars.xyz` within :code:`imports` when using :code:`icinga2_object`. Previously, all list entries passed to `imports` were treated as plain strings and thus were quoted in the resulting configuration. The values are now checked against the :code:`<obj>.vars` pattern and all defined constants to decide whether the values should be quoted or not. (#317)
- The :code:`icingadb` feature for Icinga 2 can now work with the :code:`username` attribute. This can be used when working with Redis ACLs. (#447)

v0.4.6
======

Release Summary
---------------

Besides some smaller fixes this release mostly contains enhancements to the documentation. It is now (more) compatible with Ansible Galaxy, properly rendering the collection README and the roles's README files. Links within the READMEs redirect to the repository for further documentation.
Some roles now also use :code:`argument_specs`. This is used for input validation (role variables), and for documentation.
You can run :code:`ansible-doc --type role netways.icinga.<role>` to read a short documentation about the role's variables locally.
To see what roles already have `argument_specs`, run :code:`ansible-doc --type role --list netways.icinga`.

Minor Changes
-------------

- Add EL 10 to the :code:`monitoring_plugins` role.
- Add templating support for :code:`url`, :code:`user` and :code:`password` variables in :code:`netways.icinga.icinga` inventory plugin to support loading them from :code:`ansible-vault`. Thanks @johannesst
- Add the `Performance Data Graphs <https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs>`__ modules as available modules to the `icingaweb2` role. They rely on the `NETWAYS Extras Repository <https://packages.netways.de/extras/>`__ being enabled.
- Add the ability to add the `NETWAYS Extras <https://packages.netways.de/extras/>`__ and `NETWAYS Plugins <https://packages.netways.de/plugins/>`__ repositories to provide more packages. If the repositories `netways-extras` / `netways-plugins` already exist on the system, they are - by default - disabled by the role.
- Change occurrences of :code:`ansible_<fact_name>` to :code:`ansible_facts["<fact_name>"]` in preparation of :code:`ansible-core=2.24`'s new :code:`INJECT_FACTS_AS_VARS` behavior.

Bugfixes
--------

- Fix escaping of special characters within the generic INI writer (:code:`icingaweb2` role). Values are now enclosed by double quotes while using the :code:`to_json` filter for the escaping (#426).
- The :code:`icinga2_object` plugin did not make use of the :code:`name` parameter passed to it when using :code:`apply_for`. If more than one service used the same :code:`apply_for`, this would result in multiple services with the same name, thus leading to failure (#434). The plugin now uses the :code:`name` as a prefix for the service name.
- The IfW :code:`InstallCommand` now uses double quotes around the JSON to avoid timeouts during the task (#432). The JSON is also properly parsed and put into a single line to further avoid unwanted behavior. Thanks @afeefghannam89 for bringing up the topic again and testing the fix.
- The package name for EPEL on OracleLinux is :code:`oracle-epel-release-el<version number>`. Some versions of OracleLinux provide a mapping from :code:`epel-release` to the appropriate package name while others do not. The :code:`repos` and :code:`monitoring_plugins` roles now use variables to handle the different names of the package correctly (#437).
- Using the :code:`ifw` role in pre-existing Icinga for Windows installations would fail due to :code:`IfW-CustomHostname` potentially not being set at all. The role now defaults to comparing with :code:`null` if unset, avoiding failure in the process.

v0.4.5
======

Release Summary
---------------

Small bugfix release.

Bugfixes
--------

- Empty config directories are now cleaned up **after** config assembly within the :code:`icinga2` role. This should avoid leftover files from previous deployments.
- Fix automatic determination of IfW framework path (:code:`ifw_framework_path`).
- Fix quoting of password within mysql command for IDO database schema import.
- Use explicit booleans in conditions inside of role :code:`monitoring_plugins` for compatibility with :code:`ansible-core >= 2.19`. Thanks @gianmarco-mameli
- Using :code:`ansible.windows.win_powershell` for the :code:`Install-Icinga` command can sometimes get stuck and stay idle indefinitely. The according task now uses :code:`ansible.windows.win_shell` as this seems to be more reliable.

v0.4.4
======

Release Summary
---------------

Introduction of Icinga for Windows role :code:`ifw` and performance increase in deployment of :code:`icinga2_objects`.

Major Changes
-------------

- Introduction of role :code:`ifw` - Icinga for Windows: This role allows to install the Icinga PowerShell Framework, manage components and repositories, and install and configure Icinga 2 through Icinga for Windows.
- Module :code:`ifw_backgrounddaemon`: Registers/unregisters an Icinga for Windows background daemon.
- Module :code:`ifw_component`: Installs/removes/updates Icinga for Windows components (e.g. :code:`agent`, :code:`plugins`).
- Module :code:`ifw_restapicommand`: Adds/removes commands to/from the whitelist/blacklist of the Icinga for Windows REST-Api.
- The performance of the action plugin :code:`icinga2_object` has been greatly improved.
  Instead of writing individual objects to files and later merging them,
  they are instead now merged in memory on a per destination basis.
  This means that configuration files no longer have to be assembled after the fact.

  This also drops the :code:`order` parameter previously used to define the order in which
  objects are written if they belong to the same destination file.
  The new behavior only changes the order in the files but does not change the end result.

  A performance gain of up to 80% has been seen in testing.

Minor Changes
-------------

- In the :code:`icinga2` role objects are collected from different places before writing them to files. Duplicates could occur which was not taken care of. All collected objects are now deduplicated using the :code:`unique` filter right before writing to save some time during execution.
- The deb repositories made available by the :code:`repos` role now use the `deb822 format <https://repolib.readthedocs.io/en/latest/deb822-format.html>`__. This can lead to APT warnings on systems that already have the repositories deployed using the old format (sources.list). To fix this, simply remove the old :code:`icinga.list` file after the repositories have been deployed in the new format.
- The error messages about unsupported operating systems have been tuned. They should now appear if and only if the actual OS is in fact not supported instead of appearing after unrelated task failures.

Bugfixes
--------

- :code:`icingaweb2_roles` was not deployed at all if :code:`icingaweb2_admin_username` and :code:`icingaweb2_admin_password` were missing. Now for both, the predefined admin role and user-defined :code:`icingaweb2_roles`, the respective variables are tested for correctly when creating :code:`roles.ini`. Thus, the creation of an initial admin user is no longer strictly necessary.
- A short example for the previously undocumented :code:`icingaweb2_roles` has been added.

Known Issues
------------

- With the changes in :code:`icinga2_object` arises a problem.
  The prior directory structure within :code:`icinga2_fragments_path` (default: :code:`/var/tmp/icinga/`) does not fit the new approach for writing configuration files.
  Some paths that would become directories before are now treated as files.
  If the old directory structure is present on a remote host, deployment with the new method will most likely fail due to this.

  If the execution of :code:`icinga2_object` fails, deleting :code:`icinga2_fragments_path` should fix the problem.
  This, however, is a manual step that needs to be done.

v0.4.3
======

Release Summary
---------------

Small bugfix release mostly regarding databases and Icinga Web 2.

Bugfixes
--------

- Add internal modules to installable modules list. This allows for modules directly shipped with Icinga Web 2 to be configurable. This mostly affects the :code:`monitoring` module since it has actual configuration options. Others like :code:`setup` can now be enabled/disabled.
- Fix issue where the package for any given Icinga Web 2 module was not installed if that module had set :code:`enabled: false`.
  Modules are now installed and configured properly even when they are set to be disabled in the end.
- Fixed an issue where the :code:`config.ini` file of the :code:`monitoring` module was not deployed.
- More complex database passwords have been an issue when importing database schemas. The passwords are now properly quoted using the :code:`quote` filter.
  This means that passwords containing characters such as :code:`#` and :code:`\\` should now work correctly.

  The change affects Icinga 2 (IDO), Icinga for Kubernetes, Icinga DB and Icinga Web 2.
- Switch from :code:`run_once: true` to :code:`throttle: 1` when applying database schema.
  The initial intention was to apply the schema once per cluster. However, if nodes are independent, e.g. multiple clusters, this would still only run on the first host, leaving the other node(s) with empty databases.

  The tasks are rewritten to now check whether the schema needs to be applied before trying to do so.
  This happens one host at a time. Thus, the tasks take slightly more time but work when using multiple clusters.

v0.4.2
======

Release Summary
---------------

Small quality of life & bugfix release.

Minor Changes
-------------

- Extend condition for the API feature when using self generated certificates.
  This avoids running the given portion of the code unnecessarily.
  Thanks @thesefer
- For Icinga2 certificates and key file permissions are now set explicitly when using self generated certificates (**0644** and **0600** respectively).
- The Icinga2 API feature now allows for the use of certificates already present on the remote host.
  This means that certificates (and the key) no longer have to be present on the Ansible controller
  which allows for more flexibility when it comes to certificate deployment.
  The new behavior can be activated by setting :code:`ssl_remote_source: true` within the API feature.

Bugfixes
--------

- The TLS configuration for Icinga DB / Icinga DB Redis has been faulty. Both configuration templates now render properly based on the given TLS related variables.
  If using TLS in Icinga DB Redis, the non-TLS port will be disabled. The Icinga DB (daemon) configuration now uses the correct YAML key for both the TLS port and the non-TLS port.

v0.4.1
======

Release Summary
---------------

This release introduces Icinga for Kubernetes (thanks to @gianmarco-mameli), removes deprecation warnings present in the prior release, adds a new filter and support for the Graphite module.

Major Changes
-------------

- Add a role for the installation and configuration of `Icinga for Kubernetes <https://icinga.com/docs/icinga-for-kubernetes/latest/>`_.
- Add tasks to role :code:`icingaweb2` to install and configure `Icinga for Kubernetes Web <https://icinga.com/docs/icinga-kubernetes-web/latest/doc/02-Installation/>`_.

Minor Changes
-------------

- Add :code:`netways.icinga.icinga2_ticket` filter. This filter converts a given string (NodeName) into an Icinga2 ticket using a TicketSalt.
- Add Icinga Web 2 module :code:`Graphite`.
- Add variable :code:`icingadb_redis_client_certificate` to define whether TLS client certificates are accepted/required/rejected when connecting to the Redis server. Only has an effect when using TLS encryption.

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

- netways.icinga.icinga2_compatlogger - Creates information for CompatLogger object.

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
