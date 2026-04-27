from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_otlpmetricswriter
short_description: Creates information for OTLPMetricsWriter object.
description:
  - Returns information used to create a OTLPMetricsWriter object.
  - Requires Icinga 2 2.15 or later.
version_added: 0.1.0
author:
  - NETWAYS GmbH <info@netways.de>

options:
  name:
    description:
      - The name of the OTLPMetricsWriter object.
    required: true
    type: str
  state:
    description:
      - The state of the OTLPMetricsWriter object.
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
    default: "features-available/otlpmetrics.conf"
    type: str
  host:
    description:
      - OTLP backend host address.
    required: false
    default: "127.0.0.1"
    type: str
  port:
    description:
      - OTLP backend HTTP port.
    required: false
    default: 4318
    type: int
  metrics_endpoint:
    description:
      - OTLP metrics endpoint path.
    required: false
    default: "/v1/metrics"
    type: str
  service_namespace:
    description:
      - Namespace used in the service.namespace OTel resource attribute.
    required: false
    default: "icinga"
    type: str
  basic_auth:
    description:
      - Optional HTTP basic auth credentials with the keys username and password.
    required: false
    type: dict
  ssl_enable:
    description:
      - Whether to use a TLS stream.
    required: false
    type: bool
  ssl_insecure_noverify:
    description:
      - Disable TLS peer verification.
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
  enable_send_thresholds:
    description:
      - Whether to send threshold values (warn, crit, min, max) as state_check.threshold metric points.
    required: false
    type: bool
  host_resource_attributes:
    description:
      - Custom resource attributes attached to host check metrics. Values may contain Icinga 2 macros.
    required: false
    type: dict
  service_resource_attributes:
    description:
      - Custom resource attributes attached to service check metrics. Values may contain Icinga 2 macros.
    required: false
    type: dict
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
    required: false
    type: bool
'''

EXAMPLES = '''
- netways.icinga.icinga2_otlpmetricswriter:
    name: "myotlpmetrics"
    host: "127.0.0.1"
    port: 4318
    metrics_endpoint: "/v1/metrics"
    service_namespace: "icinga2-production"
    basic_auth:
      username: "icinga"
      password: "secret"
    ssl_enable: false
    enable_send_thresholds: true
    host_resource_attributes:
      environment: "prod"
    service_resource_attributes:
      environment: "prod"
      team: "$host.vars.team$"
    enable_ha: true
'''

RETURN = '''
args:
  description: Arguments used to create the OTLPMetricsWriter object.
  returned: success
  type: dict
  contains:
    host:
      description: The specified host.
      returned: success
      type: str
      sample: 127.0.0.1
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 4318
    metrics_endpoint:
      description: The specified metrics endpoint path.
      returned: success
      type: str
      sample: /v1/metrics
    service_namespace:
      description: The specified service namespace.
      returned: success
      type: str
      sample: icinga
    basic_auth:
      description: The specified basic auth credentials.
      returned: success
      type: dict
      sample: { "username": "icinga", "password": "secret" }
    ssl_enable:
      description: Whether TLS is used.
      returned: success
      type: bool
      sample: false
    ssl_insecure_noverify:
      description: Whether TLS peer verification is disabled.
      returned: success
      type: bool
      sample: false
    ssl_ca_cert:
      description: The specified path to the ca.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/otlp-ca.crt
    ssl_cert:
      description: The specified path to the certificate.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/local-icinga-host.crt
    ssl_key:
      description: The specified path to the key.
      returned: success
      type: str
      sample: /etc/pki/tls/private/local-icinga-host.key
    enable_send_thresholds:
      description: Whether threshold data is sent.
      returned: success
      type: bool
      sample: false
    host_resource_attributes:
      description: The specified host resource attributes.
      returned: success
      type: dict
      sample: { "environment": "prod" }
    service_resource_attributes:
      description: The specified service resource attributes.
      returned: success
      type: dict
      sample: { "environment": "prod" }
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: true
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/otlpmetrics.conf
name:
  description: The name of the OTLPMetricsWriter object.
  returned: success
  type: str
  sample: myotlpmetrics
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
        argument_spec = dict(
            state                       = dict(default='present', choices=['present', 'absent']),
            name                        = dict(required=True),
            order                       = dict(default=10, type='int'),
            file                        = dict(default='features-available/otlpmetrics.conf', type='str'),
            host                        = dict(default='127.0.0.1', type='str'),
            port                        = dict(default=4318, type='int'),
            metrics_endpoint            = dict(default='/v1/metrics', type='str'),
            service_namespace           = dict(default='icinga', type='str'),
            basic_auth                  = dict(type='dict'),
            ssl_enable                  = dict(type='bool'),
            ssl_insecure_noverify       = dict(type='bool'),
            ssl_ca_cert                 = dict(type='str'),
            ssl_cert                    = dict(type='str'),
            ssl_key                     = dict(type='str'),
            enable_send_thresholds      = dict(type='bool'),
            host_resource_attributes    = dict(type='dict'),
            service_resource_attributes = dict(type='dict'),
            enable_ha                   = dict(type='bool'),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')

    module.exit_json(changed=False, args=args, name=name, order=str(order), state=state, file=file)

if __name__ == '__main__':
    main()
