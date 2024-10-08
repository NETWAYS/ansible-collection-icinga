from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = '''
name: icinga2_apiuser
short_description: Creates information for ApiUser object.
description:
  - Returns information used to create an ApiUser object.
version_added: 0.1.0
author:
  - Lennart Betz <lennart.betz@netways.de>

options:
  name:
    description:
      - The name of the ApiUser object.
    required: true
    type: str
  state:
    description:
      - The state of the ApiUser object.
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
  password:
    description:
      - Password string.
    required: false
    type: str
  client_cn:
    description:
      - Client Common Name (CN).
    required: false
    type: str
  permissions:
    description:
      - Array of permissions.
    required: true
    type: list
    elements: str
'''

EXAMPLES = '''
icinga.icinga.icinga2_apiuser:
  name: "myapiuser"
  permissions:
    - "objects/query/Host"
    - "objects/query/Service"
'''

RETURN = '''
args:
  description: Arguments used to create the ApiUser object.
  returned: success
  type: dict
  contains:
    client_cn:
      description: The specified client_cn.
      returned: success
      type: str
      sample: "satellite1.localdomain"
    password:
      description: The specified password.
      returned: success
      type: str
      sample: "super-secret"
    permissions:
      description: The specified password.
      returned: success
      type: list
      sample: [ "objects/query/Host", "objects/query/Service" ]
file:
  description: Path to the file that will contain the object.
  returned: success
  type: str
  sample: custom/apiusers.conf
name:
  description: The name of the ApiUser object.
  returned: success
  type: str
  sample: myapiuser
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
            password=dict(type='str'),
            client_cn=dict(type='str'),
            permissions=dict(type='list'),
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
