DOCUMENTATION = '''
---
name: ifw_backgrounddaemon
short_description: (Un-)Registers an IfW Background Daemon.
description:
  - This module allows you to register/unregister an Icinga for Windows Background Daemon.
  - They are used to collect metrics over time or used for the IfW API Check Forwarder.
version_added: 0.1.0
author:
  - Matthias Döhler <matthias.doehler@netways.de>
seealso:
  - name: Icinga for Windows Background Daemons
    description: Reference for the Background Daemons.
    link: https://icinga.com/docs/icinga-for-windows/latest/doc/110-Installation/05-Background-Daemons/
  - name: Icinga for Windows API Check Forwarder
    description: Reference for a possible use case regarding the API Check Forwarder.
    link: https://icinga.com/docs/icinga-for-windows/latest/doc/110-Installation/30-API-Check-Forwarder/
options:
  state:
    description:
      - The state of the Background Daemon.
    required: false
    default: present
    choices: [ "present", "absent" ]
    type: str
  command:
    description:
      - The name of a valid command available in the used PowerShell.
      - This could be something like C(Start-MyCustomDaemon).
      - If O(state=absent), only the O(command) is used to determine which Background Daemon should be removed.
    required: true
    type: str
  arguments:
    description:
      - Arguments to be passed to O(command).
      - Must be key value pairs.
      - The leading C(-) is prepended in front of the argument name/key (C(key) becomes C(-key)).
    required: false
    type: dict
'''

EXAMPLES = r'''
# The PowerShell equivalent is:
# Register-IcingaBackgroundDaemon `
#     -Command 'Start-MyCustomDaemon' `
#     -Arguments @{
#         '-MySwitchParameter'  = $True;
#         '-MyIntegerParameter' = 42;
#         '-MyStringParameter'  = 'Example';
#     };
- name: Register a Background Daemon for a specific command passing argument flags with values to that command
  netways.icinga.ifw_backgrounddaemon:
    state: present
    command: "Start-MyCustomDaemon"
    arguments:
      MySwitchParameter: true
      MyIntegerParameter: 42
      MyStringParameter: "Example"

- name: Register the Icinga for Windows RESTApi as a Background Daemon to use API Check Forwarder
  netways.icinga.ifw_backgrounddaemon:
    state: present
    command: "Start-IcingaWindowsRESTApi"
'''

RETURN = r'''
before:
  description:
    - Shows information about the previously (un-)registered command and its arguments.
    - If no change occurs, will be the same as RV(after).
  returned: success
  type: dict
  contains:
    command:
      description: The name of the previously (un-)registered command.
      returned: success
      type: str
      sample:
    arguments:
      description: The arguments used previously for the specified command.
      returned: success
      type: dict
      sample:
after:
  description:
    - Shows information about the newly (un-)registered command and its arguments.
    - If no change occurs, will be the same as RV(before).
  returned: success
  type: dict
  contains:
    command:
      description: The name of the newly (un-)registered command.
      returned: success
      type: str
      sample: Start-MyCustomDaemon
    arguments:
      description: The arguments now used for the specified command.
      returned: success
      type: dict
      sample:
        -MyIntegerParameter: 42
        -MyStringParameter: "Example"
        -MySwitchParameter: true
'''
