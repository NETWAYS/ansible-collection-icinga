from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_graphitewriter
short_description: Creates information for GraphiteWriter object.
description:
  - Returns information used to create a GraphiteWriter object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the GraphiteWriter object.
    required: true
    type: str
  state:
    description:
      - The state of the GraphiteWriter object.
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
    default: "features-available/graphite.conf"
    type: str
  command:
    description:
      - The command. This is an array of individual command arguments.
    required: true
    type: list
    elements: str
  env:
    description:
      - A dictionary of macros which should be exported as environment variables prior to executing the command.
    required: false
    type: dict
  vars:
    description:
      - A dictionary containing custom variables that are specific to this command.
    required: false
    type: dict
    default: {}
  timeout:
    description:
      - The command timeout in seconds. Defaults to 1m.
    required: false
    type: str
  arguments:
    description:
      - A dictionary of command arguments.
    required: false
    type: dict
  imports:
    description:
      - List of imports for the GraphiteWriter.
    required: false
    type: list
    elements: str
    default: []
  template:
    description:
      - Whether the GraphiteWriter is a template.
    required: false
    type: bool
    default: false
'''

EXAMPLES = '''
icinga.icinga.icinga2_graphitewriter:
  name: "mygraphitewriter"
  enable_ha: false
  enable_send_metadata: true
  enable_send_thresholds: true
  host: "carbon.localdomain"
  host_name_template: "icinga.$host.name$.host.$host.check_command$"
  port: 2003
  service_name_template: "icinga.$host.name$.services.$service.name$.$service.check_command$"
'''

RETURN = '''
args:
  description: Arguments used to create the GraphiteWriter object.
  returned: success
  type: dict
  contains:
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: true
    enable_send_metadata:
      description: Whether metadata is sent.
      returned: success
      type: bool
      sample: true
    enable_send_thresholds:
      description: Whether additional threshold metrics are sent.
      returned: success
      type: bool
      sample: true
    host:
      description: The specified host.
      returned: success
      type: str
      sample: carbon.localdomain
    host_name_template:
      description: The specified host name template.
      returned: success
      type: str
      sample: icinga.$host.name$.host.$host.check_command$
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 2003
    service_name_template:
      description: The specified service name template.
      returned: success
      type: str
      sample: icinga.$host.name$.services.$service.name$.$service.check_command$
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/graphite.conf
name:
  description: The name of the GraphiteWriter object.
  returned: success
  type: str
  sample: mygraphitewriter
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
            file=dict(default='features-available/graphite.conf', type='str'),
            host=dict(type='str'),
            port=dict(type='int'),
            host_name_template=dict(type='str'),
            service_name_template=dict(type='str'),
            enable_send_thresholds=dict(type='bool'),
            enable_send_metadata=dict(type='bool'),
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
