# ansible-collection-icinga

Collection to setup and manage components of the Icinga software stack.

## Documentation and Roles
* [Getting Started](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/getting-started.md)
* [Role: netways.icinga.repos](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-repos/)
* [Role: netways.icinga.icinga2](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/)
  * [Parser and Monitoring Objects](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/objects.md)
  * [Features](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/features.md)
* [Role: netways.icinga.ifw](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-ifw/)
* [Role: netways.icinga.icingadb](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icingadb/)
* [Role: netways.icinga.icingadb_redis](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icingadb_redis/)
* [Role: netways.icinga.icingaweb2](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icingaweb2/)
* [Role: netways.icinga.monitoring_plugins](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-monitoring_plugins/)
  * [List of Available Check Commands](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-monitoring_plugins/check_command_list.md)
* [Role: netways.icinga.icinga_kubernetes](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga_kubernetes/)
* [Inventory Plugin: netways.icinga.icinga](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/plugins/inventory/icinga-inventory-plugin.md)


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

## Secrets and no_log

Some tasks in these roles make use of sensitive information (e.g. passwords).
To avoid leaking this information the tasks in question use Ansible's `no_log: true` option.<br>
This however can make troubleshooting cumbersome.
**If** you need to and you are fine with secrets being present in Ansible's logs, you can turn logging back on.
Be sure though to [**deactivate logging to syslog**](https://docs.ansible.com/projects/ansible/latest/reference_appendices/config.html#default-no-target-syslog) to avoid leaking secrets on your target hosts.

Example to turn on logging for the `icinga2` role while not logging to syslog:

```
ANSIBLE_NO_TARGET_SYSLOG=True ansible-playbook </path/to/playbook> -e '{ "icinga2_no_log": false }'
```
