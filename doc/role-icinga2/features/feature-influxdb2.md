## InfluxDB2

To enable the feature **influxdb2** use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature Influxdb2Writer](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#influxdb2writer)

```yaml
icinga2_features:
  - name: influxdb2
    host: localhost
    port: 8086
    bucket: icinga2
    organization: monitoring
    auth_token: "changeme"
```

### Feature variables

* `host: string`
  *  InfluxDB host address. Defaults to 127.0.0.1.

* `port: int`
  * InfluxDB HTTP port. Defaults to 8086.

* `organization: string`
  * InfluxDB organization name.

* `bucket: string`
  * InfluxDB bucket name.

* `auth_token: string`
  * InfluxDB authentication token.

* `ssl_enable: boolean`
  * Whether to use a TLS stream. Defaults to false.

* `ssl_insecure_noverify: boolean`
  * Disable TLS peer verification.

* `ssl_ca_cert: string`
  * Path to CA certificate to validate the remote host.

* `ssl_cert: string`
  * Path to host certificate to present to the remote host for mutual verification.

* `ssl_key: string`
  * Path to host key to accompany the ssl_cert.

* `host_template: dictionary`
  * Host template to define the InfluxDB line protocol.

* `service_template: dictionary`
  * Service template to define the influxDB line protocol.

* `enable_send_thresholds: boolean`
  * Whether to send warn, crit, min & max tagged data.

* `enable_send_metadata: boolean`
  * Whether to send check metadata e.g. states, execution time, latency etc.

* `flush_interval: string`
  * How long to buffer data points before transferring to InfluxDB. Defaults to 10s.

* `flush_threshold: int`
  * How many data points to buffer before forcing a transfer to InfluxDB. Defaults to 1024.

* `enable_ha: boolean`
  * Enable the high availability functionality. Only valid in a cluster setup. Defaults to false.
