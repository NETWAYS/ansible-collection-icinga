from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_dependency
short_description: Creates information for Dependency object.
description:
  - Returns information used to create a Dependency object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the Dependency object.
    required: true
    type: str
  state:
    description:
      - The state of the Dependency object.
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
      - Decides whether a template or an object will be created.
    required: false
    default: false
    type: bool
  imports:
    description:
      - List of imports to make in order to create the Dependency.
    required: false
    default: []
    type: list
    elements: str
  apply:
    description:
      - Whether this Dependency should be an applied Dependency.
    required: false
    default: false
    type: bool
  apply_target:
    description:
      - The Icinga 2 object type the Dependency should be applied to.
    required: false
    type: str
  parent_host_name:
    description:
      - The name of the parent host object.
      - This is the host to depend on.
    required: false
    type: str
  parent_service_name:
    description:
      - The name of the parent host's service to depend on.
      - If provided, the child host or service will depend on this parent service.
    required: false
    type: str
  child_host_name:
    description:
      - The name of the child host object.
      - This is the dependent host.
    required: false
    type: str
  child_service_name:
    description:
      - The name of the child's service object.
      - If provided, this service will depend on the parent host or service.
    required: false
    type: str
  disable_checks:
    description:
      - Whether to disable checks (i.e., don’t schedule active checks and drop passive results) when this dependency fails.
    required: false
    type: bool
  disable_notifications:
    description:
      - Whether to disable notifications when this dependency fails.
    required: false
    type: bool
  ignore_soft_states:
    description:
      - Whether to ignore soft states for the reachability calculation.
    required: false
    type: bool
  period:
    description:
      - Time period object during which this dependency is enabled
    required: false
    type: str
  states:
    description:
      - A list of state filters when this dependency should be OK.
      - Defaults to [ OK, Warning ] for services and [ Up ] for hosts (within Icinga 2).
    required: false
    type: list
    elements: str
  assign:
    description:
      - List of assign rules to use.
    required: false
    type: list
    elements: str
  ignore:
    description:
      - List of ignore rules to use.
    required: false
    type: list
    elements: str
'''

EXAMPLES = '''
# A service depending on a parent's service
icinga.icinga.icinga2_dependency:
  name: "service-to-service-dependency"
  file: "custom/dependencies.conf"
  parent_host_name: "dbhost"
  parent_service_name: "mysql-service"
  child_host_name: "webserver"
  child_service_name: "myapplication"


# Multiple hosts depending on common parent host
icinga.icinga.icinga2_dependency:
  name: "apply-host-to-host-dependency"
  file: "custom/dependencies.conf"
  apply: true
  apply_target: "Host"
  parent_host_name: "example-router"
  disable_checks: false
  disable_notifications: true
  assign:
    - "example-router == host.vars.parent_router"
'''

RETURN = '''
args:
  description: Arguments used to create the Dependency object.
  returned: success
  type: dict
  contains:
    assign:
      description: The list of used assign rules.
      returned: success
      type: list
      elements: str
      sample: [ "host.vars.os == linux" ]
    child_host_name:
      description: The specified child host's name.
      returned: success
      type: str
      sample: null
    child_service_name:
      description: The specified child service's name.
      returned: success
      type: str
      sample: null
    disable_checks:
      description: Whether checks are disabled.
      returned: success
      type: bool
      sample: false
    disable_notifications:
      description: Whether notifications are disabled.
      returned: success
      type: bool
      sample: true
    ignore:
      description: The list of used ignore rules.
      returned: success
      type: list
      elements: str
      sample: [ "host.vars.os_family == suse" ]
    ignore_soft_states:
      description: Whether soft states are ignored.
      returned: success
      type: bool
      sample: false
    parent_host_name:
      description: The specified parent host's name.
      returned: success
      type: str
      sample: example-router
    parent_service_name:
      description: The specified parent service's name.
      returned: success
      type: str
      sample: null
    period:
      description: The specified time period's name.
      returned: success
      type: str
      sample: null
    states:
      description: The specified list states that are considered OK.
      returned: success
      type: list
      elements: str
      sample: [ "OK" ]
apply:
  description: Whether this Dependency is an applied Dependency.
  returned: success
  type: bool
  sample: true
apply_target:
  description: Whether this Dependency is applied to hosts or services.
  returned: success
  type: str
  sample: Host
imports:
  description: Import statements made for the Dependency object.
  returned: success
  type: list
  elements: str
  sample: [ "only-ok-allowed" ]
template:
  description: Whether the Dependency is set to be a template.
  returned: success
  type: bool
  sample: false
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/dependencies.conf
name:
  description: The name of the Dependency object.
  returned: success
  type: str
  sample: mydependency
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
            apply_target=dict(type='str'),
            parent_host_name=dict(type='str'),
            parent_service_name=dict(type='str'),
            child_host_name=dict(type='str'),
            child_service_name=dict(type='str'),
            disable_checks=dict(type='bool'),
            disable_notifications=dict(type='bool'),
            ignore_soft_states=dict(type='bool'),
            period=dict(type='str'),
            states=dict(type='list', elements='str'),
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
