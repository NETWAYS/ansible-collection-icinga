from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_service
short_description: Creates information for Service object.
description:
  - Returns information used to create a Service object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>
options:
  name:
    description:
      - The name of the Service object.
    required: true
    type: str
  state:
    description:
      - The state of the Service object.
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
      - Whether the Service is a template.
    required: false
    type: bool
    default: false
  imports:
    description:
      - List of imports for the Service.
    required: false
    default: []
    type: list
    elements: str
  assign:
    description:
      - List of conditions for where to apply this Service.
    required: false
    default: []
    type: list
    elements: str
  ignore:
    description:
      - List of conditions for where to ignore this Service.
    required: false
    default: []
    type: list
    elements: str
  apply:
    description:
      - Whether this Service should be an applied Service.
    required: false
    default: false
    type: bool
  apply_for:
    description:
      - String specifying the iterator for a Service of form "apply Service for (<ITERATOR>)".
    required: false
    default: false
    type: bool
  display_name:
    description:
      - A short description of the Service (e.g. displayed by external interfaces instead of the name if set).
    required: false
    type: str
  host_name:
    description:
      - The host this service belongs to. There must be a host object with that name.
    required: false
    type: str
  groups:
    description:
      - A list of service groups this Service belongs to.
    required: false
    type: list
    elements: str
  vars:
    description:
      - A dictionary containing custom variables that are specific to this Service.
    required: false
    type: dict
    default: {}
  check_command:
    description:
      - The name of the check command.
    required: false
    type: str
  max_check_attempts:
    description:
      - The number of times a Service is re-checked before changing into a hard state. Defaults to 3.
    required: false
    type: int
  check_period:
    description:
      - The name of a time period which determines when this Service should be checked. Not set by default (effectively 24x7).
    required: false
    type: str
  check_timeout:
    description:
      - Check command timeout in seconds. Overrides the CheckCommand's timeout attribute."
    required: false
    type: str
  check_interval:
    description:
      - The check interval (in seconds). This interval is used for checks when the Service is in a HARD state. Defaults to 5m.
    required: false
    type: str
  retry_interval:
    description:
      - 'The retry interval (in seconds). This interval is used for checks when the Service is in a SOFT state. Defaults to 1m. Note: This does not affect the scheduling after a passive check result.'
    required: false
    type: str
  enable_notifications:
    description:
      - Whether notifications are enabled. Defaults to true.
    required: false
    type: bool
  enable_active_checks:
    description:
      - Whether active checks are enabled. Defaults to true.
    required: false
    type: bool
  enable_passive_checks:
    description:
      - Whether passive checks are enabled. Defaults to true.
    required: false
    type: bool
  enable_event_handler:
    description:
      - Enables event handlers for this Service. Defaults to true.
    required: false
    type: bool
  enable_flapping:
    description:
      - Whether flap detection is enabled. Defaults to false.
    required: false
    type: bool
  enable_perfdata:
    description:
      - Whether performance data processing is enabled. Defaults to true.
    required: false
    type: bool
  event_command:
    description:
      - The name of an event command that should be executed every time the Service's state changes or the Service is in a SOFT state.
    required: false
    type: str
  flapping_threshold_high:
    description:
      - Flapping upper bound in percent for a Service to be considered flapping. Default 30.0
    required: false
    type: float
  flapping_threshold_low:
    description:
      - Flapping lower bound in percent for a Service to be considered  not flapping. Default 25.0
    required: false
    type: float
  volatile:
    description:
      - Treat all state changes as HARD changes. See here for details. Defaults to false.
    required: false
    type: bool
  zone:
    description:
      - The zone this object is a member of. Please read the distributed monitoring chapter for details.
    required: false
    type: str
  command_endpoint:
    description:
      - The endpoint where commands are executed on.
    required: false
    type: str
  notes:
    description:
      - Notes for the Service.
    required: false
    type: str
  notes_url:
    description:
      - URL for notes for the Service (for example, in notification commands).
    required: false
    type: str
  icon_image:
    description:
      - Icon image for the Service. Used by external interfaces only.
    required: false
    type: str
  icon_image_alt:
    description:
      - Icon image description for the Service. Used by external interface only.
    required: false
    type: str
'''

EXAMPLES = '''
- icinga.icinga.icinga2_service:
    name: "myservice"
    file: "custom/service.conf"
    host_name: "host.example.com"
    check_command: "ping"

- icinga.icinga.icinga2_service:
    name: "myservice"
    file: "custom/service.conf"
    check_command: "disk"
    apply: true
    assign: host.vars.disks
    apply_for: disk_x in host.vars.disks
    vars:
      disk_partitions: disk_x
'''

RETURN = '''
args:
  description: Arguments used to create the Service object.
  returned: success
  type: dict
  contains:
    assign:
      description: The specified assign rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.disks
    ignore:
      description: The specified ignore rule.
      returned: success
      type: list
      elements: str
      sample:
        - host.vars.is_agent == false
    check_command:
      description: The specified check command.
      returned: success
      type: str
      sample: disk
    check_interval:
      description: The specified check interval.
      returned: success
      type: str
      sample: 120s
    check_period:
      description: The specified check period.
      returned: success
      type: str
      sample: 24x7
    check_timeout:
      description: The specified check timeout.
      returned: success
      type: str
      sample: 60s
    command_endpoint:
      description: The specified command endpoint.
      returned: success
      type: str
      sample: icingaweb2.example.com
    display_name:
      description: The specified display name.
      returned: success
      type: str
      sample: My custom display name
    enable_active_checks:
      description: Whether active checks are enabled.
      returned: success
      type: bool
      sample: true
    enable_event_handler:
      description: Whether event handler is enabled.
      returned: success
      type: bool
      sample: true
    enable_flapping:
      description: Whether flap detection is enabled.
      returned: success
      type: bool
      sample: true
    enable_notifications:
      description: Whether notifications are enabled.
      returned: success
      type: bool
      sample: true
    enable_passive_checks:
      description: Whether passive checks are enabled.
      returned: success
      type: bool
      sample: true
    enable_perfdata:
      description: Whether performance data processing is enabled.
      returned: success
      type: bool
      sample: true
    event_command:
      description: The specified event command.
      returned: success
      type: str
      sample: send-event-to-collector
    flapping_threshold_high:
      description: The specified upper bound for flap detection.
      returned: success
      type: float
      sample: 30.0
    flapping_threshold_low:
      description: The specified lower bound for flap detection.
      returned: success
      type: float
      sample: 25.0
    groups:
      description: The specified groups.
      returned: success
      type: list
      elements: str
      sample:
        - group1
        - group2
    host_name:
      description: The specified host.
      returned: success
      type: str
      sample: host.example.com
    icon_image:
      description: The specified icon image.
      returned: success
      type: str
      sample: sitemap
    icon_image_alt:
      description: The specified icon image description.
      returned: success
      type: str
      sample: Sitemap - Icon showing tree-like structure
    max_check_attempts:
      description: The specified maximum number of check attempts.
      returned: success
      type: int
      sample: 5
    notes:
      description: The specified notes.
      returned: success
      type: str
      sample: This is a dummy object
    notes_url:
      description: The specified notes url.
      returned: success
      type: str
      sample: https://docs.example.com
    retry_interval:
      description: The specified retry interval.
      returned: success
      type: str
      sample: 30s
    volatile:
      description: Whether this Service is volatile.
      returned: success
      type: bool
      sample: false
    zone:
      description: The specified zone.
      returned: success
      type: str
      sample: master
apply:
  description: Whether the Service is set to be an applied Service.
  returned: success
  type: bool
  sample: true
apply_for:
  description: The specified apply for iterator.
  returned: success
  type: str
  sample: disk in host.vars.os.disks
imports:
  description: Import statements made for the Service object.
  returned: success
  type: list
  elements: str
  sample:
    - default-template
    - linux-template
template:
  description: Whether the Service is set to be a template.
  returned: success
  type: bool
  sample: false
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/service.conf
name:
  description: The name of the Service object.
  returned: success
  type: str
  sample: myservice
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
            apply_for=dict(type='str'),
            imports=dict(default=list(), type='list', elements='str'),
            display_name=dict(type='str'),
            host_name=dict(type='str'),
            groups=dict(type='list', elements='str'),
            _vars=dict(default=dict(), type='raw', aliases=['vars']),
            check_command=dict(type='str'),
            max_check_attempts=dict(type='int'),
            check_period=dict(type='str'),
            check_timeout=dict(type='str'),
            check_interval=dict(type='str'),
            retry_interval=dict(type='str'),
            enable_notifications=dict(type='bool'),
            enable_active_checks=dict(type='bool'),
            enable_passive_checks=dict(type='bool'),
            enable_event_handler=dict(type='bool'),
            enable_flapping=dict(type='bool'),
            flapping_threshold_high=dict(type='float'),
            flapping_threshold_low=dict(type='float'),
            enable_perfdata=dict(type='bool'),
            event_command=dict(type='str'),
            volatile=dict(type='bool'),
            zone=dict(type='str'),
            command_endpoint=dict(type='str'),
            notes=dict(type='str'),
            notes_url=dict(type='str'),
            icon_image=dict(type='str'),
            icon_image_alt=dict(type='str'),
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
    apply_for = args.pop('apply_for')
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
        apply_for=apply_for
    )


if __name__ == '__main__':
    main()
