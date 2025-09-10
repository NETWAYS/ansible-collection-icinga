from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_idopgsqlconnection
short_description: Creates information for IdoPgsqlConnection object.
description:
  - Returns information used to create an IdoPgsqlConnection object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the IdoPgsqlConnection object.
    required: true
    type: str
  state:
    description:
      - The state of the IdoPgsqlConnection object.
    required: false
    default: present
    choices: [ "present", "absent" ]
    type: str
  order:
    description:
      - Value to determine internal precedence.
    required: false
    default: 10
    type: int
  file:
    description:
      - Path to the file in which the object will be defined.
    required: true
    type: str
  host:
    description:
      - PostgreSQL database host address.
    required: false
    type: str
  port:
    description:
      - PostgreSQL database port.
    required: false
    type: int
  user:
    description:
      - PostgreSQL database user with read/write permission to the icinga database.
    required: false
    type: str
  password:
    description:
      - PostgreSQL database user’s password.
    required: false
    type: str
  database:
    description:
      - PostgreSQL database name.
    required: false
    type: str
  ssl_mode:
    description:
      - Enable SSL connection mode.
    required: false
    type: str
    choices:
      - prefer
      - require
      - verify-ca
      - verify-full
      - allow
      - disable
  ssl_key:
    description:
      - PostgreSQL SSL client key file path.
    required: false
    type: str
  ssl_cert:
    description:
      - PostgreSQL SSL certificate file path.
    required: false
    type: str
  ssl_ca:
    description:
      - PostgreSQL SSL certificate authority certificate file path.
    required: false
    type: str
  table_prefix:
    description:
      - PostgreSQL database table prefix.
    required: false
    type: str
  extra_options:
    description:
      - Extra options to be passed to the psql command when applying the database schema.
    required: false
    type: str
  instance_name:
    description:
      - Unique identifier for the local Icinga 2 instance, used for multiple Icinga 2 clusters writing to the same database.
    required: false
    type: str
  instance_description:
    description:
      - Description for the Icinga 2 instance.
    required: false
    type: str
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
    required: false
    type: bool
  failover_timeout:
    description:
      - Set the failover timeout in a HA cluster. Must not be lower than 30s.
    required: false
    type: str
  cleanup:
    description:
      - Dictionary with items for historical table cleanup.
    required: false
    type: dict
  categories:
    description:
      - Array of information types that should be written to the database.
    required: false
    type: list
    elements: str
  import_schema:
    description:
      - Whether to apply the database schema.
    required: false
    type: bool
'''

EXAMPLES = '''
icinga.icinga.icinga2_idopgsqlconnection:
  name: "myidopgsqlconnection"
  password: "super-secret-password"
'''

RETURN = '''
args:
  description: Arguments used to create the IdoPgsqlConnection object.
  returned: success
  type: dict
  contains:
    categories:
      description: The specified categories.
      returned: success
      type: list
      elements: str
      sample: [ "DbCatCheck", "DbCatComment" ]
    cleanup:
      description: The specified cleanup.
      returned: success
      type: dict
      sample: { "acknowledgements_age": "0" }
    database:
      description: The specified database name.
      returned: success
      type: str
      sample: "icinga-ido"
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: true
    extra_options:
      description: The extra options passed to the psql command.
      returned: success
      type: str
      sample: "--no-beep"
    failover_timeout:
      description: The specified failover timeout.
      returned: success
      type: str
      sample: "30s"
    host:
      description: The specified database host.
      returned: success
      type: str
      sample: "localhost"
    instance_description:
      description: The specified instance description.
      returned: success
      type: str
      sample: "Primary Icinga instance for all monitoring needs"
    instance_name:
      description: The specified instance name.
      returned: success
      type: str
      sample: "icinga2"
    password:
      description: The specified password
      returned: success
      type: str
      sample: "super-secret-password"
    port:
      description: The specified database port.
      returned: success
      type: int
      sample: 3306
    ssl_ca:
      description: The specified SSL certificate authority certificate file path.
      returned: success
      type: str
      sample: "/etc/local_ssl/ca.cert"
    ssl_cert:
      description: The specified PostgreSQL SSL certificate file path.
      returned: success
      type: str
      sample: "/etc/local_ssl/postgresql.cert"
    ssl_key:
      description: The specified PostgreSQL SSL client key file path.
      returned: success
      type: str
      sample: "/etc/local_ssl/client.key"
    ssl_mode:
      description: The specified SSL connection mode.
      returned: success
      type: str
      sample: "verify-full"
    table_prefix:
      description: The specified table prefix to use.
      returned: success
      type: str
      sample: "icinga"
    user:
      description: The specified PostgreSQL database user.
      returned: success
      type: str
      sample: "icinga"
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/idopgsqlconnection.conf
name:
  description: The name of the IdoPgsqlConnection object.
  returned: success
  type: str
  sample: myidopgsqlconnection
order:
  description: The order value of this object. Used internally when combining multiple templates / objects.
  returned: success
  type: int
  sample: 10
state:
  description: The chosen state for the object.
  returned: success
  type: str
  sample: present
'''

def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent']),
            name=dict(required=True),
            order=dict(default=10, type='int'),
            file=dict(default='features-available/ido-postgresql.conf', type='str'),
            host=dict(default='localhost', type='str'),
            port=dict(default='5432', type='int'),
            user=dict(default='icinga2', type='str'),
            password=dict(required=True, type='str'),
            database=dict(default='icinga2', type='str'),
            ssl_mode=dict(choices=['prefer', 'require', 'verify-ca', 'verify-full', 'allow', 'disable']),
            ssl_key=dict(type='str'),
            ssl_cert=dict(type='str'),
            ssl_ca=dict(type='str'),
            table_prefix=dict(type='str'),
            extra_options=dict(type='str'),
            instance_name=dict(type='str'),
            instance_description=dict(type='str'),
            enable_ha=dict(type='bool'),
            failover_timeout=dict(type='str'),
            cleanup=dict(type='dict'),
            categories=dict(type='list', elements='str'),
            import_schema=dict(type='bool'),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')
    if 'import_schema' in args:
        args.pop('import_schema')

    module.exit_json(
        changed=False,
        args=args,
        name=name,
        order=str(order),
        state=state,
        file=file
    )


if __name__ == '__main__':
    main()
