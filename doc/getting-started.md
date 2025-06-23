### Getting Started

The collection includes six roles in the current version.

* icinga.repos: Role to manage repositories
  * [Documentation: doc/role-repos](role-repos/role-repos.md)
* netways.icinga2: Role to install and manage Icinga 2 instances.
  * [Documentation: doc/role-icinga2](role-icinga2/role-icinga2.md)
* netways.icingadb: Role to install and manage IcingaDB, Icinga2's new data backend.
  * [Documentation: doc/role-icingadb](role-icingadb/role-icingadb.md)
* netways.icingadb_redis: Role to install and manage Redis, IcingaDB's cache backend.
  * [Documentation: doc/role-icingadb_redis](role-icingadb_redis/role-icingadb_redis.md)
* netways.icingaweb2: Role to install and manage Icinga Web 2.
  * [Documentation: doc/role-icingaweb2](role-icingaweb2/role-icingaweb2.md)
* icinga.monitoring_plugins: Role to install and manage Icinga2 compatible monitoring plugins.
  * [Documentation: doc/role-monitoring_plugins](role-monitoring_plugins/role-monitoring_plugins.md)

---

The collection includes a plugin that allows you to use Icinga as an inventory source for Ansible.

* netways.icinga.icinga: Ansible Inventory Plugin to fetch hosts from Icinga.
  * [Documentation: doc/plugins/inventory/icinga-inventory-plugin.md](plugins/inventory/icinga-inventory-plugin.md)

---
**NOTE**

Please be careful if you have an existing installation and you want to use the
collection. All features which are not configured will be disabled.

---

## Requirements

**Operatingsystems**:
For **OSFamily Suse** please make sure the Collection **community.general** is available.
Otherwise the modules **zypper_repository** and **zypper** are missing.

**Imports**:
If you want the collection roles to **import schemas and users to databases**, make sure
the client (**"mysql", "psql"**) for your database is available on your system.

**Permissions/Become**:
The collection does administrative work on the server. Please ensure the ansible_user you are using has the right permissions. Otherwise use the parameter '--become' with your ansible-playbook command. 

If you need to use become for a specific role only, you can add the following structure in your playbook.

```yaml
- name: Play
  become: false
  hosts: all
  roles:
    - name: netways.icinga.icinga2
      become: true
    - some_other_role_without_become
    - name: explicit_no_become
      become: false
```


## Installation

To start with the collection, easily install it with the **ansible-galaxy** command.

Installation from Galaxy Server:

```bash
ansible-galaxy collection install netways.icinga
```

Or pull the collection from the git. (Only useable with Ansible version 2.10.9)
```bash
ansible-galaxy collection install git+https://github.com/NETWAYS/ansible-collection-icinga.git,0.4.0
```

Pre 2.10 you can also clone the repository, manually build and install the collection.

```bash
git clone https://github.com/NETWAYS/ansible-collection-icinga.git
ansible-galaxy collection build
ansible-galaxy collection install netways-icinga-0.4.0.tar.gz
```

## Databases

Icinga2 relies on relational databases for many parts of its functionality. **None** of those databases get installed by the roles. You need to install and configure them yourself. For doing so, there are many ways available, e.g. the Ansible role [geerlingguy.mysql](https://galaxy.ansible.com/geerlingguy/mysql) for MySQL flavours (both MySQL and MariaDB) or [geerlingguy.postgresql](https://galaxy.ansible.com/geerlingguy/postgresql) for PostGresQL:

```yaml
- name: Configure databases for Icinga2
  hosts: database
  vars:
    mysql_databases:
      - name: icingadb
      - name: icingaweb
      - name: vspheredb
        encoding: utf8mb4
        collation: utf8mb4_unicode_ci
      - name: director
    mysql_users:
      - name: icingadb-user
        host: localhost
        password: icingadb-password
        priv: "icingadb.*:ALL"
    [...]
  roles:
    - role: geerlingguy.mysql
```

> [!NOTE]
> Schema migrations needed for the respective Icinga components to work will be handled either by the respective roles or by the Icinga components themselves.



## Example Playbooks

This is an example on how to install an Icinga 2 server/master instance.

```yaml
- name: install icinga2 master
  hosts: master
  vars:
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
      - name: idomysql
        state: present
        import_schema: false   # Enable this if the database and permissions for the user is created in advance.
        user: icinga
        password: icinga123
        database: icingaido
        cleanup:
          downtimehistory_age: 31d
          contactnotifications_age: 31d
      - name: mainlog
        severity: information

  roles:
    - netways.icinga.repos
    - netways.icinga.icinga2
```

This is an example on how to install an Icinga 2 agent instance.

```yaml
- name: install icinga2 agent
  hosts: agent
  vars:
    icinga2_confd: false # Disable example configuration
    icinga2_purge_features: yes # Ansible will manage all features
    icinga2_features:
      - name: api           # Enable Feature API
        ca_host: master.localdomain
        # Trusted Cert and Ticket will be gathered from this host.
        # Ticket will be "delegated" if the FQDN is not in your Ansible environment
        # use the variable icinga2_delegate_host in addition.
        endpoints:
          - name: NodeName
        zones:
          - name: ZoneName
            endpoints:
              - NodeName
      - name: notification
        state: absent

  roles:
    - netways.icinga.repos
    - netways.icinga.icinga2
```

This is a example on how to install Icinga 2 server with Icinga Web 2 and Icinga DB.

```yaml
- name: Converge
  hosts: all
  vars:
    icingaweb2_db:
      type: mysql
      name: icingaweb
      host: 127.0.0.1
      user: icingaweb
      password: icingaweb
    icingaweb2_db_import_schema: true

    icingadb_database_type: mysql
    icingadb_database_host: localhost
    icingadb_database_user: icingadb
    icingadb_database_password: icingadb
    icingadb_database_import_schema: true

    # Mysql Configuration on Ubuntu2204
    mysql_innodb_file_format: barracuda
    mysql_innodb_large_prefix: 1
    mysql_innodb_file_per_table: 1
    mysql_packages:
      - mariadb-client
      - mariadb-server
      - python3-mysqldb
    mysql_users:
      - name: icingaweb
        host: "%"
        password: icingaweb
        priv: "icingaweb.*:ALL"
      - name: icingadb
        host: "%"
        password: icingadb
        priv: "icingadb.*:ALL"
    mysql_databases:
      - name: icingadb
      - name: icingaweb


    icinga2_confd: false
    icinga2_features:
      - name: icingadb
        host: 127.0.0.1
      - name: notification
      - name: checker
      - name: mainlog
      - name: api
        ca_host: none
        endpoints:
          - name: "{{ ansible_fqdn }}"
        zones:
          - name: "main"
            endpoints:
              - "{{ ansible_fqdn }}"
  pre_tasks:
    - ansible.builtin.include_role:
        name: netways.icinga.repos
    # Geerlingguy mysql role to configure the databases.
    - ansible.builtin.include_role:
        name: geerlingguy.mysql
    - ansible.builtin.include_role:
        name: netways.icinga.icinga2
    - ansible.builtin.include_role:
        name: netways.icinga.icingadb
    - ansible.builtin.include_role:
        name: netways.icinga.icingadb_redis

  post_tasks:
    - ansible.builtin.include_role:
        name: netways.icinga.icingaweb2
```
