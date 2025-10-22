# Monitoring Objects Configuration

## Objects

By adding the variable `icinga2_objects` the role Icinga 2 will
generate configuration files with objects included.

This variable consists of Icinga 2 object attributes and attributes referring to the file created in the process.

> **_NOTE:_** The second level of the dictionary defines on which host the configuration is created. All objects in the example below, will be gathered and deployed on the host.: `host.example.org`.<br>
In addition this variable can be logically defined at the **host_vars/agent** and are still deployed on the master **host.example.org**.<br>
The second level can **only** be used in **hostvars**!

The `file` key will be used to control in which directory structure the object will be placed.
In addition the `order` key will define the order of the objects in the destination file.
The default for `order` is set to **10**, so everything below that number will be in front of the file, all objects with the order above 10 will be placed later in the file.

The `type` will be the original Icinga 2 object types, a list of all can be found in the documentation. [Icinga 2 Monitoring Objects](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#monitoring-objects)

### Icinga2 Objects in Hostvars

When defining `icinga2_objects` as a host specific variable (hostvars/groupvars) you can define the variable as a dictionary. Each dictionary key represents the host on which the key's value will be deployed as configuration.<br>
Alternatively you can define `icinga2_objects` as a list which results in the configuration being deployed on just the host for which the variable is defined.
Because it's easily overlooked, here are few more words of clarification: The first example shows variables of the host `webserver.example.org` but the `icinga2_objects` variable includes `host.example.org` and an extra level of indentation. This means that the following configuration will not be deployed on `webserver.example.org` but on `host.example.org`. This is especially useful when defining host objects on agents but "sending" them to the central nodes.

Example defining the variable within hostvars as a dictionary (inventory entry):

```yaml
webserver.example.org:
  ansible_host: 10.0.0.8
  icinga2_objects:
    host.example.org:
      - name: "{{ inventory_hostname }}"
        type: Host
        file: "{{ 'conf.d/' + ansible_hostname + '.conf' }}"
        address: "{{ ansible_host }}"
        check_command: hostalive
        check_interval: 3m
      - ...
```

This way you can use some host's variables (like `ansible_host`) to deploy configuration on another host (in this case `host.example.org`).

You can use this variant within a playbook where `host.example.org` is your central Icinga 2 instance. Run it on all agents. They will collect their local facts and the central system `host.example.org` will receive host objects for each agent. This approach will only work if you run the play simultanously on your agents and on your central system.

```
- hosts: icinga2_main:icinga2_agents
  collections:
    - netways.icinga
  pre_tasks:
    - name: Add agent hosts to Icinga 2 objects
      set_fact:
        icinga2_objects:
          host.example.org   // name of the central system
            - name: "{{ inventory_hostname }}"
              type: Zone
              file: "zones.d/{{ monitoring_zone }}/hosts/{{ inventory_hostname }}.conf"
              endpoints:
                - "{{ inventory_hostname }}"
              parent: "{{ monitoring_zone }}"
            - name: "{{ inventory_hostname }}"
              type: Endpoint
              file: "zones.d/{{ monitoring_zone }}/hosts/{{ inventory_hostname }}.conf"
            - name: "{{ inventory_hostname }}"
              type: Host
              file: "zones.d/{{ monitoring_zone }}/hosts/{{ inventory_hostname }}.conf"
              imports:
                - linux-host
              vars:
                distro: "{{ ansible_distribution }}"
                distroversion: "{{ ansible_distribution_version }}"
                arch: "{{ ansible_architecture }}"
              address: "{{ ansible_default_ipv4.address }}"
      when:
        - inventory_hostname in groups["icinga2_agents"]
  roles:
    - netways.icinga.icinga2
```

Example defining the variable within hostvars as a list (inventory entry):

```yaml
webserver.example.org:
  ansible_host: 10.0.0.8
  icinga2_objects:
    - name: "web-api-user"
      type: ApiUser
      file: "{{ 'conf.d/' + ansible_hostname + '.conf' }}"
      password: "somepassword"
      permissions:
        - "objects/query/Host"
        - "objects/query/Service"
    - ...
```

In the above case the list `icinga2_objects` will only be deployed as configuration on host `webserver.example.org`.

Additionally, the list `icinga2_objects` from within a play's `vars` key will be merged with each host's individual objects.

### Icinga2 Objects in Play Vars

If you need to deploy certain Icinga 2 objects on every host in your play, you can define the variable `icinga2_objects` as a list within your play's `vars` key.<br>
This ensures that, **in addition** to the individual host's objects, there is a common set of objects between your hosts.

Example defining the variable within your play's vars:

```yaml
icinga2_objects:
  - name: "GlobalApiUser"
    type: ApiUser
    file: "conf.d/global_api_users.conf"
    order: 20
    password: supersecrectpassword123
    permissions:
      - "objects/query/Host"
      - "objects/query/Service"
```

---

More examples at the end -> [Examples](#examples)

## Managing Config directories

To create or prepare the directories for the monitoring configuration use the variable `icinga2_config_directories`.
Those directories are only managed when they are part of `zones.d`, `conf.d` or the variable `icinga2_confd`.

```yaml
icinga2_config_directories:
  - zones.d/main/hosts/
  - zones.d/main/services/
  - conf.d/commands/
```

### Custom configuration files

In some cases Icinga 2 DSL can be complex and uneasy to write into YAML format. For those scenarios you can provide own files on the
Ansible controller node and let the role deploy the file to your instance.

Create the custom file below an Ansible **files/** directory and use the variable **icinga2_custom_config**

```yaml
icinga2_custom_config:
  - name: myown_command.conf
    path: zones.d/main/myown_command.conf
    order: 10
```

## Parser Rules

The collection provides the possibility to deploy Icinga 2 configuration, this includes configuration to shape the instance and monitoring data to create a complete monitoring environment.

### Basic Syntax

The parser takes every value in the configuration and decides how the value should be written in the configuration. This takes a few rules to handle the configuration the right way.

First of all, to disable the parser use the prefix `-:`.

```yaml
attr: -:"unparsed quoted string"
```

Strings are parsed in chunks, by splitting the original string into separate substrings at specific keywords (operators) such as `+`, `-`, `in`, `&&`, `||`, etc.

**NOTICE:** This splitting only works for keywords that are surrounded by whitespace, e.g.:

```yaml
attr: string1 + string2 - string3
```

The algorithm will loop over the parameter and start by splitting it into 'string1' and 'string2 - string3'. 'string1' will be passed to the sub function 'value_types' and then the algorithm will continue parsing the rest of the string ('string2 - string3'), splitting it, passing it to value_types, etc.

Brackets are parsed for expressions:

```yaml
attr: 3 * (value1 -  value2) / 2
```

The parser also detects function calls and will parse all parameters separately.

```yaml
attr: function(param1, param2, ...)
```

Boolean values can be defined with or without quotes. In addition the Ansible bool types `yes` or `no` can be used either.

```python
attr: true or attr: 'true'
```

To avoid overlapping syntax with Ansible variable syntax, please refer to single quotes `' '` when using own lambda functions in Icinga.

```jinja
attrs => '{{ ... }}'
```

In general all values can be defined without quotes except for lamba functions where Ansible's own syntax would interfere with the double brackets.

| Type           | Examples                                 |
|----------------|------------------------------------------|
| Boolean        | `true`,`false`,`True`,`False`,`yes`,`no` |
| Numbers        | `2` or `3.5`                             |
| Time Intervals | `3m` or `3.5h`                           |
| String         | `attr: string`                           |

### Advanced Syntax

To replicate Icinga 2 advanced syntax like assignments with `+=` or `-=` you can use the prefix `+` or `-`.

To create the following Icinga 2 DSL syntax,
```python
var += config
```
simply use a string with the prefix `+` e.g.

```yaml
var: `+ config`
```

Because of the blank between the `+` and `config` those values are separately parsed and therefore numbers are also possible. For numbers we also can build `-=`, just use the minus sign `-`. This method will work for every attribute or custom attribute.

```python
attr: + -14 or attr: - -14
```

The parser is able to merge or reduce an array. For this method set the first item of your array as `+` or `-` sign.

```yaml
attr:
  - +
  - item1
  - item2

# Alterntive syntax
attr: ['-','item1','item2']
```
Result in Icinga will be `attr += [ "item1", "item2", ]`.

To reduce arrays use the minus sign `-`.

**NOTICE** Please be aware that the minus sign needs to be quoted otherwise the Ansible parser will have troubles reading the array.

```yaml
attr:
  - '-'
  - item1
  - item2

# Alterntive syntax
attr: ['-','item1','item2']
```

Result in Icinga will be `attr -= [ "item1", "item2", ]`.

#### Dictionaries

To merge dictionaries we can use the plus sign `+`. The plus sign needs to be a key in the dictionary. See following example.

```yaml
attr:
  +: true
  key1: value1
```

The result:

```ini
attr["key1"] = "value1"
```

The useage of levels in dictionaries aren't limited.

```yaml
attr:
  key1:
    key2:
      key3:
        +: true
        value: test
```

Result:

```ini
vars.attr["key1"] = {
    key2 = {
      key3 += {
        value = "test"
      }
    }
  }
```

### Examples:

#### Host Template

```yaml
icinga2_objects:
[...]
    - name: generic-host
      type: Host
      file: zones.d/main/hosts/template.conf
      check_command: hostalive
      check_interval: 3m
      template: true
```

#### Host

```yaml
icinga2_objects:
  host.example.org:
    - name: agent.example.org
      type: Host
      file: zones.d/main/hosts.conf
      imports:
        - generic-host
      groups:
        - linux-hosts
      address: 192.168.2.10
      vars:
        os: linux

```

#### Host Group

```yaml
icinga2_objects:
[...]
    - name: linux-host
      type: HostGroup
      file: zones.d/main/hostgroups.conf
      display_name: Linux Server
      assign:
        - host.vars.os == Linux
```

#### Service Template

```yaml
icinga2_objects:
[...]
    - name: generic-service
      type: Service
      file: zones.d/main/services/template.conf
      check_interval: 300s
      retry_interval: 30s
      order: 1
      template: true
```

#### Service Apply

```yaml
icinga2_objects:
[...]
  - name: ping
    type: Service
    order: 11
    file: zones.d/main/services.conf
    apply: true
    imports:
      - generic-service
    check_command: ping4
    assign:
      - host.address
```

#### Service Apply for

```yaml
[...]
  - name: ping
    type: Service
    apply: true
    apply_for: config in host.vars.ips
    check_command: ping4
    vars: + config
    assign:
      - host.vars.ips
```

#### Service Object

```yaml
icinga2_objects:
[...]
  - name: ping6
    type: Service
    file: zones.d/main/agent.localdomain.conf
    imports:
      - generic-service
    check_command: ping6
    host_name: agent.localdomain
```

#### Service Group

```yaml
icinga2_objects:
[...]
  - name: service_group_linux
    type: ServiceGroup
    file: "local.d/groups.conf"
    display_name: Linux Services
    assign:
      - host.vars.os == linux
```

#### ApiUser

```yaml
icinga2_objects:
[...]
  - name: icinga-api
    type: ApiUser
    file: "local.d/apiuser.conf"
    password: supersecrectpassword123
    permissions:
      - "objects/query/Host"
      - "objects/query/Service"
```

#### TimePeriod

```yaml
icinga2_objects:
[...]
- name: 24x7
  type: TimePeriod
  file: "local.d/timeperiods.conf"
  ranges:
    monday: "00:00-24:00"
    tuesday: "00:00-24:00"
    wednesday: "00:00-24:00"
    thursday: "00:00-24:00"
    friday: "00:00-24:00"
```

#### Endpoint

```yaml
icinga2_objects:
[...]
  - name: agent.localdomain
    type: Endpoint
    file: zones.d/main/hosts/agent.localdomain
    host: 10.10.10.10
```

#### Zone

```yaml
icinga2_objects:
[...]
  - name: agent.localdomain
    type: Zone
    file: zones.d/main/hosts/agent.localdomain
    endpoints:
      - agent.localdomain
```

#### ScheduledDowntime

```yaml
icinga2_objects:
[...]
  - name: webserver_downtime
    type: ScheduledDowntime
    display_name: "webserver_downtime"
    host_name: "web1.localdomain"
    author: "icingaadmin"
    comment: "web server maintenance"
    fixed: false
    file: zones.d/main/downtime.conf
    ranges:
        "sunday": "10:00-11:00"
```

#### Notification Template

```yaml
icinga2_objects:
[...]
  - name: notification-template
    type: Notification
    command: generic-notification
    file: zones.d/main/notification/template.conf
    template: true
```

#### Notification

```yaml
icinga2_objects:
[...]
  - name: notification-to-rhel-host
    type: Notification
    file: zones.d/main/notification.conf
    imports:
      - notification-template
    user_groups: ['administrators']
    apply: true
    apply_target: Host
    assign:
      - match(*web, host.name) && (host.vars.customer == customer-xy)
    ignore:
      - match(host.vars.os_family == Debian)
```

#### User

```yaml
[...]
  - name: admin
    type: User
    period: "24x7"
    groups: [ administrators ]
    email: "icinga@localhost"
    states: [ OK, Warning, Critical, Unknown ]
    types: [ Problem, Recovery ]
    file: zones.d/main/users.conf
```

#### NotificationCommand

```yaml
icinga2_objects:
[...]
  - name: service-notification-command
    command: [ ConfigDir + /scripts/mail-service-notification.sh ]
    type: NotificationCommand
    file: zones.d/main/notification_command.conf
    arguments:
      +: true
      -4:
        required: true
        value: $notification_address$
        description: The notification address
      -6: $notification_address6$
      -b: $notification_author$
    vars:
      +: true
      notification_address: $address$
      notification_address6: $address6$
      notification_author: $notification.author$
```

#### UserGroup

```yaml
[...]
  - name: administrators
    type: UserGroup
    display_name: Admins
    file: zones.d/main/groups.conf
```

#### CheckCommand

```yaml
icinga2_objects:
[...]
  - name: http
    command: [ PluginDir + /check_http ]
    type: CheckCommand
    file: zones.d/main/check_command.conf
    arguments:
      -H: $http_vhost$
      -S:
        set_if: $http_ssl$
```

#### CompatLogger

```yaml
icinga2_objects:
[...]
  - name: mycompatlogger
    type: CompatLogger
    file: "local.d/complog.conf"
    log_dir: "LogDir + /custom_complog"
    rotation_method: "hourly"
```

#### Dependency

```yaml
- name: dependency-to-host
  type: Dependency
  apply: true
  apply_target: Host
  file: zones.d/main/dependencies.conf
  parent_host_name: router.localdomain
  disable_checks: true
  disable_notifications: true
  states:
    - Up
  assign:
    - host.name == agent.localdomain
```

#### EventCommand

```yaml
- name: restart-httpd-event
  type: EventCommand
  file: zones.d/main/eventcommands.conf
  command: /opt/bin/restart-httpd.sh
```
