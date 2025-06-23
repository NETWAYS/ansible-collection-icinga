# Role netways.icinga.icingaweb2

The role icingaweb2 installs and configures Icinga Web 2 and its modules.

### Modules
* [Director](./module-director.md)
* [IcingaDB](./module-icingadb.md)
* [Monitoring](./module-monitoring.md)

## Databases

Icingaweb2 and some of its modules rely on a relational database to persist data. These databases **won't** be created by this role - you need to deploy and configure them in advance. For more information, see the [Databases](../getting-started.md#databases) section in the getting started guide.

## Variables

### Icinga Web 2 DB Configuration

If you use this configuration it will be your main Icinga Web DB, this means if the variable `icingaweb2_db_import_schema` is used the schema will be imported to this database.

```yaml
icingaweb2_db:
  type: mysql
  name: icingaweb
  host: 127.0.0.1
  user: icingaweb
  password: icingaweb
```

* `icingaweb2_db_import_schema: boolean`
  * Decides whether the schema should be imported in the database defined at `icingaweb2_db`. **Default: False**

* `icingaweb2_admin_<username|password>: string`
  * Set the username and password for the first admin user for Icinga Web 2.

* `icingaweb2_admin_recreate: boolean`
  * Recreate can be used to change the password of the admin. **Default: False**

In addition to the Icinga Web 2 Admin, other users can be configured by defining `icingaweb2_users`.<br>
The `recreate` parameter can be used to change passwords or to enable the user if he has been disabled. **Default: False**

```yaml
icingaweb2_users:
  - username: 'foo'
    password: 'bar'
    recreate: true
  - username: webadmin
    [...]
```

### Resources

Besides the standard Icinga Web 2 database you may configure additional resources for IcingaDB or automated imports.

```yaml
icingaweb2_resources:
  icinga_ido:
    type: db
    db: mysql
    host: localhost
    dbname: icinga
    username: icinga
    password: icinga
    use_ssl: 0
    charset: utf8
  my_ldap:
    type: ldap
    [...]
```

### General Configuration

The general configuration of Icinga Web 2 is located at `{{ icingaweb2_config_dir }}/config.ini`.
To create the file the following variable is used (default):

```yaml
icingaweb2_config:
  global:
    show_stacktraces: 1
    show_application_state_messages: 1
    config_resource: icingaweb2_db
    module_path: /usr/share/icingaweb2/modules
  logging:
    log: syslog
    level: ERROR
    application: icingaweb2
    facility: user
  themes:
    default: Icinga
```

Within a task the YAML structure is effectively translated to INI and written to `{{ icingaweb2_config_dir }}/config.ini`.

Explained:

* `icingaweb2_config` defines the file to be written (`config.ini`)
* `global`, `logging` and `themes` are the names of the respective sections within the INI file
* Everything underneath each key / section is a key value pair for the given section within the INI file

So the above YAML results in:

```ini
[global]
show_stacktraces = "1"
show_application_state_messages = "1"
config_resource = icingaweb2_db
module_path = /usr/share/icingaweb2/modules

[logging]
log = syslog
level = ERROR
application = icingaweb2
facility = user

[themes]
default = Icinga
```

For more information about the general configuration have a look at the [official documentation](https://icinga.com/docs/icinga-web/latest/doc/03-Configuration/#general-configuration).

### Authentication

At least one method of user authentication needs to be configured in order to use Icinga Web 2. This is achieved by defining `icingaweb2_authentication`.<br>
By default the following is set:

```yaml
icingaweb2_authentication:
  icingaweb2:
    backend: db
    resource: icingaweb2_db
```

This is also converted to INI and written to `{{ icingaweb2_config_dir }}/authentication.ini`

---

Similar to the above snippet group backends can also be defined using `icingaweb2_groups`.<br>
Default:

```yaml
icingaweb2_groups:
  icingaweb2:
    backend: db
    resource: icingaweb2_db
```

For more information about key value pairs for different authentication methods see the [official documentation](https://icinga.com/docs/icinga-web/latest/doc/05-Authentication/).
