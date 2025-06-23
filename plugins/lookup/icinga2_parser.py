# (c) 2020, Icinga Team <www.icinga.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
from ansible_collections.netways.icinga.plugins.module_utils.parse import (
    Icinga2Parser,
)

DOCUMENTATION = '''
    author:
      - Lennart Betz (lennart.betz@netways.de)
      - Thilo Wening (thilo.wening@netways.de
    lookup: icinga2_parser
    version_added: "1.0"
    short_description: parse icinga2 attributes and custom attributes
    requirements:
      - hiera (command line utility)
    description:
        - Retrieves data from an Puppetmaster node using Hiera as ENC
    options:
      _hiera_key:
            description:
                - The list of keys to lookup on the Puppetmaster
            type: list
            element_type: string
            required: True
# FIXME: incomplete options .. _terms? environment/fqdn?
'''

EXAMPLES = """
# All this examples depends on hiera.yml that describes the hierarchy

- name: "a value from Hiera 'DB'"
  debug: msg={{ lookup('hiera', 'foo') }}
"""

RETURN = """
    _raw:
        description:
            - a parsed icinga2 config snippet
        type: strings
"""


class LookupModule(LookupBase):
    # TODO can the variables parameter be removed?
    def run(self, terms, variables=None, **kwargs):  # pylint: disable=unused-argument
        config = Icinga2Parser()
        ret = []
        constants = list(kwargs.get('constants', {}).keys())
        reserved = kwargs.get('reserved', [])
        indent = kwargs.get('indent', 2)

        ret.append(config.parse(terms[0], constants+reserved, indent))
        return ret
