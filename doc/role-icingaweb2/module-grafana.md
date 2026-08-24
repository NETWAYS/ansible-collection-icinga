# Module Grafana

This module installs and configures the NETWAYS Grafana module for Icinga Web 2.
It configures the module only. Grafana itself and its data source must be managed separately.

## Requirements

The `icinga-grafana` package is provided by the NETWAYS Extras repository. When managing repositories with the `netways.icinga.repos` role, enable it:

```yaml
netways_repo_extras: true
```

## Example

```yaml
icingaweb2_modules:
  grafana:
    enabled: true
    source: package
    config:
      grafana:
        host: grafana.example.org:3000
        protocol: https
        accessmode: iframe
        defaultdashboard: icinga2-default
        defaultdashboarduid: ad5bxjg
    graphs:
      load:
        dashboarduid: ad5pjfp
        panelId: "1,2,3"
```
