from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_livestatuslistener
short_description: Creates information for LiveStatusListener object.
description:
  - Returns information used to create a LiveStatusListener object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the LiveStatusListener object.
    required: true
    type: str
  state:
    description:
      - The state of the LiveStatusListener object.
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
    default: "features-available/livestatus.conf"
    type: str
  socket_type:
    description:
      - Specifies the socket type. Can be either tcp or unix.
    required: false
    choices: [ "tcp", "unix" ]
    type: str
  bind_host:
    description:
      - Only valid when socket_type is set to tcp. Host address to listen on for connections.
    required: false
    type: str
  bind_port:
    description:
      - Only valid when socket_type is set to tcp. Port to listen on for connections.
    required: false
    type: int
  socket_path:
    description:
      - Only valid when socket_type is set to unix. Specifies the path to the UNIX socket file.
    required: false
    type: str
  compat_log_path:
    description:
      - Path to Icinga 1.x log files. Required for historical table queries. Requires CompatLogger feature enabled.
    required: false
    type: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_livestatuslistener:
  name: "mylivestatuslistener"
  socket_type: "unix"
  socket_path: "RunDir + /icinga2/cmd/livestatus"
  compat_log_path: "LogDir + /compat"
'''

RETURN = '''
args:
  description: Arguments used to create the LiveStatusListener object.
  returned: success
  type: dict
  contains:
    bind_host:
      description: The specified host.
      returned: success
      type: str
      sample: null
    bind_port:
      description: The specified port.
      returned: success
      type: int
      sample: null
    compat_log_path:
      description: The specified path to Icinga 1.x log files.
      returned: success
      type: str
      sample: LogDir + /compat
    compat_log_path:
      description: The specified path to Icinga 1.x log files.
      returned: success
      type: str
      sample: LogDir + /compat
    socket_path:
      description: The specified path to the UNIX socket file.
      returned: success
      type: str
      sample: RunDir + /icinga2/cmd/livestatus
    socket_type:
      description: The specified socket type.
      returned: success
      type: str
      sample: unix
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/livestatus.conf
name:
  description: The name of the LiveStatusListener object.
  returned: success
  type: str
  sample: mylivestatuslistener
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
            file                 = dict(default='features-available/livestatus.conf', type='str'),
            socket_type          = dict(type='str', choices=['tcp', 'unix']),
            bind_host            = dict(type='str'),
            bind_port            = dict(type='int'),
            socket_path          = dict(type='str'),
            compat_log_path      = dict(type='str'),
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
