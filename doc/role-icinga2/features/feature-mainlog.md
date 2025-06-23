## Mainlog

To enable the feature mainlog add the following block to the variable `icinga2_features`.

```yaml
icinga2_features:
  - name: mainlog
```

### Feature variables

* `severity: string`
  * The minimum severity for this log. Possible values “debug”, “notice”, “information”, “warning” or “critical”.

* `path: string`
  * The Log Path, default: `LogDir + /icinga2.log`

* `state: string`
  * Decides whether the feature is enabled or disabled. Possible values present, absent.
