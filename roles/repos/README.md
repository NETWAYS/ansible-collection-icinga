# Ansible Role netways.icinga.repos

This role configures Icinga 2 related repositories to provide all necessary packages.


## Variables

To enable the EPEL repository.

```yaml
icinga_repo_epel: true
icinga_repo_scl: true
```

To manage which Icinga Repos to use the following variables:

```yaml
icinga_repo_stable: true
icinga_repo_testing: false
icinga_repo_snapshot: false
```

To use the Icinga Repository Subscription:

```yaml
icinga_repo_subscription_username: "Your username"
icinga_repo_subscription_password: "Your password"
```

# NETWAYS Repositories

In addition to the Icinga 2 related repositories NETWAYS repositories are also managed by this role.

> Packages exist mainly for Debian/Ubuntu and EL.

## Variables

To activate either the [Extras repository](https://packages.netways.de/extras/) or the [Plugins repository](https://packages.netways.de/plugins/) set the respective variable to `true`.

```
netways_repo_extras: false
netways_repo_plugins: false
```
