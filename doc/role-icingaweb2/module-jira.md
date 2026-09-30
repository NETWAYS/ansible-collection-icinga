# Module Jira

This module installs and configures the Icinga Jira module for Icinga Web 2.
It creates Jira issues for Icinga problems and links them back to Icinga Web.

## Requirements

The `icinga-jira` package is provided by the official Icinga repository, which the `netways.icinga.repos` role enables by default.

The module needs two custom fields in Jira that represent `icingaKey` and `icingaStatus`.

## Configuration

The module uses two configuration files:

* `config` writes `config.ini` with the connection to Jira and the module settings.
* `templates` writes `templates.ini`. Each key is a template name, each subkey a Jira field.
  For the available fields and placeholders see the [module documentation](https://icinga.com/docs/icinga-web-jira-integration/latest/doc/03-Configuration/#fill-jira-custom-fields).

```yaml
icingaweb2_modules:
  jira:
    enabled: true
    source: package
    config:
      api:
        host: jira.example.com
        username: icinga
        password: secret
      deployment:
        type: cloud
      ui:
        default_project: ITSM
        default_issuetype: Incident
      icingaweb:
        url: https://icinga.example.com/icingaweb2
    templates:
      my-workflow:
        duedate: 3 days
        SearchTerm: "${host}.example.com"
        Teams.0.value: "My Team"
        Teams.1.value: "Another Team"
```

The notification commands for the Director are not created by the role.
Use "Sync to Director" in the module's Director Config tab to create them.
