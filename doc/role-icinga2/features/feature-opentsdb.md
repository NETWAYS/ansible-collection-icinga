## OpenTSDB

To enable the feature OpenTSDB use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature OpenTsdbWriter](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#opentsdbwriter)

```yaml
icinga2_features:
  - name: opentsdb
    host: localhost
    port: 4242
```

### Feature variables

* `host: string`
  * OpenTSDB host address. Defaults to 127.0.0.1.

* `port: int`
  * OpenTSDB port. Defaults to 4242.

* `enable_ha: boolean`
  * Enable the high availability functionality. Only valid in a cluster setup. Defaults to false

* `enable_generic_metrics: boolean`
  * Re-use metric names to store different perfdata values for a particular check. Use tags to distinguish perfdata instead of metric name. Defaults to false

* `host_template: dictionary`
  * Specify additional tags to be included with host metrics. This requires a sub-dictionary named tags. Also specify a naming prefix by setting metric. More information can be found in OpenTSDB custom tags and OpenTSDB Metric Prefix. More information can be found in OpenTSDB custom tags. Defaults to an empty Dictionary

* `service_template: dictionary`
  * Specify additional tags to be included with service metrics. This requires a sub-dictionary named tags. Also specify a naming prefix by setting metric. More information can be found in OpenTSDB custom tags and OpenTSDB Metric Prefix. Defaults to an empty Dictionary.
