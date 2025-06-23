## Module Monitoring

The module Monitoring is the main module for the deprecated IDO backend.

## Configuration

The general module parameter `enabled` be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values. For all parameters please check the [module documentation](https://icinga.com/docs/icinga-web/latest/doc/03-Configuration/#configuration)

```yaml
icingaweb2_modules:
  monitoring:
    enabled: true
    commandtransports:
      icinga2_api:
        transport: api
        host: localhost
        username: root
        password: changeme
    backends:
      icinga2_ido_mysql:
        type: ido
        resource: icinga_ido
    config:
      security:
        protected_customvars: "*pw*,*pass*,community"
```
