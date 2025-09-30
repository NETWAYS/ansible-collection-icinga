DOCUMENTATION = '''
---
name: ifw_component
short_description: (Un-)Installs an IfW Component.
description:
  - This module allows you to install/uninstall an Icinga for Windows Component.
version_added: 0.1.0
author:
  - Matthias Döhler <matthias.doehler@netways.de>
seealso:
  - name: Icinga for Windows Components
    description: Reference for the Components.
    link: https://icinga.com/docs/icinga-for-windows/latest/doc/120-Repository-Manager/05-Install-Components/
options:
  state:
    description:
      - The state of the Component.
      - Decides whether the Component will be installed (or its version changed) or removed.
    required: false
    default: present
    choices: [ "present", "latest", "absent" ]
    type: str
  name:
    description:
      - A list of Component names that should be installed / removed.
      - If O(state=present), a Component will be installed if not already present.
      - If O(state=absent), a Component will be removed if present.
      - If O(state=latest), a Component will be installed if not already present with the latest version.
      - Each list entry can use the syntax of C(<NAME>:<VERSION>) to install Component C(<NAME>) in version C(<VERSION>). C(<NAME>:latest) will evaluate to the appropriate version for the given Component. C(<NAME>:) is the same as C(<NAME>:latest).
      - If O(state=present) or O(state=latest), the above syntax takes precedence. This means that specifying a version should always result in that specific version of the component being installed. Has no impact if O(state=absent).
    required: true
    type: list
    elements: str
    aliases:
      - "component"
'''

EXAMPLES = r'''
- name: Install the Component 'plugins' in version '1.11.1'
  netways.icinga.ifw_component:
    state: present
    name: "plugins:1.11.1"

- name: Install multiple Components while keeping installed Components in their current version
  netways.icinga.ifw_component:
    state: present
    name:
      - "plugins"
      - "agent"
      - "service"
      - "mssql"

- name: Install the latest version of Components 'plugins' and 'mssql' while keeping 'agent' in version '2.14.1'
  netways.icinga.ifw_component:
    state: latest
    name:
      - "plugins"
      - "mssql"
      - "agent:2.14.1"

- name: Remove Components 'mssql' and 'hyperv'
  netways.icinga.ifw_component:
    state: absent
    name:
      - "mssql"
      - "hyperv"
'''

RETURN = r'''
added:
  description:
    - Shows information about newly added or changed Components and the versions they now have.
  returned: success
  type: list
  elements: dict
  sample:
    - name: "plugins"
      version: "1.12.0"
    - name: "mssql"
      version: "1.5.0"
    - name: "agent"
      version: "2.14.1"
removed:
  description:
    - Shows information about removed Components and the versions they were installed with.
  returned: success
  type: list
  elements: dict
  sample:
    - name: "hyperv"
      version: "1.3.0"
    - name: "mssql"
      version: "1.5.0"
'''
