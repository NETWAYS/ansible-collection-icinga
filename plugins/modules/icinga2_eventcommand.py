from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_eventcommand
short_description: Creates information for EventCommand object.
description:
  - Returns information used to create an EventCommand object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the EventCommand object.
    required: true
    type: str
  state:
    description:
      - The state of the EventCommand object.
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
  command:
    description:
      - The command. This is an array of individual command arguments.
    required: true
    type: list
    elements: str
  env:
    description:
      - A dictionary of macros which should be exported as environment variables prior to executing the command.
    required: false
    type: dict
  vars:
    description:
      - A dictionary containing custom variables that are specific to this command.
    required: false
    type: dict
    default: {}
  timeout:
    description:
      - The command timeout in seconds. Defaults to 1m.
    required: false
    type: str
  arguments:
    description:
      - A dictionary of command arguments.
    required: false
    type: dict
  imports:
    description:
      - List of imports for the EventCommand.
    required: false
    type: list
    elements: str
    default: []
  template:
    description:
      - Whether the EventCommand is a template.
    required: false
    type: bool
    default: false
'''

EXAMPLES = '''
icinga.icinga.icinga2_eventcommand:
  name: "restart-httpd-event"
  file: "custom/eventcommands.conf"
  command:
    - /opt/bin/restart-httpd.sh
'''

RETURN = '''
args:
  description: Arguments used to create the EventCommand object.
  returned: success
  type: dict
  contains:
    arguments:
      description: The arguments passed.
      returned: success
      type: dict
      sample: null
    command:
      description: The strings that make up the command.
      returned: success
      type: list
      elements: str
      sample: [ "restart-httpd-event.sh" ]
    env:
      description: The specified macros.
      returned: success
      type: dict
      sample: null
    timeout:
      description: The specified timeout.
      returned: success
      type: str
      sample: 15s
imports:
  description: Import statements made for the EventCommand object.
  returned: success
  type: list
  elements: str
  sample: []
template:
  description: Whether the EventCommand is set to be a template.
  returned: success
  type: bool
  sample: false
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/eventcommands.conf
name:
  description: The name of the EventCommand object.
  returned: success
  type: str
  sample: restart-httpd-event
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
            file=dict(required=True, type='str'),
            template=dict(default=False, type='bool'),
            imports=dict(default=list(), type='list', elements='str'),
            command=dict(required=True, type='list', elements='str'),
            env=dict(type='dict', elements='str'),
            _vars=dict(default=dict(), type='raw', aliases=['vars']),
            timeout=dict(type='str'),
            arguments=dict(type='dict'),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')
    template = args.pop('template')
    imports = args.pop('imports')
    del args['_vars']

    module.exit_json(
        changed=False,
        args=args,
        name=name,
        order=str(order),
        state=state,
        file=file,
        template=template,
        imports=imports
    )


if __name__ == '__main__':
    main()
