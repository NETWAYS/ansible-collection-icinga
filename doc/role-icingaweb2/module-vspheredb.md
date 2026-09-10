## Module vSphereDB

Module to monitor a VMware vSphere environment.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

```yaml
icingaweb2_modules:
  vspheredb:
    enabled: true
    source: package
    config:
      db:
        resource: "vspheredb_db"
```
