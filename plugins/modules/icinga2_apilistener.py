from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
---
name: icinga2_apilistener
short_description: Creates information for ApiListener object.
description:
  - Returns information used to create an ApiListener object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>
options:
  name:
    description:
      - The name of the ApiListener object.
    required: true
    type: str
  state:
    description:
      - The state of the ApiListener object.
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
    default: features-available/api.conf
    type: str
  cert_path:
    description:
      - Deprecated. Path to the public key.
    required: false
    type: str
  key_path:
    description:
      - Deprecated. Path to the private key.
    required: false
    type: str
  ca_path:
    description:
      - Deprecated. Path to the CA certificate file.
    required: false
    type: str
  ticket_salt:
    description:
      - Private key for CSR auto-signing. Required for a signing master instance.
    required: false
    type: str
  crl_path:
    description:
      - Path to the CRL file.
    required: false
    type: str
  bind_host:
    description:
      - 'The IP address the api listener should be bound to. If not specified, the ApiListener is bound to :: and listens for both IPv4 and IPv6 connections or to 0.0.0.0 if IPv6 is not supported by the operating system.'
    required: false
    type: str
  bind_port:
    description:
      - The port the api listener should be bound to. Defaults to 5665.
    required: false
    type: int
  accept_config:
    description:
      - Accept zone configuration. Defaults to false.
    required: false
    type: bool
  accept_commands:
    description:
      - Accept remote commands. Defaults to false.
    required: false
    type: bool
  max_anonymous_clients:
    description:
      - Limit the number of anonymous client connections (not configured endpoints and signing requests).
    required: false
    type: int
  cipher_list:
    description:
      - Cipher list that is allowed. For a list of available ciphers run openssl ciphers. Defaults to ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256.
    required: false
    type: str
  tls_protocolmin:
    description:
      - Minimum TLS protocol version. Since v2.11, only TLSv1.2 is supported. Defaults to TLSv1.2.
    required: false
    type: str
  tls_handshake_timeout:
    description:
      - Deprecated. TLS Handshake timeout. Defaults to 10s.
    required: false
    type: int
  connect_timeout:
    description:
      - Timeout for establishing new connections. Affects both incoming and outgoing connections. Within this time, the TCP and TLS handshakes must complete and either a HTTP request or an Icinga cluster connection must be initiated. Defaults to 15s.
    required: false
    type: int
  access_control_allow_origin:
    description:
      - Specifies an array of origin URLs that may access the API. (MDN docs)
    required: false
    type: list
    elements: str
  access_control_allow_credentials:
    description:
      - Deprecated. Indicates whether or not the actual request can be made using credentials. Defaults to true. (MDN docs)
    required: false
    type: bool
  access_control_allow_headers:
    description:
      - Deprecated. Used in response to a preflight request to indicate which HTTP headers can be used when making the actual request. Defaults to Authorization. (MDN docs)
    required: false
    type: str
  access_control_allow_methods:
    description:
      - Deprecated. Used in response to a preflight request to indicate which HTTP methods can be used when making the actual request. Defaults to GET, POST, PUT, DELETE. (MDN docs)
    required: false
    type: str
  environment:
    description:
      - Used as suffix in TLS SNI extension name; default from constant ApiEnvironment, which is empty.
    required: false
    type: str

'''

EXAMPLES = r'''
icinga.icinga.icinga2_apilistener:
  name: "api"
'''

RETURN = r'''
args:
  description: Arguments used to create the ApiListener object.
  returned: success
  type: dict
  contains:
    accept_commands:
      description: Whether the feature is configured to accept commands.
      returned: success
      type: bool
      sample: true
    accept_config:
      description: Whether the feature is configured to accept configuration.
      returned: success
      type: bool
      sample: false
    access_control_allow_origin:
      description: List of origin URLs that may access the API.
      returned: success
      type: list
      sample: null
    bind_host:
      description: The address on which to listen.
      returned: success
      type: str
      sample: "127.0.0.1"
    bind_port:
      description: The port on which to listen.
      returned: success
      type: int
      sample: 5665
    cipher_list:
      description: Cipher list that is allowed.
      returned: success
      type: list
      sample: null
    environment:
      description: Used as suffix in TLS SNI extension name.
      returned: success
      type: str
      sample: null
    max_anonymous_clients:
      description: Number of max. allowed anonymous client connections.
      returned: success
      type: int
      sample: null
    ticket_salt:
      description: Used private key for CSR auto-signing.
      returned: success
      type: str
      sample: "TicketSalt"
    tls_handshake_timeout:
      description: TLS Handshake timeout.
      returned: success
      type: bool
      sample: 10
    tls_protocolmin:
      description: Minimum TLS protocol version.
      returned: success
      type: str
      sample: "TLSv1.2"
file:
  description: Path to the file that will contain the object.
  returned: success
  type: bool
  sample: features-available/api.conf
name:
  description: The name of the ApiListener object.
  returned: success
  type: str
  sample: icinga-api
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
            file=dict(default='features-available/api.conf', type='str'),
            ticket_salt=dict(default='TicketSalt', type='str'),
            bind_host=dict(type='str'),
            bind_port=dict(type='int'),
            accept_config=dict(default=False, type='bool'),
            accept_commands=dict(default=True, type='bool'),
            max_anonymous_clients=dict(type='int'),
            cipher_list=dict(type='str'),
            tls_protocolmin=dict(type='str'),
            tls_handshake_timeout=dict(type='int'),
            access_control_allow_origin=dict(type='list', elements='str'),
            environment=dict(type='str'),
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
