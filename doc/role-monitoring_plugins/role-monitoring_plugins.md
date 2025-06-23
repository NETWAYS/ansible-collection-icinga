# Ansible Role netways.icinga.monitoring_plugins

This role manages the installation/removal of many well known check plugins typically used in monitoring systems.<br>
The list is based on the section *"Plugin Check Commands for Monitoring Plugins"* as seen in the [**Icinga Template Library** (ITL)](https://icinga.com/docs/icinga-2/latest/doc/10-icinga-template-library/#plugin-check-commands-for-monitoring-plugins).

* [List of available check commands](check_command_list.md)

> For Suse based systems you need the Ansible module `zypper`. Refer to the [getting started](https://github.com/NETWAYS/ansible-collection-icinga/blob/main/doc/getting-started.md#requirements) section.

## Variables

- `icinga_monitoring_plugins_epel: boolean`
  Decides whether to activate the epel repository. Default: `false`
  Epel needs to be available to install plugins on RHEL and derivatives.

- `icinga_monitoring_plugins_crb: boolean`<br>
  Decides whether to run the equivalent of `dnf --enablerepo crb ...` when installing the necessary packages. Default: `false`<br>
  Enabling CRB/Powertools may be necessary, depending on the plugins wanted and the repositories already enabled.

- `icinga_monitoring_plugins_dependency_repos: list`
  Decides which repositories are temporarily enabled when installing packages. Defaults to either `crb` or `powertools`.<br>
  If the need arises, you can manually overwrite this variable to temporarily enable one or multiple repositories of your choice.<br>
  You may specify `icinga_monitoring_plugins_dependency_repos: "*"` to temporarily enable every repository present.

- `icinga_monitoring_plugins_remove: boolean`<br>
  Decides whether to remove packages that have not been asked for by the user. Default `true`<br>
  The requested check commands are compared against the list of available check commands. Packages not required for installation are removed.

- `icinga_monitoring_plugins_autoremove: boolean`<br>
  Decides whether to automatically remove unneeded dependencies. Default: `false`

- `icinga_monitoring_plugins_check_commands: list`<br>
  Decides what check plugins will be installed. Default: `undefined`<br>
  An empty list will be accepted.<br>
  If undefined, the role will fail. Also see [List of available check commands](check_command_list.md).

## Check Commands

Check plugins are abreviated only using the base name (`check_apt` becomes `apt`).<br>
They are installed using the according packages provided by the distribution.<br>
This also means that more than the requested check commands might get installed.<br>

To set check plugins to be installed:

```yaml
icinga_monitoring_plugins_check_commands:
    - "ssmtp"
    - "disk"
    - "load"
    - "smtp"
    - "dns"
    ...
```

To install all available check plugins you can add the word 'all' to the list:

```yaml
icinga_monitoring_plugins_check_commands:
    - "all"
```

## Example Playbooks

Install check commands<br>
- disk
- disk_smb
- dns
- tcp
- uptime

```yaml
---

- hosts:
    - host1
  become: yes
  vars:
    icinga_monitoring_plugins_epel: true
    icinga_monitoring_plugins_crb: true
    icinga_monitoring_plugins_check_commands:
      - disk
      - disk_smb
      - dns
      - tcp
      - uptime
  roles:
    - netways.icinga.monitoring_plugins
```

---

Remove all check commands known to this role. Also remove unneeded dependencies.

```yaml
---

- hosts:
    - host1
  become: yes
  vars:
    icinga_monitoring_plugins_autoremove: true
    icinga_monitoring_plugins_check_commands: []
  roles:
    - netways.icinga.monitoring_plugins
```
