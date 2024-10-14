from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_sysloglogger
short_description: Creates information for SyslogLogger object.
description:
  - Returns information used to create a SyslogLogger object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the SyslogLogger object.
    required: true
    type: str
  state:
    description:
      - The state of the SyslogLogger object.
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
    default: "features-available/syslog.conf"
    type: str
  severity:
    description:
      - The minimum severity for this log. Can be debug, notice, information, warning or critical.
    required: false
    default: "warning"
    choices: [ "debug", "notice", "information", "warning", "critical" ]
    type: str
  facility:
    description:
      - Defines the facility to use for syslog entries. This can be a facility constant like FacilityDaemon.
    required: false
    default: "LOG_SYSLOG"
    choices: [ "LOG_AUTH", "LOG_AUTHPRIV", "LOG_CRON", "LOG_DAEMON", "LOG_FTP", "LOG_KERN", "LOG_LOCAL0", "LOG_LOCAL1", "LOG_LOCAL2", "LOG_LOCAL3", "LOG_LOCAL4", "LOG_LOCAL5", "LOG_LOCAL6", "LOG_LOCAL7", "LOG_LPR", "LOG_MAIL", "LOG_NEWS", "LOG_SYSLOG", "LOG_USER" ]
    type: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_sysloglogger:
  name: "mysysloglogger"
  severity: "information"
  facility: "LOG_USER"
'''

RETURN = '''
args:
  description: Arguments used to create the SyslogLogger object.
  returned: success
  type: dict
  contains:
    facility:
      description: The specified facility.
      returned: success
      type: str
      sample: LOG_USER
    severity:
      description: The specified severity.
      returned: success
      type: str
      sample: information
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: features-available/syslog.conf
name:
  description: The name of the SyslogLogger object.
  returned: success
  type: str
  sample: mysysloglogger
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
            file=dict(default='features-available/syslog.conf', type='str'),
            severity=dict(
                default='warning',
                choices=[
                    'debug', 'notice', 'information',
                    'warning', 'critical'
                ]
            ),
            facility=dict(
                default='LOG_SYSLOG',
                choices=[
                    'LOG_AUTH', 'LOG_AUTHPRIV', 'LOG_CRON',
                    'LOG_DAEMON', 'LOG_FTP', 'LOG_KERN',
                    'LOG_LOCAL0', 'LOG_LOCAL1', 'LOG_LOCAL2',
                    'LOG_LOCAL3', 'LOG_LOCAL4', 'LOG_LOCAL5',
                    'LOG_LOCAL6', 'LOG_LOCAL7', 'LOG_LPR',
                    'LOG_MAIL', 'LOG_NEWS', 'LOG_SYSLOG',
                    'LOG_USER'
                ]
            ),
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
