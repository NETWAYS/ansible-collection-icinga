## Module Performance Data Graphs Elasticsearch

Backend Icinga Web Module for Performance Data Graphs.
This module provides Elasticsearch data to the [Performance Data Graphs](https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs) module.

**Important:** This module expects the [NETWAYS Extras repository](https://packages.netways.de/extras/) to be enabled on the system.
It can be enabled using the `repos` role.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values.
For parameters please check the [module documentation](https://github.com/NETWAYS/icingaweb2-module-perfdatagraphs-elasticsearch) or make manual changes in Icinga Web and have a look at the resulting configuration files.

> For `icinga_writer` choose `ElasticsearchWriter` or `OTLPMetricsWriter` based on the Icinga 2 feature used to write the metrics.

Example - No auth:

```yaml
icingaweb2_modules:
  perfdatagraphselasticsearch:
    enabled: true
    source: package
    config:
      elasticsearch:
        icinga_writer: "ElasticsearchWriter"
        api_index: "icinga2"
        api_url: "https://node1:9200,https://node2:9200"
        api_auth_method: "none"
        api_timeout: "10"
        api_max_data_points: "10000"
```

Example - Basic auth:

```yaml
icingaweb2_modules:
  perfdatagraphselasticsearch:
    enabled: true
    source: package
    config:
      elasticsearch:
        icinga_writer: "ElasticsearchWriter"
        api_index: "icinga2"
        api_url: "https://node1:9200"
        api_auth_method: "basic"
        api_auth_username: "icinga2-user"
        api_auth_password: "icinga2-password"
        api_tls_insecure: "0"
```


Example - Token auth:

```yaml
icingaweb2_modules:
  perfdatagraphselasticsearch:
    enabled: true
    source: package
    config:
      elasticsearch:
        icinga_writer: "ElasticsearchWriter"
        api_index: "icinga2"
        api_url: "https://node1:9200"
        api_auth_method: "token"
        api_auth_tokentype: "Bearer"
        api_auth_tokenvalue: "super-secret-bearer-token"
        api_tls_insecure: "0" # don't validate certificates
```
