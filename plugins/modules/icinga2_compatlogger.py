from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_compatlogger
short_description: Creates information for CompatLogger object.
description:
  - Returns information used to create a CompatLogger object.
version_added: 0.4.0
author:
  - Matthias Döhler <matthias.doehler@netways.de>
options:
  name:
    description:
      - The name of the CompatLogger object.
    required: true
    type: str
  state:
    description:
      - The state of the CompatLogger object.
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
    default: "features-available/compatlog.conf"
    type: str
  log_dir:
    description:
      - Path to the compat log directory.
    required: false
    type: str
  rotation_method:
    description:
      - Specifies when to rotate log files.
    required: false
    choices: [ "hourly", "daily", "weekly", "monthly" ]
    type: str
'''

EXAMPLES = '''
netways.icinga.icinga2_compatlogger:
  name: "mycompatlogger"
  log_dir: "LogDir + /compat"
  rotation_method: "monthly"
'''

RETURN = '''
args:
  description: Arguments used to create the CompatLogger object.
  returned: success
  type: dict
  contains:
    log_dir:
      description: The specified log directory.
      returned: success
      type: str
      sample: "LogDir + /compat"
    rotation_method:
      description: The specified rotation method.
      returned: success
      type: str
      sample: "MONTHLY"
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/compatlog.conf
name:
  description: The name of the CompatLogger object.
  returned: success
  type: str
  sample: mycompatlogger
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
            file=dict(default='features-available/compatlog.conf', type='str'),
            log_dir=dict(type='str'),
            rotation_method=dict(type='str', choices=['hourly', 'daily', 'weekly', 'monthly']),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')

    # Capslock if rotation_method is set
    if args.get('rotation_method', None):
        args.update({'rotation_method': args.get('rotation_method').upper()})

    module.exit_json(
        changed=False,
        args=args,
        name=name,
        order=str(order),
        state=state,
        file=file,
    )


if __name__ == '__main__':
    main()
