from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_perfdatawriter
short_description: Creates information for PerfdataWriter object.
description:
  - Returns information used to create a PerfdataWriter object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the PerfdataWriter object.
    required: true
    type: str
  state:
    description:
      - The state of the PerfdataWriter object.
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
    default: "features-available/perfdata.conf"
    type: str
  host_perfdata_path:
    description:
      - Path to the host performance data file.
    required: false
    type: str
  service_perfdata_path:
    description:
      - Path to the service performance data file.
    required: false
    type: str
  host_temp_path:
    description:
      - Path to the temporary host file.
    required: false
    type: str
  service_temp_path:
    description:
      - Path to the temporary service file.
    required: false
    type: str
  host_format_template:
    description:
      - Host Format template for the performance data file.
    required: false
    type: str
  service_format_template:
    description:
      - Service Format template for the performance data file.
    required: false
    type: str
  rotation_interval:
    description:
      - Rotation interval for the files specified in V(host_perfdata_path) and V(host_perfdata_path).
    required: false
    type: str
  enable_ha:
    description:
      - Enable the high availability functionality. Only valid in a cluster setup.
    required: false
    type: bool
'''

EXAMPLES = '''
icinga.icinga.icinga2_perfdatawriter:
  name: "myperfdatawriter"
  enable_ha: true
  host_perfdata_path: "/var/spool/icinga2/perfdata/host-perfdata"
  host_temp_path: "/var/spool/icinga2/tmp/host-perfdata"
  rotation_interval: 60
  service_perfdata_path: "/var/spool/icinga2/perfdata/service-perfdata"
  service_temp_path: "/var/spool/icinga2/tmp/service-perfdata"
'''

RETURN = '''
args:
  description: Arguments used to create the PerfdataWriter object.
  returned: success
  type: dict
  contains:
    enable_ha:
      description: Whether HA is enabled.
      returned: success
      type: bool
      sample: true
    host_format_template:
      description: The specified host format template for the performance data file.
      returned: success
      type: str
      sample: null
    host_perfdata_path:
      description: The specified path to the host performance data file.
      returned: success
      type: str
      sample: /var/spool/icinga2/perfdata/host-perfdata
    host_temp_path:
      description: The specified path the temporary host file.
      returned: success
      type: str
      sample: /var/spool/icinga2/tmp/host-perfdata
    rotation_interval:
      description: The arguments passed.
      returned: success
      type: str
      sample: 60
    service_format_template:
      description: The specified service format template for the performance data file.
      returned: success
      type: str
      sample: null
    service_perfdata_path:
      description: The specified path to the service performance data file.
      returned: success
      type: str
      sample: /var/spool/icinga2/perfdata/service-perfdata
    service_temp_path:
      description: The specified path the temporary service file.
      returned: success
      type: str
      sample: /var/spool/icinga2/tmp/service-perfdata
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/perfdata.conf
name:
  description: The name of the PerfdataWriter object.
  returned: success
  type: str
  sample: myperfdatawriter
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
            state                   = dict(default='present', choices=['present', 'absent']),
            name                    = dict(required=True),
            order                   = dict(default=10, type='int'),
            file                    = dict(default='features-available/perfdata.conf', type='str'),
            host_perfdata_path      = dict(type='str'),
            service_perfdata_path   = dict(type='str'),
            host_temp_path          = dict(type='str'),
            service_temp_path       = dict(type='str'),
            host_format_template    = dict(type='str'),
            service_format_template = dict(type='str'),
            rotation_interval       = dict(type='str'),
            enable_ha               = dict(type='bool'),
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
