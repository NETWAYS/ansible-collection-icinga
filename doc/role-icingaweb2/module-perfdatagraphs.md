## Module Performance Data Graphs

Icinga Web Module for Performance Data Graphs.
This module enables graphs on the Host and Service Detail View for the respective performance data.

This module must be used in conjunction with its "backend" modules.
Have a look at the the [available modules](https://github.com/orgs/NETWAYS/repositories?q=icingaweb2-module-perfdatagraphs-).

**Important:** This module expects the [NETWAYS Extras repository](https://packages.netways.de/extras/) to be enabled on the system.
It can be enabled using the `repos` role.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values.
For parameters please check the [module documentation](https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs/blob/main/doc/03-Configuration.md) or make manual changes in Icinga Web and have a look at the resulting configuration files.

```yaml
icingaweb2_modules:
  perfdatagraphs:
    enabled: true
    source: package
    config:
      perfdatagraphs:
        default_backend: "graphite"
        default_timerange: "PT3H"
        cache_lifetime: "800"
```

> The backend name should be written **lowercase** (`graphite`, `influxdbv1`, `influxdbv2`, `prometheus`).
> The runtime backend lookup is case-insensitive, but the module's configuration form only pre-selects the dropdown entry when the value matches the lowercase backend key.
