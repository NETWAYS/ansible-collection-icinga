from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_endpoint
short_description: Creates information for Endpoint object.
description:
  - Returns information used to create an Endpoint object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the Endpoint object.
    required: true
    type: str
  state:
    description:
      - The state of the Endpoint object.
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
    default: zones.conf
    type: str
  host:
    description:
      - The hostname/IP address of the remote Icinga 2 instance.
      - Configures this Icinga 2 instance to actively connect to the given Endpoint.
    required: false
    type: str
  port:
    description:
      - The port of the remote Icinga 2 instance.
    required: false
    type: int
  log_duration:
    description:
      - Duration for keeping replay logs on connection loss. Attribute is specified in seconds.
      - If log_duration is set to 0, replaying logs is disabled.
      - You could also specify the value in human readable format like 10m for 10 minutes or 1h for one hour.
    required: false
    type: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_endpoint:
  name: "satellite1"
  host: "192.168.2.75"
  log_duration: "2d"
  port: 5667
'''

RETURN = '''
args:
  description: Arguments used to create the Endpoint object.
  returned: success
  type: dict
  contains:
    host:
      description: The specified host.
      returned: success
      type: str
      sample: 192.168.2.75
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 5667
    host:
      description: The specified log duration.
      returned: success
      type: str
      sample: 2d
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: zones.conf
name:
  description: The name of the Endpoint object.
  returned: success
  type: str
  sample: satellite1
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
            file=dict(default='zones.conf', type='str'),
            host=dict(type='str'),
            port=dict(type='int'),
            log_duration=dict(type='str'),
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
