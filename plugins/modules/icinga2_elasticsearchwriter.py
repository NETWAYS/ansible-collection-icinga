from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_elasticsearchwriter
short_description: Creates information for ElasticsearchWriter object.
description:
  - Returns information used to create an ElasticsearchWriter object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the ElasticsearchWriter object.
    required: true
    type: str
  state:
    description:
      - The state of the ElasticsearchWriter object.
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
    default: features-available/elasticsearch.conf
    type: str
  host:
    description:
      - Elasticsearch host address.
    required: false
    type: str
  port:
    description:
      - Elasticsearch port.
    required: false
    type: int
  index:
    description:
      - Elasticsearch index name.
    required: false
    type: str
  enable_send_perfdata:
    description:
      - Send parsed performance data metrics for check results.
    required: false
    type: bool
  flush_interval:
    description:
      - How long to buffer data points before transferring to Elasticsearch.
    required: false
    type: str
  flush_threshold:
    description:
      - How many data points to buffer before forcing a transfer to Elasticsearch.
    required: false
    type: int
  username:
    description:
      - Basic auth username if Elasticsearch is hidden behind an HTTP proxy.
    required: false
    type: str
  password:
    description:
      - Basic auth password if Elasticsearch is hidden behind an HTTP proxy.
    required: false
    type: str
  enable_tls:
    description:
      - Whether to use a TLS stream.
    required: false
    type: bool
  insecure_noverify:
    description:
      - Disable TLS peer verification.
    required: false
    type: bool
  ca_path:
    description:
      - Path to CA certificate to validate the remote host. Requires enable_tls set to true.
    required: false
    type: str
  cert_path:
    description:
      - Path to host certificate to present to the remote host for mutual verification. Requires enable_tls set to true.
    required: false
    type: str
  key_path:
    description:
      - Path to host key to accompany the cert_path. Requires enable_tls set to true.
    required: false
    type: str
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
    required: false
    type: bool
'''

EXAMPLES = '''
icinga.icinga.icinga2_elasticsearchwriter:
  name: "es-writer"
  ca_path: "/etc/pki/tls/certs/es-ca.crt"
  cert_path: "/etc/pki/tls/certs/local-icinga-host.crt"
  key_path: "/etc/pki/tls/private/local-icinga-host.crt"
  enable_ha: false
  enable_send_perfdata: true
  enable_tls: true
  insecure_noverify: false
  flush_interval: "30s"
  flush_threshold: 2048
  host: "es.localdomain"
  port: 9200
  index: "icinga"
  username: "es-icinga-user"
  password: "es-icinga-user-password"
'''

RETURN = '''
args:
  description: Arguments used to create the ElasticsearchWriter object.
  returned: success
  type: dict
  contains:
    ca_path:
      description: The specified path to the ca.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/es-ca.crt
    cert_path:
      description: The specified path to the certificate.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/local-icinga-host.crt
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: false
    enable_send_perfdata:
      description: Whether performance data is sent.
      returned: success
      type: bool
      sample: true
    enable_tls:
      description: Whether TLS is used.
      returned: success
      type: bool
      sample: true
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
      sample: es.localdomain
    index:
      description: The specified index.
      returned: success
      type: str
      sample: icinga
    insecure_noverify:
      description: Whether TLS peer verification is used.
      returned: success
      type: bool
      sample: false
    key_path:
      description: The specified path to the key.
      returned: success
      type: str
      sample: /etc/pki/tls/private/local-icinga-host.key
    password:
      description: The specified password.
      returned: success
      type: str
      sample: es-icinga-user-password
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 9200
    username:
      description: The specified username.
      returned: success
      type: str
      sample: es-icinga-user
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/elasticsearch.conf
name:
  description: The name of the ElasticsearchWriter object.
  returned: success
  type: str
  sample: es-writer
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
            state                = dict(default='present', choices=['present', 'absent']),
            name                 = dict(required=True),
            order                = dict(default=10, type='int'),
            file                 = dict(default='features-available/elasticsearch.conf', type='str'),
            host                 = dict(type='str'),
            port                 = dict(type='int'),
            index                = dict(type='str'),
            enable_send_perfdata = dict(type='bool'),
            flush_interval       = dict(type='str'),
            flush_threshold      = dict(type='int'),
            username             = dict(type='str'),
            password             = dict(type='str'),
            enable_tls           = dict(type='bool'),
            insecure_noverify    = dict(type='bool'),
            ca_path              = dict(type='str'),
            cert_path            = dict(type='str'),
            key_path             = dict(type='str'),
            enable_ha            = dict(type='bool'),
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
