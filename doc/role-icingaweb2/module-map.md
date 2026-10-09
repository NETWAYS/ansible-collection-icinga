## Module Map

Icinga Web Module to show hosts and services on a map, based on OpenStreetMap and Leaflet.
The position of a host is defined by its custom variable `geolocation`, e.g. `vars.geolocation = "52.52,13.40"`.

**Important:** This module expects the [NETWAYS Extras repository](https://packages.netways.de/extras/) to be enabled on the system.
It can be enabled using the `repos` role.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values.
For parameters please check the [module documentation](https://github.com/nbuchwitz/icingaweb2-module-map/tree/master/doc).

```yaml
icingaweb2_modules:
  map:
    enabled: true
    source: package
    config:
      map:
        default_zoom: 6
        default_lat: 51.16
        default_long: 10.45
        stateType: hard
        cluster_problem_count: 1
```

> The checkbox options `cluster_problem_count` and `popup_mouseover` have to be set to `0` or `1`, not `true` / `false`.
