## Module Graphite

This module only configures the module in Icinga Web and not the graphite backend itself. 

## Variables

### Module Configuration File

The general module parameter like `enabled` and `source` can be applied here.

For the **config** file, create a dictionary with sections as keys and the parameters as values.

Example:

```
icingaweb2_modules:
  graphite:
    enabled: true
    source: package
    config:
      graphite:  # This is the section
        url: 127.0.0.1:9000
        user: graphite
        password: graphitepw
      ui:
        default_time_range: 6

```

#### Section graphite

| Variable | Type   | Example          |
|----------|--------|------------------|
| url      | string | "127.0.0.1:9000" |
| user     | string | "graphite"       |
| password | string | "password"       |
| insecure | number | "1"              |

#### Section ui

| Variable                | Type   | Example |
|-------------------------|--------|---------|
| default_time_range      | number | "1"     |
| defautl_time_range_unit | string | "hours" |
| disable_no_graphs_found | bool   | "0"/"1" |


#### Section icinga

| Variable                              | Type   | Example              |
|---------------------------------------|--------|----------------------|
| graphite_writer_host_name_template    | string | "$host.template$"    |
| graphite_writer_service_name_template | string | "$service.template$" |
| customvar_obscured_check_command      | string | "customvar"          |


### Custom Template Files

Custom templates are good to enhance the graphite basic template library. To include own
graphs and modifications.

To copy them into the templates folder please use the `custom_template_files` dictionary.

The `src_path` will search within any `files/` directory in the Ansible environment.


```
icingaweb2_modules:
  graphite:
    enabled: true
    source: package
    custom_template_files:
      - name: mygraph.ini
        src_path: graphite_templates/mygraph.ini
      - name: myothergraph.ini
        src_path: graphite_templates/myothergraph.ini
```
