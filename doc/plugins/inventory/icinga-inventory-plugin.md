# Icinga as an Inventory Source for Ansible

- [Requirements](#requirements)
- [Variables](#variables)
- [Using Constructed Inventory and Cache](#using-constructed-inventory-and-cache)
- [Filter Options](#filter-options)

There is a lot of Ansible Inventory Plugins to pull host information from different sources. This allows for dynamic inventories that adapt to changes made in other applications.<br>
Using this plugin you can use Icinga 2's API to build your Ansible Inventory.

For this to work you need to create a file ending in either `icinga.yml` or `icinga.yaml` and fill it with all required variables to fetch information from your Icinga 2 API.

> If you need further information, be sure to pass `-vvv` to your Ansible command to get additional information. This will for example tell you what filter is used by the plugin when querying Icinga's API.

Example:

**inventory-icinga.yml:**

```yaml
---
plugin: netways.icinga.icinga
user: api-user
password: api-user-password
```

```bash
ansible -i inventory-icinga.yml localhost -m debug -a "msg='{{ groups }}'"
```

```yaml
localhost | SUCCESS => {
    "msg": {
        "all": [
            "icinga-master",
            "dummy_host_1",
            "dummy_host_2",
            "dummy_host_3",
            "dummy_host_4",
            "dummy_host_5",
            "test"
        ],
        "icinga_group_testgroup1": [
            "test"
        ],
        "icinga_group_test_group_2": [
            "test"
        ],
        "icinga_zone_main": [
            "icinga-master",
            "dummy_host_1",
            "dummy_host_2",
            "dummy_host_3",
            "dummy_host_4",
            "dummy_host_5"
        ],
        "icinga_zone_test": [
            "test"
        ],
        "ungrouped": []
    }
}
```

Variables of host `icinga-master`:

```bash
ansible -i inventory-icinga.yml localhost -m debug -a "msg='{{ hostvars[\"icinga-master\"] }}'"
```

```yaml
icinga-master | SUCCESS => {
    "msg": {
        "ansible_check_mode": false,
        "ansible_config_file": "/home/matthias/.ansible.cfg",
        "ansible_diff_mode": false,
        "ansible_facts": {},
        "ansible_forks": 5,
        "ansible_inventory_sources": [
            "/home/matthias/Ansible/inventory-icinga.yml"
        ],
        "ansible_playbook_python": "/usr/bin/python",
        "ansible_verbosity": 0,
        "ansible_version": {
            "full": "2.15.3",
            "major": 2,
            "minor": 15,
            "revision": 3,
            "string": "2.15.3"
        },
        "group_names": [
            "icinga_os_linux",
            "icinga_zone_main"
        ],
        "groups": {
            "all": [
                "icinga-master",
                "dummy_host_1",
                "dummy_host_2",
                "dummy_host_3",
                "dummy_host_4",
                "dummy_host_5",
                "test"
            ],
            "icinga_group_testgroup1": [
                "test"
            ],
            "icinga_group_test_group_2": [
                "test"
            ],
            "icinga_zone_main": [
                "icinga-master",
                "dummy_host_1",
                "dummy_host_2",
                "dummy_host_3",
                "dummy_host_4",
                "dummy_host_5"
            ],
            "icinga_zone_test": [
                "test"
            ],
            "ungrouped": []
        },
        "icinga___name": "icinga-master",
        "icinga_acknowledgement": 0,
        "icinga_acknowledgement_expiry": 0,
        "icinga_acknowledgement_last_change": 0,
        "icinga_action_url": "",
        "icinga_active": true,
        "icinga_address": "icinga-master",
        "icinga_address6": "",
        "icinga_check_attempt": 1,
        "icinga_check_command": "hostalive",
        "icinga_check_interval": 300,
        "icinga_check_period": "",
        "icinga_check_timeout": null,
        "icinga_command_endpoint": "",
        "icinga_display_name": "Icinga-Master",
        "icinga_downtime_depth": 0,
        "icinga_enable_active_checks": true,
        "icinga_enable_event_handler": true,
        "icinga_enable_flapping": false,
        "icinga_enable_notifications": true,
        "icinga_enable_passive_checks": true,
        "icinga_enable_perfdata": true,
        "icinga_event_command": "",
        "icinga_executions": null,
        "icinga_flapping": false,
        "icinga_flapping_current": 0,
        "icinga_flapping_ignore_states": null,
        "icinga_flapping_last_change": 0,
        "icinga_flapping_threshold": 0,
        "icinga_flapping_threshold_high": 30,
        "icinga_flapping_threshold_low": 25,
        "icinga_force_next_check": false,
        "icinga_force_next_notification": false,
        "icinga_groups": [],
        "icinga_ha_mode": 0,
        "icinga_handled": false,
        "icinga_icon_image": "",
        "icinga_icon_image_alt": "",
        "icinga_last_check": 1693814617.791436,
        "icinga_last_check_result": {
            "active": true,
            "check_source": "icinga-master",
            "command": [
                "/usr/lib/nagios/plugins/check_ping",
                "-H",
                "icinga-master",
                "-c",
                "5000,100%",
                "-w",
                "3000,80%"
            ],
            "execution_end": 1693814617.791384,
            "execution_start": 1693814613.71081,
            "exit_status": 0,
            "output": "PING OK - Packet loss = 0%, RTA = 0.02 ms",
            "performance_data": [
                "rta=0.019000ms;3000.000000;5000.000000;0.000000",
                "pl=0%;80;100;0"
            ],
            "previous_hard_state": 99,
            "schedule_end": 1693814617.791436,
            "schedule_start": 1693814613.71,
            "scheduling_source": "icinga-master",
            "state": 0,
            "ttl": 0,
            "type": "CheckResult",
            "vars_after": {
                "attempt": 1,
                "reachable": true,
                "state": 0,
                "state_type": 1
            },
            "vars_before": {
                "attempt": 1,
                "reachable": true,
                "state": 0,
                "state_type": 1
            }
        },
        "icinga_last_hard_state": 0,
        "icinga_last_hard_state_change": 1691570988.637088,
        "icinga_last_reachable": true,
        "icinga_last_state": 0,
        "icinga_last_state_change": 1691570988.637088,
        "icinga_last_state_down": 0,
        "icinga_last_state_type": 1,
        "icinga_last_state_unreachable": 0,
        "icinga_last_state_up": 1693814617.791384,
        "icinga_max_check_attempts": 3,
        "icinga_name": "icinga-master",
        "icinga_next_check": 1693814916.361451,
        "icinga_next_update": 1693815224.5242188,
        "icinga_notes": "",
        "icinga_notes_url": "",
        "icinga_original_attributes": null,
        "icinga_package": "director",
        "icinga_paused": false,
        "icinga_previous_state_change": 1691570988.637088,
        "icinga_problem": false,
        "icinga_retry_interval": 60,
        "icinga_severity": 0,
        "icinga_source_location": {
            "first_column": 0,
            "first_line": 1,
            "last_column": 32,
            "last_line": 1,
            "path": "/var/lib/icinga2/api/packages/director/45f7ec2e-7aee-4110-a414-e32f6228e7ea/zones.d/main/hosts.conf"
        },
        "icinga_state": 0,
        "icinga_state_type": 1,
        "icinga_templates": [
            "icinga-master",
            "Default Host"
        ],
        "icinga_type": "Host",
        "icinga_vars": {
            "operating_system": "linux"
        },
        "icinga_version": 0,
        "icinga_volatile": false,
        "icinga_zone": "main",
        "inventory_dir": "/home/matthias/Ansible",
        "inventory_file": "/home/matthias/Ansible/inventory-icinga.yml",
        "inventory_hostname": "icinga-master",
        "inventory_hostname_short": "icinga-master",
        "playbook_dir": "/home/matthias/Ansible"
    }
}
```

## Requirements

This inventory plugin needs
- Python `requests` library to make API calls to Icinga 2

## Variables

**plugin**

This is a token that ensures that the plugin definitions are meant for this inventory plugin.<br>
The form is `namespace.collection_name.plugin_name`.

This must be `netways.icinga.icinga`

Required: `true`<br>
Type: `string`<br>
Default: `None`

---

**url**

The url to be used for API requests.

Required: `false`<br>
Type: `string`<br>
Default: `https://localhost`

---

**port**

The port used by Icinga 2.

Required: `false`<br>
Type: `int`<br>
Default: `5665`

---

**user**

The username to be used for API requests.

Required: `true`<br>
Type: `string`<br>
Default: `None`

---

**password**

The password to be used for API requests.

Required: `true`<br>
Type: `string`<br>
Default: `None`

---

**validate_certs**

Whether the certificates received when requesting the API should be validated to establish trust.

Required: `false`<br>
Type: `bool`<br>
Default: `true`

---

**ansible_user_var**

You may decide to define the username for Ansible to connect as within your Icinga 2 host object. This allows the inventory to dynamically adapt the Ansible variable `ansible_user`.

Required: `false`<br>
Type: `string`<br>
Default: `None`

---

**filters**

The `filters` variable allows for filtering the Icinga 2 hosts to be used within Ansible. In the background [Icinga 2 API filters](https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#filters) are used.<br>
Options for the `filters` variable are explained in [their own section](#filter-options).

---

**group_prefix**

The inventory plugin automatically builds Ansible groups based on the Icinga 2 host object attributes `groups` and `zone`.<br>
This prefix is used as a prefix for those groups within Ansible.

By default groups will be prefixed with `icinga_group_` and `icinga_zone_` respectively.

Required: `false`<br>
Type: `string`<br>
Default: `icinga_`

---


**want_ipv4**

It is common practice to set an Icinga 2 host's name equal to its FQDN. This way DNS is the source of truth. But you may want to use a host's IP address for connections made by Ansible.<br>
If `want_ipv4` is true, the Ansible variable `ansible_host` will be set to the Icinga host's `address` attribute if applicable.<br>
`want_ipv4` takes precedence over `want_ipv6`.

Required: `false`<br>
Type: `bool`<br>
Default: `false`

---

**want_ipv6**

Analogous to `want_ipv4` you may want to use a Icinga host's `address6` attribute to establish connections using Ansible.<br>
If `want_ipv6` is true, the Ansible variable `ansible_host` will be set to the Icinga host's `address6` attribute if applicable.<br>
`want_ipv4` takes precedence over `want_ipv6`.

Required: `false`<br>
Type: `bool`<br>
Default: `false`

---

**vars_prefix**

All attributes of an Icinga 2 host will be used as host variables within Ansible. Those variables are prefixed with the `vars_prefix`.

Required: `false`<br>
Type: `string`<br>
Default: `icinga_`

---

## Using Constructed Inventory and Cache

Other than the variables used for this plugin explicitly, you can also make use of some options offered by Ansible's Inventory Module [**Constructed**](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/constructed_inventory.html).<br>
Specifically `keyed_groups` might be useful. This allows you to build new Ansible groups based on Icinga host attributes, e.g. `vars["operating_system"]`.

Example:

**inventory-icinga.yml:**

```yaml
---
plugin: netways.icinga.icinga
user: api-user
password: api-user-password

groups:
    # simple name matching
    dummies: inventory_hostname.startswith('dummy')

keyed_groups:
  - prefix: "icinga_os"
    key: vars["operating_system"]
```

```bash
ansible -i inventory-icinga.yml localhost -m debug -a "msg='{{ groups }}'"
```

```yaml
localhost | SUCCESS => {
    "msg": {
        "all": [
            "icinga-master",
            "dummy_host_1",
            "dummy_host_2",
            "dummy_host_3",
            "dummy_host_4",
            "dummy_host_5",
            "test"
        ],
        "dummies": [
            "dummy_host_1",
            "dummy_host_2",
            "dummy_host_3",
            "dummy_host_4",
            "dummy_host_5"
        ],
        "icinga_group_testgroup1": [
            "test"
        ],
        "icinga_group_test_group_2": [
            "test"
        ],
        "icinga_os_linux": [
            "icinga-master"
            "dummy_host_1",
            "dummy_host_2"
        ],
        "icinga_os_windows": [
            "dummy_host_3",
            "dummy_host_4",
            "dummy_host_5"
        ],
        "icinga_zone_main": [
            "icinga-master",
            "dummy_host_1",
            "dummy_host_2",
            "dummy_host_3",
            "dummy_host_4",
            "dummy_host_5"
        ],
        "icinga_zone_test": [
            "test"
        ],
        "ungrouped": []
    }
}
```

---

In order to minimize API queries made against Icinga you might want to use cache and retrieve host information this way.<br>
The following is an example on how to use the Ansible builtin cache plugin `jsonfile`.

```yaml
---
plugin: netways.icinga.icinga
user: api-user
password: api-user-password

cache: true
cache_plugin: "jsonfile"
cache_connection: "/tmp/icinga_cache"
cache_timeout: 1800
```

Here the plugin is told to
- use cache
- use the `jsonfile` cache plugin
- use `/tmp/icinga_cache` as its cache directory
- only use cache that is newer than `1800` seconds / 30 minutes

If cache is used and the cache is valid, no API calls are made.

## Filter Options

You might want to restrict which hosts are part of the API query result. You can for example choose to only fetch host information for hosts within a specific Icinga zone.<br>
If you use custom variables like e.g. *'operating_system'* to distinguish between different operating systems, you can use those variables to narrow down the results.

Valid subkeys for `filters` are
- name
- group
- zone
- custom
- vars

The subkeys 'name', 'group' and 'zone' are meant as defaults that allow for quick filtering based on those Icinga host attributes.<br>
Internally Icinga's '**match**' filter is used for 'name' and 'zone'. This way string and boolean comparisons can be made while also allowing for pattern matching.<br>
'group' uses the '**in**' filter to check membership.

The following example shows filters to restrict the result to hosts
- that are part of **either** zone 'main' or zone 'satellite'
- whose names begin with 'dummy' (matching a pattern)
- that are part of the group 'linux\_hosts'

**Example**

Using CURL:

```
curl -k -u 'api-user':'api-user-password' -H 'X-HTTP-Method-Override: GET' -X POST https://localhost:5665/v1/objects/hosts -d '{ "filter": "((match(\"main\", host.zone)||match(\"satellite\", host.zone)))&&((match(\"dummy*\", host.name)))&&(((\"linux_hosts\" in host.groups)))" }'
```

Using the plugin:

```yaml
---
plugin: netways.icinga.icinga
user: api-user
password: api-user-password

filters:
  zone:
    - main
    - satellite
  name:
    - dummy*
  group:
    - linux_hosts
```

In general, all subkeys of `filters` have to evaluate to true **simultaneously**. In the example above 'zone', 'name' and 'group' **must** all match.<br>
Within one of those filter options **only one** of the list's elements must match.

It is also possible to negate entries. In that case **either** entry in the list has to match while **neither** of the negated entries is allowed to match.

To illustrate the logic, we will use 'group' as an example.

```yaml
group:
  - 'linux_hosts'
  - 'windows_hosts'
  - '!dns-server'
  - '!web-server'
```

Logically this results in: ( in group 'linux_hosts' **OR** in group 'windows_hosts' ) **AND** ( **not** in group 'dns-server' **AND** **not** in group 'web-server' )

---

The 'custom' option lets you simply supply your own filter as it would be passed with CURL (`'{ "filter": "YOUR CUSTOM FILTER" }'`).<br>
Supplying multiple filters will use logic AND to combine them.

The last subkey you can use is 'vars'. It behaves slightly differently since one cannot anticipate the variables other people might use.<br>
Therefore you have to manually decide on the filter and the custom variable to be used.

Currently the '**match**', '**in**' and '**is**' filters are supported. As before all their subkeys have to match with only one entry that has to match while none of the negated entries are allowed to match.

The '**is**' is filter is special in that regard that here you are supposed to only pass one value to it. If multiple values are passed, only the first value in the list will be used.<br>
Also, negation is only allowed for 'set' and 'null' using the '**is**' filter.

The following values are accepted:
- true
- false
- set
- !set
- null
- !null

The value 'set' allows to check if the value of variable either evaluates to `true` or is set, meaning the variable **has** a value that is not `false` and not `null`.

Example:

```yaml
---
plugin: netways.icinga.icinga
user: api-user
password: api-user-password

filters:
  vars:
    match:
      linux_distribution:
        - '!ubuntu'
        - 'debian'
        - 'centos'
        - 'rhel'
        - 'suse'
    in:
      services:
        - 'dns'
        - 'database'
    is:
      ansible_managed: true
      ansible_user: set
```

This results in the following filter: `((match(\"debian\", host.vars.linux_distribution)||match(\"centos\", host.vars.linux_distribution)||match(\"rhel\", host.vars.linux_distribution)||match(\"suse\", host.vars.linux_distribution))&&(!match(\"ubuntu\", host.vars.linux_distribution))&&((\"dns\" in host.vars.services)||(\"database\" in host.vars.services))&&(host.vars.ansible_managed==true))`

Prettier version:

```
(
  (
    match(\"debian\", host.vars.linux_distribution)||match(\"centos\", host.vars.linux_distribution)||match(\"rhel\", host.vars.linux_distribution)||match(\"suse\", host.vars.linux_distribution)
  )
  &&
  (
    !match(\"ubuntu\", host.vars.linux_distribution)
  )
  &&
  (
    (\"dns\" in host.vars.services)||(\"database\" in host.vars.services)
  )
  &&
  (
    host.vars.ansible_managed==true
  )
  &&
  (
    host.vars.ansible_user
  )
)
```
