## OTLPMetrics

To enable the feature **otlpmetrics** use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature OTLPMetricsWriter](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#otlpmetricswriter)

**NOTE** The `otlpmetrics` feature requires Icinga 2 `2.16` or later.

```yaml
icinga2_features:
  - name: otlpmetrics
    host: 127.0.0.1
    port: 4318
    metrics_endpoint: /v1/metrics
    service_namespace: icinga2-production
```

### Feature variables

* `host: string`
  * OTLP backend host address. Defaults to 127.0.0.1.

* `port: int`
  * OTLP backend HTTP port. Defaults to 4318.

* `metrics_endpoint: string`
  * OTLP metrics endpoint path. Defaults to /v1/metrics. Some backends use different paths, for example the Prometheus OTLP receiver uses /api/v1/otlp/v1/metrics.

* `service_namespace: string`
  * Namespace used in the `service.namespace` OTel resource attribute. Defaults to icinga.

* `basic_auth: dictionary`
  * Optional HTTP basic auth credentials with the keys `username` and `password`.

* `enable_tls: boolean`
  * Whether to use a TLS stream. Defaults to false.

* `tls_insecure_noverify: boolean`
  * Disable TLS peer verification.

* `tls_ca_file: string`
  * Path to CA certificate to validate the remote host.

* `tls_cert_file: string`
  * Path to host certificate to present to the remote host for mutual verification.

* `tls_key_file: string`
  * Path to host key to accompany the `tls_cert_file`.

* `enable_send_thresholds: boolean`
  * Whether to send threshold values (warn, crit, min, max) as `state_check.threshold` metric points. Defaults to false.

* `host_resource_attributes: dictionary`
  * Custom resource attributes attached to host check metrics. Values may contain Icinga 2 macros. Exported with the prefix `icinga2.custom.`.

* `service_resource_attributes: dictionary`
  * Custom resource attributes attached to service check metrics. Values may contain Icinga 2 macros. Exported with the prefix `icinga2.custom.`.

* `enable_ha: boolean`
  * Enable the high availability functionality. Only valid in a cluster setup. Defaults to true.
