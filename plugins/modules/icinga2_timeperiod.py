from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_timeperiod
short_description: Creates information for TimePeriod object.
description:
  - Returns information used to create an TimePeriod object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the TimePeriod object.
    required: true
    type: str
  state:
    description:
      - The state of the TimePeriod object.
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
      - A short description of the TimePeriod.
    required: false
    type: str
  ranges:
    description:
      - A dictionary containing information which days and durations apply to this TimePeriod.
    required: false
    type: dict
  prefer_includes:
    description:
      - Whether to prefer timeperiods includes or excludes.
    required: false
    type: bool
  excludes:
    description:
      - An array of TimePeriods, which should exclude from your timerange.
    required: false
    type: list
    elements: str
  includes:
    description:
      - An array of TimePeriods, which should include into your timerange.
    required: false
    type: list
    elements: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_timeperiod:
  name: "mytimeperiod"
  file: "custom/timeperiods.conf"
  ranges:
    monday: "08:00-09:00"
'''

RETURN = '''
args:
  description: Arguments used to create the TimePeriod object.
  returned: success
  type: dict
  contains:
    display_name:
      description: The specified display name.
      returned: success
      type: str
      sample: "My Nice TimePeriod"
    excludes:
      description: The specified TimePeriods to exclude.
      returned: success
      type: list
      elements: str
      sample: [ "lunch-break" ]
    includes:
      description: The specified TimePeriods to include.
      returned: success
      type: list
      elements: str
      sample: [ "work-hours" ]
    prefer_includes:
      description: Whether to prefer includes over excludes.
      returned: success
      type: bool
      sample: true
    ranges:
      description: The specified TimePeriod ranges.
      returned: success
      type: dict
      sample: { monday: "00:00-8:00,17:00-24:00" }
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/timeperiod.conf
name:
  description: The name of the TimePeriod object.
  returned: success
  type: str
  sample: mytimeperiod
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
            ranges=dict(type='dict'),
            prefer_includes=dict(type='bool'),
            excludes=dict(type='list', elements='str'),
            includes=dict(type='list', elements='str')
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
