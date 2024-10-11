from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_externalcommandlistener
short_description: Creates information for ExternalCommandListener object.
description:
  - Returns information used to create an ExternalCommandListener object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the ExternalCommandListener object.
    required: true
    type: str
  state:
    description:
      - The state of the ExternalCommandListener object.
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
    default: "features-available/command.conf"
    type: str
  command_path:
    description:
      - Path to the command pipe.
    required: false
    default: "features-available/command.conf"
    type: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_externalcommandlistener:
  name: "myexternalcommandlistener"
'''

RETURN = '''
args:
  description: Arguments used to create the ExternalCommandListener object.
  returned: success
  type: dict
  contains:
    command_path:
      description: The specified path to the pipe.
      returned: success
      type: str
      sample: null
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/command.conf
name:
  description: The name of the ExternalCommandListener object.
  returned: success
  type: str
  sample: myexternalcommandlistener
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
            file=dict(default='features-available/command.conf', type='str'),
            command_path=dict(type='str'),
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
