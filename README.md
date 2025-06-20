# ansible-collection-icinga

Collection to setup and manage components of the Icinga software stack.

## Documentation and Roles

* [Getting Started](doc/getting-started.md)
* [Role: netways.icinga.repos](doc/role-repos/role-repos.md)
* [Role: netways.icinga.icinga2](doc/role-icinga2/role-icinga2.md)
  * [Parser and Monitoring Objects](doc/role-icinga2/objects.md)
  * [Features](doc/role-icinga2/features.md)
* [Role: netways.icinga.icingadb](doc/role-icingadb/role-icingadb.md)
* [Role: netways.icinga.icingadb_redis](doc/role-icingadb_redis/role-icingadb_redis.md)
* [Role: netways.icinga.icingaweb2](doc/role-icingaweb2/role-icingaweb2.md)
* [Role: netways.icinga.monitoring_plugins](doc/role-monitoring_plugins/role-monitoring_plugins.md)
  * [List of Available Check Commands](doc/role-monitoring_plugins/check_command_list.md)
* [Inventory Plugin: netways.icinga.icinga](doc/plugins/inventory/icinga-inventory-plugin.md)

## Installation

You can easily install the collection with the `ansible-galaxy` command.

```bash
ansible-galaxy collection install netways.icinga
```

Or if you are using Tower or AWX add the collection to your requirements file.

```yaml
collections:
  - name: netways.icinga
```

## Usage

To use the collection in your playbooks, add the collection and then use the roles.

```yaml
- hosts: icinga-server
  roles:
    - netways.icinga.repos
    - netways.icinga.icinga2
    - netways.icinga.icingadb
    - netways.icinga.icingadb_redis
    - netways.icinga.monitoring_plugins
```
