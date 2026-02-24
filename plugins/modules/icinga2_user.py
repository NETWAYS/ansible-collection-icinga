from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_user
short_description: Creates information for User object.
description:
  - Returns information used to create a User object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the User object.
    required: true
    type: str
  state:
    description:
      - The state of the User object.
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
  template:
    description:
      - Whether the User is a template.
    required: false
    type: bool
    default: false
  imports:
    description:
      - List of imports for the User.
    required: false
    default: []
    type: list
    elements: str
  display_name:
    description:
      - A short description of the user.
    required: false
    type: str
  email:
    description:
      - An email string for this user. Useful for notification commands.
    required: false
    type: str
  pager:
    description:
      - A pager string for this user. Useful for notification commands.
    required: false
    type: str
  vars:
    description:
      - A dictionary containing custom variables that are specific to this user.
    required: false
    type: dict
  groups:
    description:
      - An array of group names.
    required: false
    default: []
    type: list
    elements: str
  enable_notifications:
    description:
      - Whether notifications are enabled for this user.
    required: false
    type: bool
  period:
    description:
      - The name of a time period which determines when a notification for this user should be triggered. Not set by default (effectively 24x7).
    required: false
    type: str
  types:
    description:
      - A set of type filters when a notification for this user should be triggered. By default everything is matched.
    required: false
    default: []
    type: list
    elements: str
  states:
    description:
      - A set of state filters when a notification for this should be triggered. By default everything is matched.
    required: false
    default: []
    type: list
    elements: str
'''

EXAMPLES = '''
- icinga.icinga.icinga2_user:
    name: "myuser"
    file: "custom/users.conf"
    display_name: "My User Display Name"
    email: "myuser@localhost"
    enable_notifications: true
    groups:
      - "linux-admins"
      - "databse-admins"
    states:
      - "Down"
      - "Warning"
      - "Critical"
    types:
      - "Problem"
'''

RETURN = '''
args:
  description: Arguments used to create the User object.
  returned: success
  type: dict
  contains:
    display_name:
      description: The specified display name.
      returned: success
      type: str
      sample: My User Display Name
    email:
      description: The specified email.
      returned: success
      type: str
      sample: myuser@localhost
    enable_notifications:
      description: Whether notifications are enabled for this User.
      returned: success
      type: bool
      sample: true
    groups:
      description: The specified groups.
      returned: success
      type: list
      elements: str
      sample:
        - linux-admins
        - database-admins
    pager:
      description: The specified pager for this User.
      returned: success
      type: str
      sample: icingaadmin@localhost.localdomain
    period:
      description: The specified period.
      returned: success
      type: str
      sample: 24x7
    states:
      description: The specified states.
      returned: success
      type: list
      elements: str
      sample:
        - Down
        - Warning
        - Critical
    types:
      description: The specified types.
      returned: success
      type: list
      elements: str
      sample:
        - Problem
imports:
  description: Import statements made for the User object.
  returned: success
  type: list
  elements: str
  sample: [ "default-template", "department-a" ]
template:
  description: Whether the User is set to be a template.
  returned: success
  type: bool
  sample: false
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/users.conf
name:
  description: The name of the User object.
  returned: success
  type: str
  sample: myuser
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
            display_name=dict(type='str'),
            email=dict(type='str'),
            pager=dict(type='str'),
            _vars=dict(default=dict(), type='raw', aliases=['vars']),
            groups=dict(type='list', elements='str'),
            enable_notifications=dict(type='bool'),
            period=dict(type='str'),
            types=dict(type='list', elements='str'),
            states=dict(type='list', elements='str'),
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
