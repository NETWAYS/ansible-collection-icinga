## Livestatus

To enable the feature livestatus add the following block to the variable `icinga2_features`.

```yaml
icinga2_features:
  - name: livestatus
```

### Feature variables

* `socket_type: string`
  * Specifies the socket type. Can be either tcp or unix.
* `bind_host: string`
  * Host address to listen on for connections.
* `bind_port: int`
  * Port to listen on for connections.
* `socket_path: str`
  * Specifies the path to the UNIX socket file.
* `compat_log_path: str`
  * Path to Icinga 1.x log files. Required for historical table queries. Requires CompatLogger feature enabled.
