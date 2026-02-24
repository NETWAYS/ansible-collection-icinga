from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_gelfwriter
short_description: Creates information for GelfWriter object.
description:
  - Returns information used to create a GelfWriter object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the GelfWriter object.
    required: true
    type: str
  state:
    description:
      - The state of the GelfWriter object.
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
    default: "features-available/gelf.conf"
    type: str
  host:
    description:
      - GELF receiver host address.
    required: false
    type: str
  port:
    description:
      - GELF receiver port.
    required: false
    type: int
  source:
    description:
      - Source name for this instance.
    required: false
    type: str
  enable_send_perfdata:
    description:
      - Enable performance data for 'CHECK RESULT' events.
    required: false
    type: bool
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
    required: false
    type: bool
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
'''

EXAMPLES = '''
icinga.icinga.icinga2_gelfwriter:
  name: "mygelfwriter"
  host: "gelf.localdomain"
  port: 12201
  source: "icinga"
  ca_path: "/etc/pki/tls/certs/gelf-ca.crt"
  cert_path: "/etc/pki/tls/certs/local-icinga-host.crt"
  key_path: "/etc/pki/tls/private/local-icinga-host.key"
  enable_ha: false
  enable_send_perfdata: true
  enable_tls: true
  insecure_noverify: false
'''

RETURN = '''
args:
  description: Arguments used to create the GelfWriter object.
  returned: success
  type: dict
  contains:
    ca_path:
      description: The specified path to the ca.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/gelf-ca.crt
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
    host:
      description: The specified host.
      returned: success
      type: str
      sample: gelf.localdomain
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
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 12201
    source:
      description: The specified source.
      returned: success
      type: str
      sample: icinga
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/gelf.conf
name:
  description: The name of the GelfWriter object.
  returned: success
  type: str
  sample: mygelfwriter
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
            file                 = dict(default='features-available/gelf.conf', type='str'),
            host                 = dict(type='str'),
            port                 = dict(type='int'),
            source               = dict(type='str'),
            enable_send_perfdata = dict(type='bool'),
            enable_ha            = dict(type='bool'),
            enable_tls           = dict(type='bool'),
            insecure_noverify    = dict(type='bool'),
            ca_path              = dict(type='str'),
            cert_path            = dict(type='str'),
            key_path             = dict(type='str'),
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
