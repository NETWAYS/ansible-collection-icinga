from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_servicegroup
short_description: Creates information for ServiceGroup object.
description:
  - Returns information used to create a ServiceGroup object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the ServiceGroup object.
    required: true
    type: str
  state:
    description:
      - The state of the ServiceGroup object.
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
  display_name:
    description:
      - A short description of the ServiceGroup.
    required: false
    type: str
  groups:
    description:
      - An array of nested group names.
    required: false
    default: []
    type: list
    elements: str
  assign:
    description:
      - List of conditions for where to apply this ServiceGroup.
    required: false
    default: []
    type: list
    elements: str
  ignore:
    description:
      - List of conditions for where to ignore this ServiceGroup.
    required: false
    default: []
    type: list
    elements: str
'''

EXAMPLES = '''
- icinga.icinga.icinga2_servicegroup:
    name: "myservicegroup"
    file: "custom/servicegroup.conf"
    display_name: "My ServiceGroup Display Name"
    assign:
      - host.vars.os == Linux
'''

RETURN = '''
args:
  description: Arguments used to create the ServiceGroup object.
  returned: success
  type: dict
  contains:
    assign:
      description: The specified assign rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.os == linux
    display_name:
      description: The specified display name.
      returned: success
      type: str
      sample: My ServiceGroup Display Name
    groups:
      description: The specified groups.
      returned: success
      type: list
      elements: str
      sample:
        - group1
        - group2
    ignore:
      description: The specified ignore rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.os == windows
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/servicegroup.conf
name:
  description: The name of the ServiceGroup object.
  returned: success
  type: str
  sample: myservicegroup
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
            display_name=dict(type='str'),
            groups=dict(type='list', elements='str'),
            assign=dict(default=list(), type='list', elements='str'),
            ignore=dict(default=list(), type='list', elements='str')
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
