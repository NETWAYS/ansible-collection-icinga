## Module Director

The module Icinga Director provides a management GUI for Icinga 2 DSL.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values. For all parameters please check the [module documentation](https://icinga.com/docs/icinga-director/latest/doc/03-Automation/)

The database resource won't be created
as Icinga Web 2 resource, please use the `icingaweb2_resources` variable to define
the resource.

`import_schema`: Checks for pending migrations on the database and applies them if needed.

`run_kickstart`: Runs kickstart when needed, please make sure the api user is available before.



```yaml
icingaweb2_modules:
  director:
    enabled: true
    source: package
    import_schema: true
    run_kickstart: true
    kickstart:
      config:
        endpoint: "{{ ansible_facts['fqdn'] }}"
        host: 127.0.0.1
        username: root
        password: root
    config:
      db:
        resource: director_db
```
