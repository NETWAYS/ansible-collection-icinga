## Elasticsearch

To enable the feature Elasticsearch use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature ElasticsearchWriter](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#elasticsearchwriter)

```yaml
icinga2_features:
  - name: elasticsearch
    host: localhost
    port: 9200
    index: "icinga2"
    enable_send_perfdata: true
    flush_interval: 10
    flush_threshold: 1024
```

### Feature variables

* `host: string`
  * Required. Elasticsearch host address. Defaults to 127.0.0.1.

* `port: int`
  * Required. Elasticsearch port. Defaults to 9200.

* `index: string`
  * Required. Elasticsearch index name. Defaults to icinga2.

* `enable_send_perfdata: boolean`
  *  Send parsed performance data metrics for check results. Defaults to false.

* `flush_interval: string`
  *  How long to buffer data points before transferring to Elasticsearch. Defaults to 10s.

* `flush_threshold: int`
  * How many data points to buffer before forcing a transfer to Elasticsearch. Defaults to 1024.

* `username: string`
  * Basic auth username if Elasticsearch is hidden behind an HTTP proxy.

* `password: string`
  * Basic auth password if Elasticsearch is hidden behind an HTTP proxy.

* `enable_tls: boolean`
  * Whether to use a TLS stream. Defaults to false. Requires an HTTP proxy.

* `insecure_noverify: boolean`
  * Disable TLS peer verification.

* `ca_path: string`
  * Path to CA certificate to validate the remote host. Requires enable_tls set to true.

* `cert_path: string`
  * Path to host certificate to present to the remote host for mutual verification. Requires enable_tls set to true.

* `key_path: string`
  *  Path to host key to accompany the cert_path. Requires enable_tls set to true.

* `enable_ha: boolean`
  * Whether to send warn, crit, min & max tagged data.
