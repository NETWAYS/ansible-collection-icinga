# -*- coding: utf-8 -*-
# pylint: disable=consider-using-f-string,super-with-arguments,attribute-defined-outside-init,too-many-instance-attributes


from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth
from requests.exceptions import SSLError, RequestException
import requests

from ansible.plugins.inventory import BaseInventoryPlugin, Cacheable, Constructable, to_safe_group_name
from ansible.module_utils._text import to_bytes, to_text
from ansible.errors import AnsibleError
from ansible.parsing.yaml.objects import AnsibleSequence, AnsibleMapping

DOCUMENTATION = '''
    name: icinga
    short_description: Icinga 2 inventory source
    requirements:
        - requests >= 1.1
    description:
        - Get inventory hosts from Icinga 2.
        - Uses Icinga 2's API to get information about hosts.
        - The use of a custom filter is possible.
        - Uses a YAML configuration file that ends with ``icinga.(yml|yaml)``.
    extends_documentation_fragment:
        - constructed
        - inventory_cache
    options:
      plugin:
        description: Token that ensures this is a source file for the C(icinga) plugin.
        required: true
        choices: ['netways.icinga.icinga']
      url:
        description:
          - URL of the Icinga 2 server.
        default: 'https://localhost'
      port:
        description: The port number used for API calls against Icinga 2.
        type: int
        default: 5665
      user:
        description:
          - The name of the user who accesses the Icinga 2 API.
        required: true
      password:
        description:
          - The password of the user who accesses the Icinga 2 API.
        required: true
      validate_certs:
        description:
          - Whether to validate Icinga 2 API certificates.
        type: boolean
        default: true
      group_prefix:
        description:
          - Prefix to apply to Icinga 2 specific groups.
          - By default hosts are also grouped by their zones.
          - This prefix applies to both attributes, groups and zone.
          - Results in groups named like C(PREFIX(GROUP|ZONE)VALUE).
        type: string
        default: icinga_
      vars_prefix:
        description:
          - Prefix to apply to host variables.
          - Only affects Icinga 2 host specific attributes.
        type: string
        default: icinga_
      ansible_user_var:
        description:
          - The hosts' attribute to set as C(ansible_user).
        type: string
      want_ipv4:
        description:
          - Whether C(ansible_host) should be set to the host's C(address) attribute.
          - C(want_ipv4) takes precedence over C(want_ipv6).
        type: bool
        default: false
      want_ipv6:
        description:
          - Whether C(ansible_host) should be set to the host's C(address6) attribute.
          - C(want_ipv4) takes precedence over C(want_ipv6).
        type: bool
        default: false
      filters:
        suboptions:
          name:
            description:
              - Name(s) or pattern(s) to match specific hosts.
              - If any of these match a host, it will be included.
            type: list
            elements: string
          zone:
            description:
              - Restrict list of hosts to the requested zones.
            type: list
            elements: string
          custom:
            description:
              - Custom filter(s) that will be passed as is.
            type: list
            elements: string
          vars:
            description:
              - Restrict list of hosts based on custom variables.
            type: list
            elements: string
'''

EXAMPLES = '''
# inventory-icinga.yml
plugin: netways.icinga.icinga
url: https://icinga.example.com
user: ansibleinventory
password: changeme

# icinga.yaml
plugin: netways.icinga.icinga
url: https://icinga.example.com
user: ansibleinventory
password: changeme
validate_certs: false
filters:
  # Only get hosts with 'zone' attribute equal to 'main' or 'sat*'
  zone:
    - main
    - sat*
  # Only get hosts which are part of the group 'linux_hosts'
  group:
    - linux_hosts
  vars:
    is:
      # Only get hosts whose variable 'ansible_managed' is set to true
      ansible_managed: true
    in:
      # Only get hosts who have 'dns' or 'database' in their array variable 'services'
      services:
        - dns
        - database
# Set Ansible's variable 'ansible_user' equal to the host's variable 'ansible_user'
ansible_user_var: vars.ansible_user
# Create groups with name 'icinga_os' + '_{VALUE OF VARIABLE}' and add hosts accordingly
keyed_groups:
  - prefix: "icinga_os"
    key: vars.operating_system
'''



class InventoryModule(BaseInventoryPlugin, Cacheable, Constructable):
    # pylint: disable=too-many-ancestors
    NAME = 'icinga'

    def verify_file(self, path):
        ''' return true/false if this is possibly a valid file for this plugin to consume '''
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('icinga.yaml', 'icinga.yml')):
                valid = True
            else:
                self.display.vvv('Skipping due to inventory source not ending in "icinga.yaml" nor "icinga.yml"')
        return valid


    def _get_recursive_sub_element(self, d, key_string):
        delimiters     = [ '.', '[', ']' ]
        post_delimiter = '...'
        final_keys     = list()
        new_d          = d

        for delimiter in delimiters:
            key_string = key_string.replace(delimiter, post_delimiter)

        keys = key_string.split(post_delimiter)

        # Remove empty entries and cast numbers to integers
        for key in keys:
            if not key:
                continue
            if key.isdigit():
                key = int(key)
            else:
                key = key.strip('\'').strip('"')
            final_keys.append(key)

        # Recurse into structure
        for index, key in enumerate(final_keys):
            try:
                new_d = new_d[key]
            except IndexError:
                self.display.vvvv(f'Structure \'{d}\' has no index \'{index}\' for sub-structure \'{new_d}\'.')
                raise
            except (KeyError, TypeError):
                self.display.vvvv(f'Strucutre \'{d}\' has no key \'{key}\' for sub-structure \'{new_d}\'.')
                raise

        return new_d


    def _get_session(self):
        self.session         = requests.session()
        self.session.auth    = HTTPBasicAuth(to_bytes(self.icinga_user), to_bytes(self.icinga_password))
        self.session.headers = {
                                 'Accept': 'application/json',
                                 'X-HTTP-Method-Override': 'GET',
                               }
        self.session.verify  = self.validate_certs
        return self.session


    def _validate_filter(self):
        valid_filter    = True
        valid_keys      = [ 'name', 'group', 'zone', 'custom', 'vars' ]
        valid_vars_keys = [ 'match', 'in', 'is' ]
        invalid_keys    = list()

        if self.filters:
            # Check if each key is valid
            for key in self.filters.keys():
                if key not in valid_keys:
                    valid_filter = False
                    invalid_keys.append(key)

            # Check validity of each 'vars' key subkey
            if 'vars' in self.filters:
                for sub_key in self.filters['vars']:
                    if sub_key not in valid_vars_keys:
                        valid_filter = False
                        invalid_keys.append(f'vars.{sub_key}')

        else:
            valid_filter = False

        if invalid_keys:
            raise AnsibleError(f'The following keys are not valid for \'filters\': {invalid_keys}')

        return valid_filter


    def _create_filter_general(self, filter_string_base, key, values):
        # Creates a filter for multiple list entries for a given key
        # Handles logical concatenation and negation
        # For each key at least on entry in the list must match their hosts according attribute
        # The kind of filter ('match', 'in', 'is') is passed to this function

        # Create filters for positive matches logically combined by 'or', and negated matches logically combined by 'and'
        # Combine both with a logical 'and'
        # E.g.: name must match (A or B or C) AND must match (NOT D and NOT E)
        sub_filter          = list()
        sub_filter_positive = list()
        sub_filter_negative = list()

        for value in values:
            tmp_string = filter_string_base.format(value, key)
            if value.startswith('!'):
                tmp_string = '!{}'.format(tmp_string.replace('!', ''))
                sub_filter_negative.append(tmp_string)
            else:
                sub_filter_positive.append(tmp_string)

        if sub_filter_positive:
            sub_filter_positive_string = '({})'.format('||'.join(sub_filter_positive))
            sub_filter = sub_filter + [sub_filter_positive_string]
        if sub_filter_negative:
            sub_filter_negative_string = '({})'.format('&&'.join(sub_filter_negative))
            sub_filter = sub_filter + [sub_filter_negative_string]

        sub_filter_string = '&&'.join(sub_filter)

        return sub_filter_string


    def _create_is_filter(self, key, values):
        true_filter_string          = '(host.{}==true)'
        false_filter_string         = '(host.{}==false)'
        null_filter_string          = '(host.{}==null)'
        set_or_true_filter_string   = '(host.{})'

        values = [value.lower() for value in values]
        # Only allow one value passed to a key of the 'is' filter
        if len(values) > 1:
            self.display.vvv(f'Multiple values provided to a key of the \'is\' filter. Only using first value \'{values[0]}\'.')
        value = values[0]

        if value == 'true':
            filter_string = true_filter_string.format(key)
        elif value == 'false':
            filter_string = false_filter_string.format(key)
        elif value == 'set':
            filter_string = set_or_true_filter_string.format(key)
        elif value == '!set':
            filter_string = '!' + set_or_true_filter_string.format(key)
        # 'null' results in 'none' if passed wihtout string enclosure
        elif value in [ 'none', 'null' ]:
            filter_string = null_filter_string.format(key)
        elif value in [ '!none', '!null' ]:
            filter_string = '!' + null_filter_string.format(key)
        else:
            # Only allow 'true', 'false', 'set', '!set', 'null' and '!null'
            self.display.vvv('Valid values for the \'is\' filter are: \'true\', \'false\', \'set\', \'!set\', \'null\' and \'!null\'.')
            raise ValueError(f'\'{value}\' is not valid value for the \'is\' filter')

        return filter_string


    def _create_in_filter(self, key, values):
        filter_string_base = '(\\"{}\\" in host.{})'
        sub_filter_string  = self._create_filter_general(filter_string_base, key, values)
        return sub_filter_string


    def _create_match_filter(self, key, values):
        filter_string_base = 'match(\\"{}\\", host.{})'
        sub_filter_string  = self._create_filter_general(filter_string_base, key, values)
        return sub_filter_string


    def _create_filter(self):
        filter_string = ''
        sub_filters   = list()

        # Validate filter. Return empty filter if not valid.
        if not self._validate_filter():
            return filter_string

        for key, value in self.filters.items():
            # Skip / ignore if an empty key has been passed
            if not value:
                self.display.vvv(f'Ignoring empty key \'{key}\'.')
                continue

            # Make sure every key within filters is considered a list, cast string to single entry list
            if isinstance(value, (AnsibleMapping, dict)):
                value = dict(value)
            elif isinstance(value, (AnsibleSequence, list)):
                value = [to_text(val) for val in value]
            else:
                value = [to_text(value)]

            # Special treatment for custom filter
            if key == 'custom':
                for entry in value:
                    sub_filters.append(entry)
                sub_filter_string = '({})'.format(')&&('.join(value))

            # Special treatment for groups
            # Overwrite the filter_string
            elif key == 'group':
                sub_filter_string = self._create_in_filter('groups', value)

            # Special treatment for custom vars
            elif key == 'vars':
                local_filter_list = list()
                for sub_key, attributes in value.items():
                    for attribute_key, attribute_values in attributes.items():
                        # Skip / ignore if an empty key has been passed
                        if not attribute_values and sub_key != 'is':
                            self.display.vvv(f'Ignoring empty key \'vars.{attribute_key}\'.')
                            continue

                        # Make sure 'attribute_values' is considered a list, cast string to single entry list
                        if isinstance(attribute_values, (AnsibleSequence, list)):
                            attribute_values = [to_text(val) for val in attribute_values]
                        else:
                            attribute_values = [to_text(attribute_values)]

                        # Choose correct filter
                        tmp_string = ''
                        if sub_key == 'match':
                            tmp_string = self._create_match_filter(f'vars.{attribute_key}', attribute_values)
                        elif sub_key == 'in':
                            tmp_string = self._create_in_filter(f'vars.{attribute_key}', attribute_values)
                        elif sub_key == 'is':
                            tmp_string = self._create_is_filter(f'vars.{attribute_key}', attribute_values)

                        local_filter_list.append(tmp_string)

                sub_filter_string = '&&'.join(local_filter_list)

            # Anything else will use the 'match' filter
            else:
                sub_filter_string = self._create_match_filter(key, value)

            sub_filters.append(sub_filter_string)

        if sub_filters:
            filter_string = '({})'.format(')&&('.join(sub_filters))

        return filter_string


    def _get_hosts(self):
        s = self._get_session()

        # Validate connection via API URL
        try:
            s.get(self.api_url)
        except SSLError:
            self.display.vvv('SSL Error: You may want to trust the certificate or pass \'validate_certs: false\'')
            raise
        except RequestException:
            self.display.vvv('Error accessing \'{self.api_url}\'.')
            raise

        # Create filter
        filter_string = self._create_filter()
        data = None
        if filter_string:
            data = '{ "filter": "' + filter_string + '" }'

        self.display.vvv(f'Using filter: \'{data}\'')

        response = s.post(self.api_url + '/objects/hosts', data=data)

        if response.status_code != 200:
            raise ValueError(f'Something went wrong. HTTP status code: \'{response.status_code}\'. Icinga 2\'s API most likely did not understand the filter!')

        hosts = response.json()['results']
        return hosts


    def _populate_inventory(self, hosts):
        # Always add keyed groups for attribute 'zone'
        zone_wanted = True
        for keyed_group in self.keyed_groups:
            if 'key' in keyed_group and keyed_group['key'] == 'zone':
                zone_wanted = False
                break

        if zone_wanted:
            zone_key = {'prefix': self.group_prefix + 'zone', 'key': 'zone'}
            self.keyed_groups.append(zone_key)

        for host in hosts:
            host_name = host['name']
            host_vars = host['attrs']

            # Add groups and make current host a member based on its 'groups' attribute
            for group in host_vars['groups']:
                group_name = to_safe_group_name(self.group_prefix + 'group_' + group)
                self.inventory.add_group(group_name)
                self.inventory.add_host(host_name, group_name)

            # Add host to group 'ungrouped' if it does not belong to a group
            if not host_vars['groups']:
                self.inventory.add_host(host_name, )

            # Set attributes as host variables
            for key, value in host_vars.items():
                self.inventory.set_variable(host_name, f'{self.vars_prefix}{key}', value)

            # Set 'ansible_host' to IP address if requested
            if self.want_ipv4 and host_vars['address']:
                self.inventory.set_variable(host_name, 'ansible_host', host_vars['address'])
                self.display.vvv(f'Set attribute \'address\' as \'ansible_host\' for host \'{host_name}\'.')
            elif self.want_ipv6 and host_vars['address6']:
                self.inventory.set_variable(host_name, 'ansible_host', host_vars['address6'])
                self.display.vvv(f'Set attribute \'address6\' as \'ansible_host\' for host \'{host_name}\'.')

            # Set 'ansible_user' if requested and defined on the Icinga 2 host
            if self.ansible_user:
                ansible_user_value = None
                try:
                    ansible_user_value = self._get_recursive_sub_element(host_vars, self.ansible_user)
                except (IndexError, KeyError, TypeError):
                    self.display.vvv(f'Could not set \'{self.ansible_user}\' as \'ansible_user\' for host \'{host_name}\'.')

                # Set 'ansible_user'
                if ansible_user_value:
                    self.inventory.set_variable(host_name, 'ansible_user', ansible_user_value)

            # Add composite vars
            self._set_composite_vars(self.compose, host_vars, host_name, strict=self.strict)

            # Add composed groups
            self._add_host_to_composed_groups(self.groups, host_vars, host_name, strict=self.strict)

            # Add keyed_groups
            self._add_host_to_keyed_groups(self.keyed_groups, host_vars, host_name, strict=self.strict)


    def _validate_url(self, url):
        valid = False

        try:
            parsed_url = urlparse(url)
            if parsed_url.scheme and parsed_url.netloc and parsed_url.path == '/v1':
                valid = True
        except ValueError:
            pass

        return valid


    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # Read config options from file for futher use
        self._read_config_data(path)

        # Set attributes based on parsed file
        self.icinga_url      = self.get_option('url')
        self.icinga_port     = self.get_option('port')
        self.icinga_user     = self.get_option('user')
        self.icinga_password = self.get_option('password')
        self.validate_certs  = self.get_option('validate_certs')
        self.filters         = self.get_option('filters')
        self.group_prefix    = self.get_option('group_prefix')
        self.vars_prefix     = self.get_option('vars_prefix')
        self.want_ipv4       = self.get_option('want_ipv4')
        self.want_ipv6       = self.get_option('want_ipv6')
        self.ansible_user    = self.get_option('ansible_user_var')

        # Related to Ansible's Constructable
        self.compose         = self.get_option('compose')
        self.groups          = self.get_option('groups')
        self.keyed_groups    = self.get_option('keyed_groups')
        self.strict          = self.get_option('strict')

        # Jinja2 templating for url, user and password
        if self.templar.is_template(self.icinga_url):
            self.icinga_url = self.templar.template(variable=self.icinga_url)
        if self.templar.is_template(self.icinga_user):
            self.icinga_user = self.templar.template(variable=self.icinga_user)
        if self.templar.is_template(self.icinga_password):
            self.icinga_password = self.templar.template(variable=self.icinga_password)

        # Build API URL and validate
        self.icinga_url      = self.icinga_url.rstrip('/')
        self.api_url         = f'{self.icinga_url}:{self.icinga_port}/v1'
        if not self._validate_url(self.api_url):
            raise ValueError(f'\'{self.api_url}\' is not a valid URL.')

        # Check if cache is available and should be used
        cache_key            = self.get_cache_key(path)
        use_cache            = self.get_option("cache") and cache
        update_cache         = self.get_option("cache") and not cache

        hosts = None

        # Get hosts from cache if available and recent
        if use_cache:
            try:
                hosts = self._cache[cache_key]
                self.display.vvv('Using existing cache.')
            except KeyError:
                self.display.vvv('Creating/updating cache.')
                update_cache = True

        if not hosts:
            # Get hosts from Icinga 2's API
            hosts = self._get_hosts()

        if update_cache:
            self._cache[cache_key] = hosts

        self._populate_inventory(hosts)
