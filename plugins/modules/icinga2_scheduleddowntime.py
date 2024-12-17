from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_scheduleddowntime
short_description: Creates information for Scheduled Downtime object.
description:
  - Returns information used to create a Scheduled Downtime object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>
options:
  name:
    description:
      - The name of the Scheduled Downtime object.
    required: true
    type: str
  state:
    description:
      - The state of the Scheduled Downtime object.
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
      - Whether the Notification is a template.
    required: false
    type: bool
    default: false
  imports:
    description:
      - List of imports for the Notification.
    required: false
    default: []
    type: list
    elements: str
  assign:
    description:
      - List of conditions for where to apply this Notification.
    required: false
    default: []
    type: list
    elements: str
  ignore:
    description:
      - List of conditions for where to ignore this Notification.
    required: false
    default: []
    type: list
    elements: str
  apply:
    description:
      - Whether this Notification should be an applied Notification.
    required: false
    default: false
    type: bool
  apply_target:
    description:
      - Whether this Notification should be a host or a service Notification.
    required: false
    type: str
    choices:
      - Host
      - Service
  display_name:
    description:
      - The display name for this Scheduled Downtime.
    required: false
    type: str
  host_name:
    description:
      - The name of the host this scheduled downtime belongs to.
    required: false
    type: str
  service_name:
    description:
      - The short name of the service this scheduled downtime belongs to. If omitted, this downtime object is treated as host downtime.
    required: false
    type: str
  author:
    description:
      - The author of the downtime.
    required: false
    type: str
  comment:
    description:
      - A comment for the downtime.
    required: false
    type: str
  fixed:
    description:
      - Whether this is a fixed downtime.
    required: false
    type: bool
  duration:
    description:
      - How long the downtime lasts. Only has an effect for flexible (non-fixed) downtimes.
    required: false
    type: str
  ranges:
    description:
      - A dictionary containing information which days and durations apply to this timeperiod.
    required: false
    type: dict
  child_options:
    description:
      - Schedule child downtimes. DowntimeNoChildren does not do anything, DowntimeTriggeredChildren schedules child downtimes triggered by this downtime, DowntimeNonTriggeredChildren schedules non-triggered downtimes.
    required: false
    type: str
    choices:
      - DowntimeNoChildren
      - DowntimeTriggeredChildren
      - DowntimeNonTriggeredChildren
'''

EXAMPLES = '''
- icinga.icinga.icinga2_scheduleddowntime:
    name: "myscheduleddowntime"
    file: "custom/scheduleddowntime.conf"
    apply: true
    apply_target: Host
    author: "myuser"
    comment: "Planned maintenance"
    assign:
      - host.vars.os == linux
    ranges:
      saturday: "10:00-11:00"
'''

RETURN = '''
args:
  description: Arguments used to create the Scheduled Downtime object.
  returned: success
  type: dict
  contains:
    assign:
      description: The specified assign rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.os == "linux"
    ignore:
      description: The specified ignore rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.distribution == "debian"
    author:
      description: The specified author.
      returned: success
      type: str
      sample: linux_admin
    comment:
      description: The specified comment.
      returned: success
      type: str
      sample: Planned maintenance
    display_name:
      description: The specified display name.
      returned: success
      type: str
      sample: Downtime - OS Upgrade
    host_name:
      description: The specified host name.
      returned: success
      type: str
      sample: example.com
    service_name:
      description: The specified service name.
      returned: success
      type: str
      sample: mysql_connection
    child_options:
      description: The specified child option.
      returned: success
      type: str
      sample: DowntimeTriggeredChildren
    duration:
      description: The specified duration.
      returned: success
      type: str
      sample: 3600
    fixed:
      description: Whether this downtime is set to be a fixed downtime instead of a flexible one.
      returned: success
      type: bool
      sample: false
    ranges:
      description: The specified ranges.
      returned: success
      type: dict
      sample:
        saturday: 08:00-10:00
apply:
  description: Whether the Scheduled Downtime is set to be an applied Scheduled Downtime.
  returned: success
  type: bool
  sample: true
apply_target:
  description: Whether the Scheduled Downtime is set to be applied to a host or service.
  returned: success
  type: str
  sample: Service
imports:
  description: Import statements made for the Scheduled Downtime object.
  returned: success
  type: list
  elements: str
  sample:
    - default-scheduleddowntime
template:
  description: Whether the Scheduled Downtime is set to be a template.
  returned: success
  type: bool
  sample: false
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/scheduleddowntime.conf
name:
  description: The name of the Scheduled Downtime object.
  returned: success
  type: str
  sample: myscheduleddowntime
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
            apply=dict(default=False, type='bool'),
            apply_target=dict(type='str', choices=['Host', 'Service']),
            display_name=dict(type='str'),
            host_name=dict(type='str'),
            service_name=dict(type='str'),
            author=dict(type='str'),
            comment=dict(type='str'),
            fixed=dict(type='bool'),
            duration=dict(type='str'),
            ranges=dict(type='dict'),
            child_options=dict(type='str', choices=['DowntimeNoChildren', 'DowntimeTriggeredChildren', 'DowntimeNonTriggeredChildren']),
            assign=dict(default=list(), type='list', elements='str'),
            ignore=dict(default=list(), type='list', elements='str'),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')
    template = args.pop('template')
    imports = args.pop('imports')
    apply = args.pop('apply')
    apply_target = args.pop('apply_target')

    module.exit_json(
        changed=False,
        args=args,
        name=name,
        order=str(order),
        state=state,
        file=file,
        template=template,
        imports=imports,
        apply=apply,
        apply_target=apply_target
    )


if __name__ == '__main__':
    main()
