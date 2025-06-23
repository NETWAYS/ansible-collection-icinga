## PerfdataWriter

To enable the feature perfdata use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature PerfdataWriter](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#perfdatabwriter)

```yaml
icinga2_features:
  - name: perfdata
    host_perfdata_path: "/var/spool/icinga2/perfdata/host-perfdata"
    service_perfdata_path: "/var/spool/icinga2/perfdata/service-perfdata"
    host_format_template: "DATATYPE::HOSTPERFDATA"
    service_format_template: "DATATYPE::SERVICEPERFDATA"
    rotation_interval: "15s"
```

### Feature variables

* `host_perfdata_path: string`
  * Path to the host performance data file. Defaults to SpoolDir + “/perfdata/host-perfdata”.

* `service_perfdata_path: string`
  * Path to the service performance data file. Defaults to SpoolDir + “/perfdata/service-perfdata”.

* `host_temp_path: string`
  * Path to the temporary host file. Defaults to SpoolDir + “/tmp/host-perfdata”.

* `service_temp_path: string`
  * Path to the temporary service file. Defaults to SpoolDir + “/tmp/service-perfdata”.

* `host_format_template: string`
  * Host Format template for the performance data file. Defaults to a template that’s suitable for use with PNP4Nagios.

* `service_format_template: string`
  * Service Format template for the performance data file. Defaults to a template that’s suitable for use with PNP4Nagios.

* `rotation_interval: string`
  * Rotation interval for the files specified in {host,service}_perfdata_path. Defaults to 30s.

* `enable_ha: boolean`
  * Enable the high availability functionality. Only valid in a cluster setup. Defaults to false.
