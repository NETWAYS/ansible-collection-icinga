## Collection Testing Guide

This guide will quickstart you on our testing environment and eases the way to
contribute on our project.

### Tests

Currently we do some molecule tests to check if the roles work in combination
and some variables to check if anything fails.

Then there are unit tests for the parser which generates the Icinga 2 DSL.

At last we implemented a way to check if our Icingaweb roles generates valid
ini files.

### Tools

Make sure the following tools are available before start testing with the collection.

```bash
pip install ansible-core ansible-lint molecule pytest-testinfra
```

To test roles locally without docker/service issues, we created a molecule test
with vagrant. Then you need to install [vagrant](link/to/vagrant) and the molecule plugin.

```bash
pip install molecule-plugins[vagrant]
```

To use molecule with docker install the docker plugin.

```bash
pip install molecule-plugins[docker]
```


### Roles Testing

To test roles over vagrant locally, it is the easiest to run the **local-default**
scenario. The local-default is very big and long running. For shorter tests use
the role-<rolename> scenarios.

```bash
molecule test -s local-default
```

The following tests are inplemented based on docker. Per default a **ubuntu2204**
image from geerlingguy's container is used. Thanks [@geerlingguy Dockerhublink](https://hub.docker.com/u/geerlingguy)

To test other distros use the command with the env **MOLECULE_DISTRO**.

```bash
MOLECULE_DISTRO=opensuseleap15 molecule test -s role-icingadb_redis
```

### Templating Tests

The roles are generating configuration for Icingaweb2 and Icinga2 in various files.
To ensure values are written to these files in right syntax we test those too.

#### Python Unittest

For testing our Icinga 2 objects syntax we implemented python unittests and try
many combinations which occur in different python versions.

For more information please have a look at the workflow `Python Unittest`.

#### Icingaweb2 INI

To test the INI configuration over Ansible in the Icinga Web 2 role, we implemented
a molecule test to include the template from the role and test it with various values.
