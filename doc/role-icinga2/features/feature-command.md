## Command

To enable the feature command use the following block in the variable `icinga2_features`.

**INFO** For detailed information and instructions see the Icinga 2 Docs. [Feature Command](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#externalcommandlistener)

```yaml
icinga2_features:
  - name: command
    state: present
    command_path: /var/run/icinga2/cmd/icinga2.cmd
```

### Feature variables

* `state: string`
  * Enable or disable feature. Options: present, absent
