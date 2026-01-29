## Module Performance Data Graphs Graphite

Backend Icinga Web Module for Performance Data Graphs.
This module provides Graphite data to the [Performance Data Graphs](https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs) module.

**Important:** This module expects the [NETWAYS Extras repository](https://packages.netways.de/extras/) to be enabled on the system.
It can be enabled using the `repos` role.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values.
For parameters please check the [module documentation](https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs-graphite/blob/main/doc/02-Installation.md) or make manual changes in Icinga Web and have a look at the resulting configuration files.

```yaml
icingaweb2_modules:
  perfdatagraphsgraphite:
    enabled: true
    source: package
    config:
      graphite:
        api_url: "http://localhost:8080"
        api_timeout: "10"
        api_tls_insecure: "0"

```
