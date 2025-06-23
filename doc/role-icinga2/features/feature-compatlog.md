## CompatLog

To enable the feature compatlog use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature CompatLog](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#compatlogger)

```
icinga2_features:
  - name: compatlog
    state: present
    log_dir: "LogDir + /compat"
    rotation_method: "monthly"
```

### Feature variables

* `state: string`
  * Enable or disable feature. Options: present, absent
* `log_dir: string`
  * Set the log directory.
* `rotation_method: string`
  * Set the log rotation interval. Options: hourly, daily, weekly, monthly
