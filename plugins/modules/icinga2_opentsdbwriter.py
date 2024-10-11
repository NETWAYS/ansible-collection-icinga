from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_opentsdbwriter
short_description: Creates information for OpenTsdbWriter object.
description:
  - Returns information used to create a OpenTsdbWriter object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the OpenTsdbWriter object.
    required: true
    type: str
  state:
    description:
      - The state of the OpenTsdbWriter object.
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
    default: "features-available/opentsdb.conf"
    type: str
  host:
    description:
      - OpenTSDB host address.
    required: false
    type: str
  port:
    description:
      - OpenTSDB port.
    required: false
    type: int
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
    required: false
    type: bool
  enable_generic_metrics:
    description:
      - Re-use metric names to store different perfdata values for a particular check. Use tags to distinguish perfdata instead of metric name.
    required: false
    type: bool
  host_template:
    description:
      - Specify additional tags to be included with host metrics. This requires a sub-dictionary named tags.
      - Also specify a naming prefix by setting metric.
      - More information can be found in OpenTSDB custom tags and OpenTSDB Metric Prefix. More information can be found in OpenTSDB custom tags.
    required: false
    type: dict
  service_template:
    description:
      - Specify additional tags to be included with service metrics. This requires a sub-dictionary named tags.
      - Also specify a naming prefix by setting metric.
      - More information can be found in OpenTSDB custom tags and OpenTSDB Metric Prefix.
    required: false
    type: dict
'''

EXAMPLES = '''
icinga.icinga.icinga2_opentsdbwriter:
  name: "myopentsdbwriter"
  host: "opentsdb-host.localdomain"
  port: 4242
  enable_ha: false
  host_template:
    metric: "icinga.host"
    tags:
      zone: "$host.zone$"
  service_template:
    metric: "icinga.service.$service.check_command$"
    tags:
      zone: "$service.zone$"
'''

RETURN = '''
args:
  description: Arguments used to create the OpenTsdbWriter object.
  returned: success
  type: dict
  contains:
    enable_generic_metrics:
      description: Whether re-use of metric names is enabled.
      returned: success
      type: bool
      sample: null
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: false
    host:
      description: The specified host.
      returned: success
      type: str
      sample: opentsdb-host.localdomain
    host_template:
      description: The specified host template
      returned: success
      type: dict
      sample: { "metric": "icinga.host", "tags": { "zone": "$host.zone$" } }
    port:
      description: The specified port.
      returned: success
      type: int
      sample: 4242
    service_template:
      description: The specified service template
      returned: success
      type: dict
      sample: { "metric": "icinga.service.$service.check_command$", "tags": { "zone": "$service.zone$" } }
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/opentsdb.conf
name:
  description: The name of the OpenTsdbWriter object.
  returned: success
  type: str
  sample: myopentsdbwriter
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
       argument_spec = dict(
          state                  = dict(default='present', choices=['present', 'absent']),
          name                   = dict(required=True),
          order                  = dict(default=10, type='int'),
          file                   = dict(default='features-available/opentsdb.conf', type='str'),
          host                   = dict(type='str'),
          port                   = dict(type='int'),
          enable_ha              = dict(type='bool'),
          enable_generic_metrics = dict(type='bool'),
          host_template          = dict(type='dict'),
          service_template       = dict(type='dict'),
       )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')

    module.exit_json(changed=False, args=args, name=name, order=str(order), state=state, file=file)

if __name__ == '__main__':
    main()
