## Graphite

To enable the feature Graphite use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature GraphiteWriter](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#graphitewriter)

```yaml
icinga2_features:
  - name: graphite
    host: localhost
    port: 2003
```

### Feature variables

* `host: string`
  * Graphite Carbon host address. Defaults to 127.0.0.1.

* `port: int`
  * Graphite Carbon port. Defaults to 2003.

* `host_name_template: string`
  * Metric prefix for host name. Defaults to icinga2.$host.name$.host.$host.check_command$.

* `service_name_template: string`
  * Metric prefix for service name. Defaults to icinga2.$host.name$.services.$service.name$.$service.check_command$.

* `enable_send_thresholds: boolean`
  * Send additional threshold metrics. Defaults to false.

* `enable_send_metadata: boolean`
  * Send additional metadata metrics. Defaults to false.

* `enable_ha: boolean`
  * Enable the high availability functionality. Only valid in a cluster setup. Defaults to false.
