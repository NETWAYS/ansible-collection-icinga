# ansible-collection-icinga

Collection to setup and manage components of the Icinga software stack.

## Documentation and Roles
* [Getting Started](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/getting-started.md)
* [Role: netways.icinga.repos](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-repos/README.md)
* [Role: netways.icinga.icinga2](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/README.md)
  * [Parser and Monitoring Objects](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/objects.md)
  * [Features](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/features.md)
* [Role: netways.icinga.icingadb](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icingadb/README.md)
* [Role: netways.icinga.icingadb_redis](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icingadb_redis/README.md)
* [Role: netways.icinga.icingaweb2](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icingaweb2/README.md)
* [Role: netways.icinga.monitoring_plugins](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-monitoring_plugins/README.md)
  * [List of Available Check Commands](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-monitoring_plugins/check_command_list.md)
* [Inventory Plugin: netways.icinga.icinga](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/plugins/inventory/README.md)


## Installation

You can easily install the collection with the `ansible-galaxy` command.

```bash
ansible-galaxy collection install netways.icinga
```

Or if you are using Tower or AWX, add the collection to your requirements file.

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
