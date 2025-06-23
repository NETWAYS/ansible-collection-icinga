## Module x509

### Variables and Configuration

The general module parameter like `enabled` and `source` can be applied here.

| Variable | Value      |
|----------|------------|
| enabled  | true/false |
| source   | package    |

#### Section configuration

The backend database for the module needs to be available and configured at the `icingaweb2_resources` variable.

```yaml
icingaweb2_modules:
  x509:
    source: package
    enabled: true
    config:
      backend:
        resource: x509
```

#### Configure SNI Names.

To configure SNIs for a IP address, use the dictionary `sni`.

Example:

```yaml
icingaweb2_modules:
  x509:
    source: package
    enabled: true
    config:
      backend:
        resource: x509
    sni:
      192.168.56.213:
        hostnames:
          - icinga.com
          - test2.icinga.com
```

#### Import Certificates

To import certificates use the **list** `certificate_files` all files need to be
available locally beforehand.

```yaml
icingaweb2_modules:
  x509:
    source: package
    enabled: true
    config:
      backend:
        resource: x509
    certificate_files:
      - /etc/ssl/certs/ca-certificates.crt
```

#### Database Schema Setup

To import the database schema use `database` dictionary with the following variables.

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `import_schema` | `Boolean` | Defines wether the schema will be imported or not. | false |
| `type` | `String` | Defines the type of database (`mysql \| pgsql`) | **n/a** |
| `host` | `String` | Defines database address to connect to. | `localhost` |
| `port` | `int` | Defines the database port to connect to. | `3306` or `5432` |
| `user` | `string` | Defines database user | `x509` |
| `name` | `String` | Defines the database to connect to. | `x509` |
| `password` | `String` | Defines the database password to connect with. | OMITTED |
| `ssl_mode` | `String` | Clients attempt to connect using encryption, falling back to an unencrypted connection if an encrypted connection cannot be established |**n/a** |
|`ssl_ca`| `String`| Defines the path to the ca certificate for client authentication. | **n/a** |
|`ssl_cert`|`String`| Defines the path to the certificate for client authentication. | **n/a** |
|`ssl_key`| `String` | Defines the path to the certificate key for client key authentication. | **n/a** |
|`ssl_cipher`|`String`| Ciphers for the client authentication. | **n/a** |
|`ssl_extra_options`|`String`| Extra options for the client authentication. | **n/a** |


```yaml
icingaweb2_modules:
  x509:
    source: package
    enabled: true
    database:
      import_schema: true
      type: mysql
      host: localhost
      port: 3306
      user: x509
      password: secret
```
