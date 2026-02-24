from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_icingaapplication
short_description: Creates information for IcingaApplication object.
description:
  - Returns information used to create a IcingaApplication object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the IcingaApplication object.
    required: true
    type: str
  state:
    description:
      - The state of the IcingaApplication object.
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
    default: "zones.conf"
    type: str
  enable_notifications:
    description:
      - Whether notifications are globally enabled.
    required: false
    type: bool
  enable_event_handlers:
    description:
      - Whether event handlers are globally enabled.
    required: false
    type: bool
  enable_flapping:
    description:
      - Whether flap detection is globally enabled.
    required: false
    type: bool
  enable_host_checks:
    description:
      - Whether active host checks are globally enabled.
    required: false
    type: bool
  enable_service_checks:
    description:
      - Whether active service checks are globally enabled.
    required: false
    type: bool
  enable_perfdata:
    description:
      - Whether performance data processing is globally enabled.
    required: false
    type: bool
  vars:
    description:
      - A dictionary containing custom variables that are available globally.
    required: false
    type: dict
  environment:
    description:
      - Specify the Icinga environment. This overrides the Environment constant specified in the configuration or on the CLI with --define.
    required: false
    type: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_icingaapplication:
  name: "myicingaapplication"
  enable_host_checks: true
  enable_service_checks: true
  enable_event_handlers: false
  enable_flapping: false
  enable_notifications: true
  enable_perfdata: true
'''

RETURN = '''
args:
  description: Arguments used to create the IcingaApplication object.
  returned: success
  type: dict
  contains:
    enable_event_handlers:
      description: Whether event handlers are globally enabled.
      returned: success
      type: bool
      sample: false
    enable_flapping:
      description: Whether flap detection is globally enabled.
      returned: success
      type: bool
      sample: false
    enable_host_checks:
      description: Whether active host checks are globally enabled.
      returned: success
      type: bool
      sample: true
    enable_notifications:
      description: Whether notifications are globally enabled.
      returned: success
      type: bool
      sample: true
    enable_perfdata:
      description: Whether performance data processing is globally enabled.
      returned: success
      type: bool
      sample: true
    enable_service_checks:
      description: Whether active service checks are globally enabled.
      returned: success
      type: bool
      sample: true
    environment:
      description: The specified environment
      returned: success
      type: str
      sample: null
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: zones.conf
name:
  description: The name of the IcingaApplication object.
  returned: success
  type: str
  sample: myicingaapplication
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
            enable_notifications=dict(type='bool'),
            enable_event_handlers=dict(type='bool'),
            enable_flapping=dict(type='bool'),
            enable_host_checks=dict(type='bool'),
            enable_service_checks=dict(type='bool'),
            enable_perfdata=dict(type='bool'),
            environment=dict(type='str'),
            _vars=dict(default=dict(), type='raw', aliases=['vars']),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')
    del args['_vars']

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
