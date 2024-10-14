from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_icingadb
short_description: Creates information for IcingaDB object.
description:
  - Returns information used to create a IcingaDB object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the IcingaDB object.
    required: true
    type: str
  state:
    description:
      - The state of the IcingaDB object.
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
    default: "features-available/icingadb.conf"
    type: str
  host:
    description:
      - Redis host.
    required: false
    type: str
  port:
    description:
      - Redis port.
    required: false
    type: int
  path:
    description:
      - Redis unix socket path.
    required: false
    type: str
  password:
    description:
      - Redis auth password.
    required: false
    type: str
  enable_tls:
    description:
      - Whether to use TLS.
    required: false
    type: bool
  cert_path:
    description:
      - Path to the certificate.
    required: false
    type: str
  key_path:
    description:
      - Path to the private key.
    required: false
    type: str
  ca_path:
    description:
      - Path to the CA certificate to use instead of the system's root CAs.
    required: false
    type: str
  crl_path:
    description:
      - Path to the CRL file.
    required: false
    type: str
  cipher_list:
    description:
      - Cipher list that is allowed. For a list of available ciphers run openssl ciphers.
    required: false
    type: str
  tls_protocolmin:
    description:
      - Minimum TLS protocol version.
    required: false
    type: str
  insecure_noverify:
    description:
      - Whether not to verify the peer.
    required: false
    type: bool
  connect_timeout:
    description:
      - Timeout for establishing new connections. Within this time, the TCP, TLS (if enabled) and Redis handshakes must complete.
    required: false
    type: int
'''

EXAMPLES = '''
icinga.icinga.icinga2_icingadb:
  name: "myicingadb"
  ca_path: "/etc/pki/tls/certs/redis-ca.crt"
  cert_path: "/etc/pki/tls/certs/local-icinga-host.crt"
  connect_timeout: 30
  enable_tls: true
  host: "redis-host.localdomain"
  insecure_noverify: false
  key_path: "/etc/pki/tls/private/local-icinga-host.key"
  password: "redis-password"
  port: 6380
'''

RETURN = '''
args:
  description: Arguments used to create the IcingaDB object.
  returned: success
  type: dict
  contains:
    ca_path:
      description: The specified path to the CA.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/redis-ca.crt
    cert_path:
      description: The specified path to the certificate.
      returned: success
      type: str
      sample: /etc/pki/tls/certs/local-icinga-host.crt
    cipher_list:
      description: The specified cipher list.
      returned: success
      type: str
      sample: null
    connect_timeout:
      description: The specified connection timeout.
      returned: success
      type: int
      sample: 30
    crl_path:
      description: The specified path to the CRL.
      returned: success
      type: str
      sample: null
    enable_tls:
      description: Whether TLS is enabled
      returned: success
      type: bool
      sample: true
    host:
      description: The specified host.
      returned: success
      type: str
      sample: localhost
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
      sample: redis-password
    path:
      description: The specified path to the UNIX socket file.
      returned: success
      type: str
      sample: null
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 6380
    tls_protocolmin:
      description: Minimum TLS protocol version.
      returned: success
      type: str
      sample: null

file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/icingadb.conf
name:
  description: The name of the IcingaDB object.
  returned: success
  type: str
  sample: myicingadb
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
            file                 = dict(default='features-available/icingadb.conf', type='str'),
            host                 = dict(type='str'),
            port                 = dict(type='int'),
            path                 = dict(type='str'),
            password             = dict(type='str'),
            enable_tls           = dict(type='bool'),
            cert_path            = dict(type='str'),
            key_path             = dict(type='str'),
            ca_path              = dict(type='str'),
            crl_path             = dict(type='str'),
            cipher_list          = dict(type='str'),
            tls_protocolmin      = dict(type='str'),
            insecure_noverify    = dict(type='bool'),
            connect_timeout      = dict(type='int'),
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
