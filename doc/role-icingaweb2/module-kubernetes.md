## Module Kubernetes

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
  kubernetes:
    enabled: true
    source: package
    config:
      database:
        resource: kubernetes_db
```
