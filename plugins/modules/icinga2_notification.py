from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_notification
short_description: Creates information for Notification object.
description:
  - Returns information used to create a Notification object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>
options:
  name:
    description:
      - The name of the Notification object.
    required: true
    type: str
  state:
    description:
      - The state of the Notification object.
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
  host_name:
    description:
      - The host this Notification belongs to. There must be a host object with that name.
    required: false
    type: str
  service_name:
    description:
      - The service this Notification belongs to. There must be a service object with that name.
    required: false
    type: str
  users:
    description:
      - A list of user names who should be notified.
    required: false
    type: list
    elements: str
  user_groups:
    description:
      - A list of user group names who should be notified.
    required: false
    type: list
    elements: str
  times:
    description:
      - A dictionary containing begin and end attributes for the notification.
    required: false
    type: dict
  command:
    description:
      - The name of the notification command which should be executed when the notification is triggered.
    required: false
    type: str
  interval:
    description:
      - The notification interval.
    required: false
    type: str
  period:
    description:
      - The name of a time period which determines when this notification should be triggered.
    required: false
    type: str
  zone:
    description:
      - The zone this object is a member of.
    required: false
    type: str
  types:
    description:
      - A list of type filters when this notification should be triggered.
    required: false
    type: list
    elements: str
    choices:
      - DowntimeStart
      - DowntimeEnd
      - DowntimeRemoved
      - Custom
      - Acknowledgement
      - Problem
      - Recovery
      - FlappingStart
      - FlappingEnd
  states:
    description:
      - A list of state filters when this notification should be triggered.
    required: false
    type: list
    elements: str
    choices:
      - Up
      - Down
      - OK
      - Warning
      - Critical
      - Unknown
  vars:
    description:
      - A dictionary containing custom variables that are specific to this Notification.
    required: false
    type: dict
    default: {}
'''

EXAMPLES = '''
- icinga.icinga.icinga2_notification:
    name: "mynotification"
    file: "custom/notification.conf"
    command: "mail-service-notification"
    apply: true
    apply_target: Service
    assign:
      - service.name
    users:
      - generic_user
    states:
      - OK
      - Warning
      - Critical
      - Unknown
    types:
      - Acknowledgement
      - Problem
      - Recovery
'''

RETURN = '''
args:
  description: Arguments used to create the Notification object.
  returned: success
  type: dict
  contains:
    assign:
      description: The specified assign rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.owner == "db-team"
    ignore:
      description: The specified ignore rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.is_agent == false
    command:
      description: The specified notification command.
      returned: success
      type: str
      sample: mail-service-notification
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
    interval:
      description: The specified notification interval.
      returned: success
      type: str
      sample: 900
    period:
      description: The specified time period object.
      returned: success
      type: str
      sample: working_hours
    times:
      description: The specified start and end times for the notification.
      returned: success
      type: dict
      sample:
        begin: 300
        end: 3600
    states:
      description: The specified states for which to send notifications.
      returned: success
      type: list
      elements: str
      sample:
        - Critical
        - Unknown
    types:
      description: The specified transition types for which to send notifications.
      description: WIP
      returned: success
      type: list
      elements: str
      sample:
        - DowntimeStart
        - DowntimeEnd
        - DowntimeRemoved
        - Acknowledgement
        - Problem
    users:
      description: The specified users.
      returned: success
      type: list
      elements: str
      sample:
        - db_admin
        - manager
    user_groups:
      description: The specified user groups.
      returned: success
      type: list
      elements: str
      sample:
        - db_admins
        - first_level_support
    zone:
      description: The specified zone.
      returned: success
      type: str
      sample: global-templates
apply:
  description: Whether the Notification is set to be an applied Notification.
  returned: success
  type: bool
  sample: true
apply_target:
  description: Whether the Notification is set to be applied to a host or service.
  returned: success
  type: str
  sample: Service
imports:
  description: Import statements made for the Notification object.
  returned: success
  type: list
  elements: str
  sample:
    - default-notification
template:
  description: Whether the Notification is set to be a template.
  returned: success
  type: bool
  sample: false
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/Notification.conf
name:
  description: The name of the Notification object.
  returned: success
  type: str
  sample: myNotification
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
            apply=dict(default=False, type='bool'),
            apply_target=dict(type='str', choices=['Host', 'Service']),
            imports=dict(default=list(), type='list', elements='str'),
            host_name=dict(type='str'),
            service_name=dict(type='str'),
            _vars=dict(default=dict(), type='raw', aliases=['vars']),
            users=dict(type='list', elements='str'),
            user_groups=dict(type='list', elements='str'),
            times=dict(type='dict'),
            command=dict(type='str'),
            interval=dict(type='str'),
            period=dict(type='str'),
            zone=dict(type='str'),
            types=dict(type='list', elements='str', choices=['DowntimeStart', 'DowntimeEnd', 'DowntimeRemoved', 'Custom', 'Acknowledgement', 'Problem', 'Recovery', 'FlappingStart', 'FlappingEnd']),
            states=dict(type='list', elements='str', choices=['Up', 'Down', 'OK', 'Warning', 'Critical', 'Unknown']),
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
    del args['_vars']

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
