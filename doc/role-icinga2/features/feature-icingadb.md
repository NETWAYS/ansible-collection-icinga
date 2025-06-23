## IcingaDB

To enable the feature icingadb use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature IcingaDB](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#icingadb)

```yaml
icinga2_features:
  - name: icingadb
    host: localhost
    port: 6380
```

### Feature variables

* `host: string`
  * Redis host for IcingaDB. Defaults to 127.0.0.1.

* `port: int`
  * Redis port for IcingaDB. Defaults to 6380.

* `path: string`
  * Redix unix socket path. Can be used instead of host and port attributes.

* `password: string`
  * Redis auth password for IcingaDB.

* `enable_tls: boolean`
  * Whether to use TLS.

* `cert_path: string`
  * Path to the certificate.

* `key_path: string`
  * Path to the private key.

* `ca_path: string`
  * Path to the CA certificate to use instead of the system’s root CAs.

* `crl_path: string`
  * Path to the CRL file.

* `cipher_list: string`
  * Cipher list that is allowed. For a list of available ciphers run openssl ciphers. Defaults to ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:AES256-GCM-SHA384:AES128-GCM-SHA256.

* `tls_protocolmin: string`
  * Minimum TLS protocol version. Defaults to TLSv1.2.

* `insecure_noverify: boolean`
  * Whether not to verify the peer.

* `connect_timeout: int`
  * Timeout for establishing new connections. Within this time, the TCP, TLS (if enabled) and Redis handshakes must complete. Defaults to 15s.
