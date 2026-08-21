## Module TOTP

TOTP module for Icinga Web for use in two-factor authentication.

## Configuration

This module needs a database to work properly, so you will want to also add a database resource definition to `icingaweb2_resources`.

```yaml
icingaweb2_resources:
  totp_db:
    type: db
    db: mysql
    host: localhost
    dbname: totp
    username: totp_username
    password: totp_password
```

The general module parameter like `enabled` and `source` can be applied here.

```yaml
icingaweb2_modules:
  totp:
    enabled: true
    source: package
    config:
      database:
        resource: totp_db
      settings:
        issuer: Icinga Web 2
        leeway: 15
    database:
      import_schema: true
      host: localhost
      type: mysql
      name: totp
      user: totp_username
      password: totp_password
```

> The `issuer` is what is presented to users as the name for their account within their TOTP authenticator app.
> The `leeway` is the accepted clock drift in seconds and must be between 0 and 29.
