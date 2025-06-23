## Module Icinga Business Process Modeling

The module Icinga Business Process Modeling provides a visualization for hierarchical business processes based on objects monitored by Icinga.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values. For all parameters please check the [module documentation](https://icinga.com/docs/icinga-business-process-modeling/latest/doc/01-About/)



Example:
```yaml
icingaweb2_modules:
  businessprocess:
    enabled: true
    source: package
```

### Custom Process Files:

Custom process files are a great way to transfer existing business process configurations into the Business Process Modeling Module.

To copy existing processes into the processes folder please use the `custom_process_files` dictionary.

The `src_path` will search within any `files/` directory in the Ansible environment.
```yaml
icingaweb2_modules:
  businessprocess:
    enabled: true
    source: package
    custom_process_files:
      - name: test.conf
        src_path: processes/test.conf
```
