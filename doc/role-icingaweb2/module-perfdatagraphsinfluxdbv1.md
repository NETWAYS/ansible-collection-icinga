## Module Performance Data Graphs InfluxDB v1

Backend Icinga Web Module for Performance Data Graphs.
This module provides InfluxDB v1 data to the [Performance Data Graphs](https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs) module.

**Important:** This module expects the [NETWAYS Extras repository](https://packages.netways.de/extras/) to be enabled on the system.
It can be enabled using the `repos` role.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values.
For parameters please check the [module documentation](https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs-influxdbv1/blob/main/doc/02-Installation.md) or make manual changes in Icinga Web and have a look at the resulting configuration files.

```yaml
icingaweb2_modules:
  perfdatagraphsinfluxdbv1:
    enabled: true
    source: package
    config:
      influx:
        api_url: "http://localhost:8086"
        api_database: "icinga2"
        api_tls_insecure: "0"
        api_username: "username"
        api_password: "password"
```
