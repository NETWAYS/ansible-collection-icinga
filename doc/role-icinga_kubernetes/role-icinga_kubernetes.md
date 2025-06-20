# Role netways.icinga.icinga_kubernetes

This role installs and configures the Icinga Kubernetes Daemon. In addition it can also import the schema into the database.
More information about this package can be found [in the official documentation](https://icinga.com/docs/icinga-for-kubernetes/latest/doc/01-About/).

## Database

Icinga Kubernetes relies on a relational database to persist received data. This database **won't** be created by this role - you need to deploy and configure one in advance. For more information, see the [Databases](../getting-started.md#databases) section in the getting started guide.

## Variables

The following variables define the configuration for Icinga Kubernetes. Some variables got predefined [defaults](../../roles/kubernetes/defaults/main.yml), others are purely opt-in.

For more information on the respective settings please see [the official documentation](https://icinga.com/docs/icinga-for-kubernetes/latest/doc/03-Configuration/).

### Database Configuration

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `icinga_kubernetes_database_host` | `String` | Defines database address to connect to. | `127.0.0.1` |
| `icinga_kubernetes_database_import_schema` | `bool` | Defines whether to import the schema into the database or not. **Needs `icinga_kubernetes_database_type` to be set**. | `false` |
| `icinga_kubernetes_database_name` | `String` | Defines the database to connect to. | `kubernetes` |
| `icinga_kubernetes_database_password` | `String` | Defines the database password to connect with. | `kubernetes` |
| `icinga_kubernetes_database_port` | `int` | Defines the database port to connect to. | **n/a** |
| `icinga_kubernetes_database_type` | `mysql` | Defines database type set in `config.yml`. |  `mysql` |
| `icinga_kubernetes_database_user` | `String` | Defines database user set in `config.yml`. | `kubernetes` |

### Icinga Kubernetes Configuration

The following variables are used for the Icinga Kubernetes setup. Normally, you can rely on the defaults to work and should **not** change them unless you know what you are doing.

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `icinga_kubernetes_config_dir` | `String` | Defines the directory where the Icinga Kubernetes configuration is stored. | `/etc/icinga-kubernetes` |
| `icinga_kubernetes_database_schema` | `String` | Defines the path to the schema file. | `"/usr/share/icinga-kubernetes/schema/{{ icinga_kubernetes_database_type }}/schema.sql"` |
| `icinga_kubernetes_group` | `String` | Defines the group membership for the Icinga Kubernetes user. | `icinga-kubernetes` |
| `icinga_kubernetes_packages` | `List` | Defines the packages to install for Icinga Kubernetes. | `[icinga-kubernetes]` |
| `icinga_kubernetes_service_name` | `String` | Defines the name of the Icinga Kubernetes service. | `icinga-kubernetes` |
| `icinga_kubernetes_user` | `String` | Defines the user for the Icinga Kubernetes service. | `icinga-kubernetes` |
| `icinga_kubernetes_cluster_config` | `List of dicts` | List of cluster configurations, list of dicts, must contain 'cluster_name' and optional 'kubeconfig' path, see example, leave unconfigured for default package config | `[ cluster_name: default ]` |
| `icinga_kubernetes_prometheus_url` | `String` | Defines optional url of a Prometheus instance to connect for metrics |  |
| `icinga_kubernetes_prometheus_insecure` | `String` | Defines an insecure connection to the Prometheus instance | `false` |
| `icinga_kubernetes_prometheus_username` | `String` | Defines optional username to access the Prometheus instance |  |
| `icinga_kubernetes_prometheus_password` | `String` | Defines optional password to access the Prometheus instance|  |

## Examples

This play installs Icinga Kubernetes with on the same host as its connected MySQL database. It also imports the schema into the database.

```yaml
- name: Install Icinga Kubernetes
  hosts: icingakubernetes
  become: true
  vars:
    icinga_kubernetes_database_import_schema: true  # Import the schema into the database
    icinga_kubernetes_database_type: mysql  # needed by the schema import

  roles:
    - role: icinga.icinga.icinga_kubernetes
```

This example installs Icinga Kubernetes and connects it to a **remote** MySQL database. It also imports the schema into the database and set a custom kubeconfig path.

```yaml
- name: Install Icinga Kubernetes
  hosts: icingadb
  become: true
  vars:
    icinga_kubernetes_database_type: mysql
    icinga_kubernetes_database_host: mysql.example.com
    icinga_kubernetes_database_port: 3306
    icinga_kubernetes_database_user: kube_user
    icinga_kubernetes_database_password: hellokube$123
    icinga_kubernetes_database_import_schema: true
    icinga_kubernetes_cluster_config:
      - cluster_name: default
        kubeconfig: ~/.kube/config

  roles:
    - role: icinga.icinga.icinga_kubernetes
```
