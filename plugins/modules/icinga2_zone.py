from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_zone
short_description: Creates information for Zone object.
description:
  - Returns information used to create an Zone object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the Zone object.
    required: true
    type: str
  state:
    description:
      - The state of the Zone object.
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
  endpoints:
    description:
      - Array of endpoint names located in this zone.
    required: false
    type: list
    elements: str
  parent:
    description:
      - The name of the parent zone.
    required: false
    type: str
  global:
    description:
      - Whether the zone is a global zone.
    required: false
    type: bool
'''

EXAMPLES = '''
icinga.icinga.icinga2_zone:
  name: "myzone"
  endpoints: "master1.example.com"

icinga.icinga.icinga2_zone:
  name: "myzone"
  endpoints:
    - "master1.example.com"
    - "master2.example.com"
'''

RETURN = '''
args:
  description: Arguments used to create the Zone object.
  returned: success
  type: dict
  contains:
    endpoints:
      description: The specified endpoints.
      returned: success
      type: list
      elements: str
      sample: [ "agent.example.com" ]
    parent:
      description: The specified parent zone.
      returned: success
      type: str
      sample: "satellite-berlin"
    global:
      description: Whether the zone is specified as global.
      returned: success
      type: bool
      sample: true
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/zone.conf
name:
  description: The name of the Zone object.
  returned: success
  type: str
  sample: myzone
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
            endpoints=dict(type='list', elements='str'),
            parent=dict(type='str'),
            _global=dict(type='bool', aliases=['global']),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')
    del args['_global']

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
