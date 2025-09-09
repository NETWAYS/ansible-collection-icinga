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

## Example Playbook

### Icinga Full-Stack

This playbook deploys Icinga2, MariaDB, Icinga DB, Icingaweb 2 and the Director on
a single host. Its good for testing Icinga or for suitable for smaller
environments.

```yaml
- name: Icinga Full-Stack
  hosts: master
  become: true
  gather_facts: true
  vars:
    # geerlingguy.mysql
    mysql_root_password: supersecurepassword
    mysql_databases:
      - name: icingadb
      - name: icingaweb2
      - name: director
    mysql_users:
      - name: icingadb
        host: localhost
        password: icingadb-password
        priv: "icingadb.*:ALL"
      - name: icingaweb2
        host: localhost
        password: icingaweb2-password
        priv: "icingaweb2.*:ALL"
      - name: director
        host: localhost
        password: director-password
        priv: "director.*:ALL"

    # icinga.icinga.icinga2
    icinga2_constants:  # Set default constants and TicketSalt for the CA
      TicketSalt: "{{ lookup('ansible.builtin.password', '.icinga-server-ticketsalt') }}"
      NodeName: "{{ ansible_fqdn }}"
      ZoneName: "main"
    icinga2_confd: false # Disable example configuration
    icinga2_purge_features: yes # Ansible will manage all features
    icinga2_config_directories:  # List of directories in which the role will manage monitoring objects
      - zones.d/main/commands
      - zones.d/main/hosts
      - zones.d/main/services
      - zones.d/main
    icinga2_features:
      - name: api           # Enable Feature API
        ca_host: none       # No CA host, CA will be created locally
        endpoints:
          - name: NodeName
        zones:
          - name: ZoneName
            endpoints:
              - NodeName
      - name: checker
        state: present
      - name: notification
        state: present
      - name: icingadb
        host: localhost
        port: 6380
        password: redis-pass
      - name: mainlog
        severity: information

    icinga2_objects:
      - name: icingadb
        type: ApiUser
        file: "zones.d/main/apiuser.conf"
        password: icingadb
        permissions:
          - "actions/*"
          - "objects/query/*"
          - "objects/modify/*"
          - "status/query"
      - name: director
        type: ApiUser
        file: "zones.d/main/apiuser.conf"
        password: director
        permissions:
          - "*"

    # icinga.icinga.icingadb
    icingadb_database_type: mysql
    icingadb_database_host: 127.0.0.1
    icingadb_database_user: icingadb
    icingadb_database_password: icingadb-password
    icingadb_database_import_schema: true

    # icinga.icinga.icingaweb2
    icingaweb2_db:
      type: mysql
      name: icingaweb2
      host: 127.0.0.1
      user: icingaweb2
      password: icingaweb2-password
    icingaweb2_db_import_schema: true
    icingaweb2_resources:
      icingadb:
        type: db
        db: mysql
        host: localhost
        dbname: icingadb
        username: icingadb
        password: icingadb-password
        use_ssl: 0
        charset: utf8
      director:
        type: db
        db: mysql
        host: localhost
        dbname: director
        username: director
        password: director-password
        use_ssl: 0
        charset: utf8
    icingaweb2_modules:
      director:
        enabled: true
        source: package
        import_schema: true
        run_kickstart: true
        kickstart:
          config:
            endpoint: "{{ ansible_fqdn }}"
            host: 127.0.0.1
            username: director
            password: director
        config:
          db:
            resource: director
      icingadb:
        enabled: true
        source: package
        commandtransports:
          instance01:
            transport: api
            host: 127.0.0.1
            username: icingadb
            password: icingadb
        config:
          icingadb:
            resource: icingadb
          redis:
            tls: '0'
        redis:
          redis1:
            host: "127.0.0.1"
        
    icingaweb2_admin_username: icinga
    icingaweb2_admin_password: icinga

    # icinga.icinga.monitoring_plugins
    icinga_monitoring_plugins_check_commands:
      - 'all'

  roles:
    - geerlingguy.mysql
    - netways.icinga.repos
    - netways.icinga.icinga2
    - netways.icinga.icingadb_redis
    - netways.icinga.icingadb
    - netways.icinga.icingaweb2
    - netways.icinga.monitoring_plugins
```

### Master-Master Setup
