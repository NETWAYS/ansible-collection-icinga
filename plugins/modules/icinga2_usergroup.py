from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_usergroup
short_description: Creates information for UserGroup object.
description:
  - Returns information used to create a UserGroup object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the UserGroup object.
    required: true
    type: str
  state:
    description:
      - The state of the UserGroup object.
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
      - A short description of the UserGroup.
    required: false
    type: str
  groups:
    description:
      - An array of nested group names.
    required: false
    default: []
    type: list
    elements: str
'''

EXAMPLES = '''
- icinga.icinga.icinga2_usergroup:
    name: "myusergroup"
    file: "custom/usergroup.conf"
    display_name: "My UserGroup Display Name"
'''

RETURN = '''
args:
  description: Arguments used to create the UserGroup object.
  returned: success
  type: dict
  contains:
    display_name:
      description: The specified display name.
      returned: success
      type: str
      sample: My UserGroup Display Name
    groups:
      description: The specified groups.
      returned: success
      type: list
      elements: str
      sample:
        - group1
        - group2
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/usergroup.conf
name:
  description: The name of the UserGroup object.
  returned: success
  type: str
  sample: myusergroup
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
