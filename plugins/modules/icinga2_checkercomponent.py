from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_checkercomponent
short_description: Creates information for CheckerComponent object.
description:
  - Returns information used to create a CheckerComponent object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the CheckerComponent object.
    required: true
    type: str
  state:
    description:
      - The state of the CheckerComponent object.
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
    default: features-available/checker.conf
    type: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_checkercomponent:
  name: "checker"
'''

RETURN = '''
args:
  description: Arguments used to create the CheckerComponent object.
  returned: success
  type: dict
  sample: {}
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/checkercomponent.conf
name:
  description: The name of the CheckerComponent object.
  returned: success
  type: str
  sample: checker
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
            file=dict(default='features-available/checker.conf', type='str'),
        )
    )

    args = dict()
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
