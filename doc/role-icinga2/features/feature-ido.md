## Feature IDO

The feature for the IDO connection installs, enables and configures the object and in
addition is able to import the db_schema. This is only possible if the mysql or
pgsql client binary is available.

> **_NOTE:_** If the database and permissions to connect are available, use the boolean key `import_schema` to enable
the schema import.

All other keys are equal to the object type an can be found in the documentation.

* [IdoPgsqlConnection](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#idopgsqlconnection)
* [IdoMysqlConnection](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#idomysqlconnection)

#### Example MYSQL:

```yaml
icinga2_features:
  - name: idomysql
    host: localhost
    port: 3306
    database: icinga2
    user: icinga2
    password: icinga2
    import_schema: false
    cleanup:
      downtimehistory_age: 48h
      contactnotifications_age: 31d
```

#### Example PGSQL:

```yaml
icinga2_features:
  - name: idopgsql
    host: localhost
    database: icinga2
    user: icinga2
    password: icinga2
    import_schema: true
    cleanup:
      downtimehistory_age: 48h
      contactnotifications_age: 31d
```

### Feature variables

* `host: string`
  * MySQL/PgSQL database host address. Default **localhost**.

* `port: int`
  * Database port. Defaults to **3306** for MySQL and **5432** for PgSQL.

* `database: string`
  * Database name. Defaults to **icinga2**.

* `user: sring`
  * Database user with read/write permission to the icinga database. Defaults to **icinga2**.

* `password: string`
  * Database user’s password.

* `state: string`
  * Decides whether the feature is enabled or disabled. Possible values present, absent.

* `enable_ssl: boolean`
  * Use SSL. Change to true in case you want to use any of the SSL options.

* `ssl_mode: string`
  * **Only PgSQL**: Enable SSL connection mode. Value must be set according to the sslmode setting: prefer, require, verify-ca, verify-full, allow, disable.

* `ssl_key: string`
  * SSL client key file path.

* `ssl_cert: string`
  * SSL certificate file path.

* `ssl_ca: string`
  * SSL certificate authority certificate file path.

* `ssl_capath: string`
  * SSL trusted SSL CA certificates in PEM format directory path.

* `ssl_cipher: string`
  * **Only MySQL**: SSL list of allowed ciphers.

* `socket_path: string`
  * **Only MySQL**: MySQL socket path.

* `table_prefix: string`
  * Database table prefix.

* `instance_name: string`
  * Unique identifier for the local Icinga 2 instance, used for multiple Icinga 2 clusters writing to the same database. Defaults to default.

* `instance_description: string`
  * Description for the Icinga 2 instance.

* `enable_ha: boolean`
  * Enable the high availability functionality. Only valid in a cluster setup.

* `failover_timeout: string`
  * Set the failover timeout in a HA cluster. Must not be lower than 30s. Defaults to 30s

* `cleanup: dict`
  * Dictionary with items for historical table cleanup.

* `categories: list`
  * Array of information types that should be written to the database.

* `import_schema: boolean`
  * Import schema in the database set for the feature.
