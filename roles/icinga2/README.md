# Role netways.icinga.icinga2

The collection provides several roles to install and configure Icinga 2.

* [Configure Features](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/features.md)
* [Configure Monitoring Objects](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/objects.md)

## Variables

* `icinga2_purge_features: boolean`
  * Decides whether the unmanaged features should be purged or not. Default: true

* `icinga2_constants: dict`
  * Define constants in **constants.conf**, for defaults check the vars folder.

```yaml
icinga2_constants:
  NodeName: satellite.localdomain
  ZoneName: zone-satellite-d1
```

### Manage Configuration

If the local **conf.d** directory shouldn't be recursively included then the
var `icinga2_confd` should be set to `false`.

Otherwise you can use a directory name to set the include to a different folder
than **conf.d**. The folder needs to exist below /etc/icinga2. If it should be created by the role use the variable `icinga2_config_directories` in addition.

```yaml
icinga2_confd: true/false/<directory_name>
```

### SELinux handling

The Icinga 2 role will automatically detect via Ansible facts if SELinux is enabled on the system. If this is the case the package icinga2-selinux will be automatically installed.

If the package should be installed, even if SELinux is not enabled or somehow wrongly disabled in Ansible, set the following fact.

```yaml
selinux:
  status: enabled
```

### Delegate Icinga ticket

The role primarily delegates the ticket creation to the [Icinga ca host](https://github.com/NETWAYS/ansible-collection-icinga/tree/main/doc/role-icinga2/features/feature-api.md). If the host is not listed with the same name in Ansible, you can set the name of the host in Ansible with **icinga2_delegate_host**.

```yaml
icinga2_delegate_host: icinga-master
```

### Tags

The role exposes two coarse-grained tags so playbooks can re-run individual phases without rolling out the full role:

| Tag                 | Effect                                              |
|---------------------|-----------------------------------------------------|
| `icinga2_install`   | Runs only the package installation                  |
| `icinga2_configure` | Renders and deploys the full configuration          |

```bash
ansible-playbook site.yml --tags icinga2_configure
```

Fact gathering and loading of the OS specific variables are marked `tags: always`, so they run on every tagged invocation and provide the required context (paths, user, group, ...).

Running the role without `--tags` behaves exactly as before: all phases execute in order.

Handlers are triggered via `notify` as soon as a tagged task reports `changed`, so a service reload still fires on, for example, `--tags icinga2_configure`.
