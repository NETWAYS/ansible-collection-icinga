## Notification

To activate the feature notification add this block to the variable `icinga2_features`.

```yaml
icinga2_features:
  - name: notification
```

### Notification Scripts

The role won't manage notifications scripts with the role. Many scripts require dependencies or libraries to be installed. To manage those dependencies create a Ansible role and use it after the Icinga 2 role.

If there are no dependencies on the script you can easily use the `post_tasks` section in your playbook. Example:

```yaml
post_tasks:
  - name: copy notifications script
    src: rocket_chat_notification.py
    dest: /etc/icinga2/scripts/rocket_chat_notification.py
    group: "{{ icinga2_group }}
    user: "{{ icinga2_user}}"
```

### Feature Attributes

* `enable_ha: boolean`
  * Enable the high availability functionality. Only valid in a cluster setup. Disabling this currently only affects reminder notifications.

* `state: string`
  * Decides whether the feature is enabled or disabled. Possible values present, absent.
