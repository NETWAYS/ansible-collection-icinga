from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_filelogger
short_description: Creates information for FileLogger object.
description:
  - Returns information used to create a FileLogger object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the FileLogger object.
    required: true
    type: str
  state:
    description:
      - The state of the FileLogger object.
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
    default: "features-available/mainlog.conf"
    type: str
  path:
    description:
      - The log path.
    required: false
    default: "LogDir + /icinga2.log"
    type: str
  severity:
    description:
      - The minimum severity for this log.
    required: false
    default: "information"
    choices: [ "debug", "notice", "information", "warning", "critical" ]
    type: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_filelogger:
  name: "myfilelogger"
'''

RETURN = '''
args:
  description: Arguments used to create the FileLogger object.
  returned: success
  type: dict
  contains:
    path:
      description: The specified path.
      returned: success
      type: str
      sample: LogDir + /icinga2.log
    severity:
      description: The specified severity.
      returned: success
      type: str
      sample: information
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/mainlog.conf
name:
  description: The name of the FileLogger object.
  returned: success
  type: str
  sample: myfilelogger
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
            file=dict(default='features-available/mainlog.conf', type='str'),
            path=dict(default='LogDir + /icinga2.log', type='str'),
            severity=dict(default='information', choices=['debug', 'notice', 'information', 'warning', 'critical']),
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
