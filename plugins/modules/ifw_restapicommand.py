DOCUMENTATION = '''
---
name: ifw_restapicommand
short_description: Adds / Removes Icinga REST-Api Commands.
description:
  - This module allows you to add / remove Icinga for Windows REST-Api Commands.
  - You can also add Commands to the Blacklist.
version_added: 0.1.0
author:
  - Matthias Döhler <matthias.doehler@netways.de>
seealso:
  - name: Icinga REST-Api Whitelists and Blacklists
    description: Reference for how to use Whitelists and Blacklists for the Icinga REST-Api.
    link: https://icinga.com/docs/icinga-for-windows/latest/doc/110-Installation/30-API-Check-Forwarder/#whitelist-check-commands
options:
  state:
    description:
      - The state of the REST-Api Command.
    required: false
    default: present
    choices: [ "present", "absent" ]
    type: str
  command:
    description:
      - The name of a valid command available in the used PowerShell.
      - This could be something like C(Invoke-IcingaCheckCPU).
      - The use of C(*) as a wildcard is allowed.
      - O(command) is added to or removed from the chosen O(list) within the chosen O(endpoint).
    required: true
    type: list
    elements: str
  list:
    description:
      - The list the command should be added to / removed from.
    required: false
    default: whitelist
    choices: [ "whitelist", "blacklist" ]
    type: str
  endpoint:
    description:
      - The endpoint the command should be added to / removed from.
    required: false
    default: apichecks
    choices: [ "apichecks", "checker" ]
    type: str
  purge:
    description:
      - If O(purge=true), removes any command not specified in O(command) from O(list) within O(endpoint). If also setting O(state=absent), nothing will remain.
      - If O(purge=false), commands in O(command) are added or removed if necessary. Existing commands stay untouched.
    required: false
    default: false
    type: bool
'''

EXAMPLES = r'''
- name: Allow all "Invoke-IcingaCheck" commands via wildcard
  netways.icinga.ifw_restapicommand:
    state: present
    list: whitelist
    endpoint: apichecks
    command: "Invoke-IcingaCheck*"

- name: Prohibit the use of "Invoke-IcingaCheckCPU" specifically
  netways.icinga.ifw_restapicommand:
    state: present
    list: blacklist
    command: "Invoke-IcingaCheckCPU"

- name: Remove all entries from the blacklist
  netways.icinga.ifw_restapicommand:
    state: absent
    list: blacklist
    purge: true
    command: "Invoke-IcingaCheckCPU" # Some valid command needed

- name: Allow only two specific commands
  netways.icinga.ifw_restapicommand:
    state: present
    purge: true
    command:
      - "Invoke-IcingaCheckCPU"
      - "Invoke-IcingaCheckDiskHealth"
'''

RETURN = r'''
added:
  description:
    - Shows information about newly added commands.
    - They were added to RV(list) within RV(endpoint).
  returned: success
  type: list
  elements: str
  sample:
    - Invoke-IcingaCheckCPU
removed:
  description:
    - Shows information about now removed commands.
    - They were removed from RV(list) within RV(endpoint).
  returned: success
  type: list
  elements: str
  sample:
    - Invoke-IcingaCheckDiskHealth
list:
  description:
    - The used list.
  returned: success
  type: str
  sample: whitelist
endpoint:
  description:
    - The used endpoint.
  returned: success
  type: str
  sample: apichecks
'''
