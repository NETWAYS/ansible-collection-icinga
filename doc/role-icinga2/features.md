# Icinga 2 Features

To configure features in addition to the set defaults use the variable `icinga2_features`.

Icinga 2 features can be added with their attributes as described in the Icinga 2 documentation.
[Documentation Icinga 2 Features](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#features)

A few other features can have more attributes to configure the feature itself, like the [API feature](features/feature-api.md).

Current supported features:

* [Feature API](features/feature-api.md)
* [Feature Command](features/feature-command.md)
* [Feature CompatLog](features/feature-compatlog.md)
* [Feature ElasticSearch](features/feature-elasticsearch.md)
* [Feature GelfWriter](features/feature-gelf.md)
* [Feature Graphite](features/feature-graphite.md)
* [Feature IcingaDB](features/feature-icingadb.md)
* [Feature IDO](features/feature-ido.md)
* [Feature InfluxDB](features/feature-influxdb.md)
* [Feature InfluxDB2](features/feature-influxdb2.md)
* [Feature Livestatus](features/feature-livestatus.md)
* [Feature mainlog](features/feature-mainlog.md)
* [Feature notification](features/feature-notification.md)
* [Feature perfdata](features/feature-perfdata.md)

```yaml
icinga2_features:
  - name: checker
  - name: mainlog
  - name: graphite
    host: localhost
    port: 3000
  - name: api
    ca_host: none
    force_newcert: false
    endpoints:
      - name: NodeName
    zones:
      - name: ZoneName
        endpoints:
          - NodeName
```
