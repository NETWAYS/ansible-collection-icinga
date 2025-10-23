# Role netways.icinga.ifw

This role manages the installation/removal of [Icinga for Windows](https://icinga.com/docs/icinga-for-windows/latest/doc/000-Introduction/) components.  
It first installs the [Icinga PowerShell Framework](https://github.com/Icinga/icinga-powershell-framework) in case it is not present yet and then goes on to use the framework's commands to manage other components.

Tasks it can do:

* Install the Icinga PowerShell Framework
* Manage repositories (no locally synced repositories yet)
* Configure the Icinga 2 Agent
* Create a valid Icinga 2 certificate

Tasks it will not do:

* Management of custom Monitoring Plugins
* Management of firewall rules outside of Icinga for Windows (like allowing ICMP echo request)
* Management of Check Commands (available as Icinga Config or Director Basket)
* Management of Background Daemons (available via module `ifw_backgrounddaemon`)
* Management of what commands are allowed by the API Check Forwarder (available via module `ifw_restapicommand`)

Table of contents:

* [Variables](#variables)
  * [Getting a Certificate](#getting-a-certificate)
* [Example Playbooks](#example-playbooks)
  * [Install Basic Components](#install-basic-components)
  * [Install Other Plugins](#install-other-plugins)
  * [Add Custom Repositories](#add-custom-repositories)
  * [Icinga 2 Setup](#icinga-2-setup)
* [Additional Tasks](#additional-tasks)

## Variables

The default values for some variables - like the ones for JEA and the API feature - are considered best practice. Though, feel free to adjust them to your needs.

- `ifw_framework_url: string`  
  The URL to the different verions of the Icinga PowerShell Framework.  
  Default: `https://packages.icinga.com/IcingaForWindows/stable/framework/`

- `ifw_framework_version: string`  
  The version of the Icinga PowerShell Framework to install. You can set a specific version here like `1.11.1`.  
  This is only used for the initial installation of the framework. Updates can be done using `ifw_components`.  
  Default: `latest`

- `ifw_framework_path: string`  
  The path where the Icinga PowerShell Framework should be installed. If unspecified, the role will try using the best available path.

- `ifw_repositories: list of dictionaries`  
  Here you can specify additional repositories from which to pull components from. The default Icinga For Windows repository will always be added.  
  Default: `none`  
  Example:  
  ```yaml
  ifw_repositories:
    - name: "Custom"
      remote_path: "https://example.com/IcingaForWindows/stable/ifw.repo.json"
  ```

- `ifw_components: list of dictionaries`  
  Specify which components should be present. Optionally specify which version of the component should be installed.  
  Components installed but not present within this list will be removed.  
  Default: `[ { name: "plugins", state: "present" }, { name: "agent", state: "present" } ]`

- `ifw_icinga2_user: string`  
   The user Icinga 2 runs as. This user is only used if `ifw_jea_managed_user=false`.  
   Default: `NT Authority\NetworkService`

- `ifw_icinga2_ca_host: string`  
  The Ansible inventory hostname of your Icinga 2 CA host (master).  
  This variable is used to sign the certificate for your Windows host using delegated tasks.  
  If `ifw_icinga2_ticket` is set, the ticket will take precedence.  
  Default: `none`

- `ifw_icinga2_ticket: string`  
  The ticket obtained from your Icinga 2 CA host (master) using `icinga2 pki ticket --cn "<COMMON_NAME>"`.  
  It is used to receive a valid certificate.  
  Default: `none`

- `ifw_connection_direction: string`  
  This variable decides whether your host should connect to its parent(s), its parent(s) to the host, or if connection should be established from both sides.  
  This influences the firewall rules that are automatically deployed.  
  In a well structured Icinga environment the master(s) (or satellite(s)) should not connect to the agent, but the agent should connect "up" to its parent(s).  
  Default: `fromagent`

- `ifw_force_newcert: boolean`  
  If set to true, this forces the generation of a new certificate.  
  Default: `false`

- `ifw_icinga2_cn: string`  
  This variable is used to define what common name your host takes within the Icinga hierarchy. Certificates will be generated using that name.  
  Default: `"{{ inventory_hostname }}"`

- `ifw_icinga2_port: int`  
  This number is used for the local port on which your host should listen.  
  Default: `5665`

- `ifw_icinga2_global_zones: list of strings`  
  Here you can specify all global zones your host should be aware of.  
  Default: `[]`

- `ifw_icinga2_parents: list of dictionaries`  
  Here you can specify the parent endpoint(s) of your host's parent zone (`ifw_icinga2_parent_zone`).  
  You can specify each parent's `cn`, its `host` attribute and the `port` on which it listens. The `cn` attribute is **required**.  
  Default: `none`  
  Example:
  ```yaml
  ifw_icinga2_parents:
    - cn: parent1
      host: icinga01.example.com
      port: 5665
    - cn: parent2
      host: 10.0.0.20
      port: 6556
  ```

- `ifw_icinga2_parent_zone: string`  
  The name of your parent(s) zone.  
  Default: `none`

- `ifw_jea_install: boolean`  
  Whether to install the Icinga for Windows JEA profile.  
  If `ifw_jea_managed_user=false`, the JEA will profile will be created and registered.  
  If `ifw_jea_managed_user=true`, the service user 'icinga' will also be created to run Icinga for Windows as.  
  If both `ifw_jea_install=true` and `ifw_jea_managed_user=true`, `ifw_icinga2_user` will essentially be ignored.  
  [Read more about Icinga for Windows and JEA](https://icinga.com/docs/icinga-for-windows/latest/doc/130-JEA/01-JEA-Profiles/).  
  Default: `true`

- `ifw_jea_managed_user: boolean`  
  Whether to use the Icinga for Windows service user 'icinga' when `ifw_jea_install=true`.  
  Default: `true`

- `ifw_api_feature: boolean`  
  Whether to enable the Icinga for Windows API Check Forwarder.  
  [Read more about the Icinga for Windows API Check Forwarder](https://icinga.com/docs/icinga-for-windows/latest/doc/110-Installation/30-API-Check-Forwarder/).  
  Default: `true`


### Getting a Certificate

If neither `ifw_icinga2_ca_host` nor `ifw_icinga2_ticket` is specified, your target host will connect to the first parent in `ifw_icinga2_parents` and file a CSR. This needs to be signed manually afterwards.

If `ifw_icinga2_ca_host` is specified, a CSR is created locally and then moved to `ifw_icinga2_ca_host` where it is signed. The resulting certificate is then moved back to your target host.

If `ifw_icinga2_ticket` is specified, `ifw_icinga2_ca_host` is ignored and the certificate should get signed automatically. `ifw_icinga2_ticket` needs to be acquired beforehand.

## Example Playbooks

The examples below showcase different aspects of the Icinga for Windows configuration. In a real scenario the variables from the examples should be used in conjunction.

### Install Basic Components

This installs just the Icinga PowerShell Framework, the Agent component and the Icinga PowerShell Plugins.

```yaml
- name: Run ifw role
  hosts: all

  roles:
    - netways.icinga.ifw
```

### Install Other Plugins

This installs the Agent component, the basic plugins and in addition to that the plugins for MSSQL and HyperV.  
It also pins the Agent component to a specific version.

```yaml
- name: Run ifw role
  hosts: all

  vars:
    ifw_components:
      - name: "agent"
        version: "2.14.0"
      - name: "plugins"
      - name: "mssql"
      - name: "hyperv"

  roles:
    - netways.icinga.ifw
```

### Add Custom Repositories

This adds more repositories to Icinga for Windows in addition to the default one.  
This is useful if you want to host a local mirror.

```yaml
- name: Run ifw role
  hosts: all

  vars:
    ifw_repositories:
      - name: "Ansible Managed"
        remote_path: "https://example.com/IcingaForWindows/stable/ifw.repo.json"

  roles:
    - netways.icinga.ifw
```

### Icinga 2 Setup

This installs the Agent component and sets it up to communicate with both its parents.  
It adds the global zone `windows-agents`.

```yaml
- name: Run ifw role
  hosts: all

  vars:
    ifw_icinga2_ca_host: icinga01.example.com

    ifw_icinga2_global_zones:
      - "windows-agents"

    ifw_icinga2_parent_zone: main

    ifw_icinga2_parents:
      - cn: main01
        host: icinga01.example.com
        port: 5665
      - cn: main02
        host: 10.0.0.20
        port: 5665

  roles:
    - netways.icinga.ifw
```


## Additional Tasks

This is meant as a hint for additional tasks you may need but which are not covered by Icinga for Windows and this role.

This will use [`community.windows.win_firewall_rule`](https://docs.ansible.com/ansible/latest/collections/community/windows/win_firewall_rule_module.html) to allow ICMP (echo request) in all network zones, so default host checks like `hostalive` work.

```yaml
- name: Allow ICMP (echo request) in firewall
  community.windows.win_firewall_rule:
    state: present
    name: "{{ item.name }}"
    enabled: true
    profiles: "{{ item.profiles }}"
    action: "{{ item.action }}"
    direction: "{{ item.direction }}"
    protocol: "{{ item.protocol }}"
    icmp_type_code: "{{ item.icmp_type }}"
  loop:
    - name: "Allow inbound ICMPv4 (echo request)"
      direction: "in"
      protocol: "icmpv4"
      icmp_type:
        - "8:*"
      action: "allow"
      profiles:
        - "domain"
        - "private"
        - "public"
    - name: "Allow inbound ICMPv6 (echo request)"
      direction: "in"
      protocol: "icmpv6"
      icmp_type:
        - "8:*"
      action: "allow"
      profiles:
        - "domain"
        - "private"
        - "public"
```
