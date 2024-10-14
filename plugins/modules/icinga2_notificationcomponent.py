from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_notificationcomponent
short_description: Creates information for NotificationComponent object.
description:
  - Returns information used to create a NotificationComponent object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the NotificationComponent object.
    required: true
    type: str
  state:
    description:
      - The state of the NotificationComponent object.
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
    default: "features-available/notification.conf"
    type: str
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
      - Disabling this currently only affects reminder notifications.
    required: false
    type: bool
'''

EXAMPLES = '''
icinga.icinga.icinga2_notificationcomponent:
  name: "mynotificationcomponent"
  enable_ha: true
'''

RETURN = '''
args:
  description: Arguments used to create the NotificationComponent object.
  returned: success
  type: dict
  contains:
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: true
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/notification.conf
name:
  description: The name of the NotificationComponent object.
  returned: success
  type: str
  sample: mynotificationcomponent
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
            file=dict(default='features-available/notification.conf', type='str'),
            enable_ha=dict(type='bool'),
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
