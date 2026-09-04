## Module Fileshipper

The Icinga Web Fileshipper module provides CSV, JSON, XML and YAML files as an import source for the Icinga Director.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values. For all parameters please check the [module documentation](https://icinga.com/docs/icinga-director/latest/fileshipper/doc/02-Installation/#setup-base-directory).

To also deploy the files from the Ansible control node, add a `files` key to the given resource (`imports`/`directories`).
If entries are removed from `files` or if it is omitted, those files will be removed from the managed node.
If the key `purge_files` is set to `false`, the files will not be deleted. This allows for manual file deployment if necessary.  
The `files` and `purge_files` keys will be removed from the dictionary before writing the configuration files (redefines `icingaweb2_modules`).

The directories for the files will be created automatically, using the joined path of `{{ icingaweb2_fragments_path }}/fileshipper/<imports|directories>/` and `fileshipper.imports.<some_name>.basedir` / `fileshipper.directories.<some_name>.source` (e.g. `/var/tmp/icingaweb/fileshipper/imports/<some_name>/`).  
The use of absolute paths within the `imports` `basedir` and the `directories` `source` is **not supported**!

```yaml
icingaweb2_modules:
  fileshipper:
    enabled: true
    source: package
    imports:
      a_bunch_of_files:
        basedir: bunch_of_files
        # Deploys 'cmdb.json' and 'firewall_rules.yml' to '/var/tmp/icingaweb2/fileshipper/imports/bunch_of_files/'
        files:
          - cmdb.json
          - firewall_rules.yml
      some_more_files:
        basedir: more_files
        files:
          - fileshipper-test.csv
        # Files in '/var/tmp/icingaweb2/fileshipper/imports/more_files/' will not be removed
        purge_files: false
    directories:
      custom_rules:
        source: custom_rules
        target: zones.d/director-global/custom_rules
        extensions: .conf .md
        files:
          - custom_icinga_dsl.conf
```
