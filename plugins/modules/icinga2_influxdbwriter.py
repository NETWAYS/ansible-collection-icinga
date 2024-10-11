from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_influxdbwriter
short_description: Creates information for InfluxdbWriter object.
description:
  - Returns information used to create a InfluxdbWriter object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the InfluxdbWriter object.
    required: true
    type: str
  state:
    description:
      - The state of the InfluxdbWriter object.
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
    required: false
    default: "features-available/influxdb.conf"
    type: str
  host:
    description:
      - InfluxDB host address.
    required: false
    type: str
  port:
    description:
      - InfluxDB HTTP port.
    required: false
    type: int
  database:
    description:
      - InfluxDB database name.
    required: false
    type: str
  username:
    description:
      - InfluxDB user name.
    required: false
    type: str
  password:
    description:
      - InfluxDB user password.
    required: false
    type: str
  ssl_enable:
    description:
      - Whether to use TLS.
    required: false
    type: bool
  ssl_ca_cert:
    description:
      - Path to CA certificate to validate the remote host.
    required: false
    type: str
  ssl_cert:
    description:
      - Path to host certificate to present to the remote host for mutual verification.
    required: false
    type: str
  ssl_key:
    description:
      - Path to host key to accompany the ssl_cert.
    required: false
    type: str
  ssl_insecure_noverify:
    description:
      - Disable TLS peer verification.
    required: false
    type: bool
  basic_auth:
    description:
      - Username and password for HTTP basic authentication.
    required: false
    type: dict
  host_template:
    description:
      - Host template to define the InfluxDB line protocol.
    required: false
    type: dict
  service_template:
    description:
      - Service template to define the InfluxDB line protocol.
    required: false
    type: dict
  enable_send_thresholds:
    description:
      - Whether to send warn, crit, min & max tagged data.
    required: false
    type: bool
  enable_send_metadata:
    description:
      - Whether to send check metadata e.g. states, execution time, latency etc.
    required: false
    type: bool
  flush_interval:
    description:
      - How long to buffer data points before transferring to InfluxDB.
    required: false
    type: str
  flush_threshold:
    description:
      - How many data points to buffer before forcing a transfer to InfluxDB.
    required: false
    type: int
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
    required: false
    type: bool
'''

EXAMPLES = '''
icinga.icinga.icinga2_influxdbwriter:
  name: "myinfluxdbwriter"
  host: "influx.localdomain"
  port: 8086
  database: "icinga"
  username: "icinga-user"
  password: "icinga-user-password"
  basic_auth:
    username: "icinga"
    password: "password"
  host_template:
    measurement: "$host.check_command$"
    tags:
      hostname: "$host.name$"
  service_template:
    measurement: "$service.check_command$"
    tags:
      hostname: "$host.name$"
      service: "$service.name$"
  ssl_enable: true
  ssl_insecure_noverify: false
  ssl_ca_cert: "/etc/pki/tls/certs/influx-ca.crt"
  ssl_cert: "/etc/pki/tls/certs/local-icinga-host.crt"
  ssl_key: "/etc/pki/tls/private/local-icinga-host.key"
  enable_ha: false
  enable_send_metadata: true
  enable_send_thresholds: true
  flush_interval: "30s"
  flush_threshold: 2048
'''

RETURN = '''
args:
  description: Arguments used to create the InfluxdbWriter object.
  returned: success
  type: dict
  contains:
    basic_auth:
      description: The specified information for basic authentication.
      returned: success
      type: dict
      sample: { "password": "password", "username": "icinga" }
    database:
      description: The specified database.
      returned: success
      type: str
      sample: icinga
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: false
    enable_send_metadata:
      description: Whether metadata is sent.
      returned: success
      type: bool
      sample: false
    enable_send_thresholds:
      description: Whether threshold data is sent.
      returned: success
      type: bool
      sample: false
    flush_interval:
      description: The specified flush interval.
      returned: success
      type: str
      sample: 30s
    flush_threshold:
      description: The specified flush threshold.
      returned: success
      type: int
      sample: 2048
    host:
      description: The specified host.
      returned: success
      type: str
      sample: influx.localdomain
    host_template:
      description: The specified host template.
      returned: success
      type: dict
      sample: { "measurement": "$host.check_command$", "tags": { "hostname": "$host.name$" } }
    password:
      description: The specified password.
      returned: success
      type: str
      sample: icinga-user-password
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 8086
    service_template:
      description: The specified service template.
      returned: success
      type: dict
      sample: { "measurement": "$service.check_command$", "tags": { "hostname": "$host.name$", "service": "$service.name$" } }
    ssl_ca_cert:
      description: The specified path to the ca.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/influx-ca.crt
    ssl_cert:
      description: The specified path to the certificate.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/local-icinga-host.crt
    ssl_enable:
      description: Whether TLS is used.
      returned: success
      type: bool
      sample: true
    ssl_insecure_noverify:
      description: Whether TLS peer verification is disabled.
      returned: success
      type: bool
      sample: false
    ssl_key:
      description: The specified path to the key.
      returned: success
      type: str
      sample: /etc/pki/tls/private/local-icinga-host.key
    username:
      description: The specified user.
      returned: success
      type: str
      sample: icinga-user
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/influxdb.conf
name:
  description: The name of the InfluxdbWriter object.
  returned: success
  type: str
  sample: myinfluxdbwriter
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
            file=dict(default='features-available/influxdb.conf', type='str'),
            host=dict(type='str'),
            port=dict(type='int'),
            database=dict(type='str'),
            username=dict(type='str'),
            password=dict(type='str'),
            ssl_enable=dict(type='bool'),
            ssl_ca_cert=dict(type='str'),
            ssl_cert=dict(type='str'),
            ssl_key=dict(type='str'),
            ssl_insecure_noverify=dict(type='bool'),
            basic_auth=dict(type='dict'),
            host_template=dict(type='dict'),
            service_template=dict(type='dict'),
            enable_send_thresholds=dict(type='bool'),
            enable_send_metadata=dict(type='bool'),
            flush_interval=dict(type='str'),
            flush_threshold=dict(type='int'),
            enable_ha=dict(type='bool'),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')

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
