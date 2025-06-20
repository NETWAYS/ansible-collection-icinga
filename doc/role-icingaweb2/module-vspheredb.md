## Module vSphereDB

> [!WARNING]
> This module can only be installed from source as it has not been packaged yet.
> Therefore, `git` is a needed dependency to be present on the target system.
> The role will then install `vspheredb` and its dependency `incubator`.

## Configuration

The general module parameter like `enabled` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values. For all parameters please check the [module documentation](https://icinga.com/docs/icinga-vsphere-integration/latest/doc/01-Installation/)

as Icinga Web 2 resource, please use the `icingaweb2_resources` variable to define
the resource.

Example:

```
icingaweb2_resources:
  vspheredb:
    type: db
    db: mysql
    host: localhost
    dbname: vspheredb
    username: vspheredb
    password: vspheredb
    charset: utf8mb4

icingaweb2_modules:
  vspheredb:
    enabled: true
    source: package
    config:
      db:
        resource: vspheredb
```

## Database 

The database can be created using the Geerlingguy mysql role. 

For more parameters please check the [role documentation](https://github.com/geerlingguy/ansible-role-mysql)

Example: 

```
mysql_databases:
  - name: vspheredb
    encoding: utf8mb4
    collation: utf8mb4_general_ci

pre_tasks:
  - ansible.builtin.include_role:
      name: geerlingguy.mysql


```