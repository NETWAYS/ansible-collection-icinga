from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
module: icinga2_api
short_description: Handles Icinga 2 API setup.
description:
  - Sets host up for communication with other Icinga 2 nodes.
  - Initiates an Icinga 2 master / satellite / agent setup.
  - Ensures correct C(NodeName) constant.
  - Manages C(zones.conf).
  - Does not manage the C(ApiListener) object / C(api) feature.
version_added: WIP
author: |
  Matthias Döhler <matthias.doehler@netways.de>
options:
  mode:
    description:
      - Defines the configuration mode to run.
      - O(mode=master) will set the host up as a master instance.
        This will create a local CA and the certificate for the host itself.
      - O(mode=agent) (and its alias O(mode=satellite)) will set the host up as an agent instance.
        This will create a certificate and key for the host,
        fetch the parent's certificate,
        and make a certificate request to that parent.
      - The configuration steps, like setting the C(NodeName), always happen.
         If O(mode=config) the master / agent setup is skipped, saving a little time if already done previously.
    type: str
    default: agent
    choices:
      - agent
      - satellite
      - master
      - config
  cn:
    description:
      - Defines the common name (CN) of the host.
        This name will be used to distinctly represent this host within the cluster.
        The O(cn) will be written to C(constants.conf) and used in this host's certificate.
      - If unspecified, the host's FQDN will be used as given by V(socket.getfqdn(\)).
    type: str
  host:
    description:
      - If O(mode=agent), V(host) will be used to fetch the parent's certificate and for certificate requests.
        Used in combination with O(port).
      - Required when O(mode=agent).
    type: str
    aliases:
      - parent_host
  port:
    description:
      - If O(mode=agent), V(port) will be used to fetch the parent's certificate and for certificate requests.
        Used in combination with O(host).
    default: 5665
    type: int
    aliases:
      - parent_port
  ticket:
    description:
      - Used for CSR auto signing. If unspecified, a request is made to the O(parent) without a valid ticket, leading to on-demand CSR signing.
        With each execution of this module, new requests will be made until the host's CSR has been signed.
      - |
        The ticket for any C(CN) can be computed using the C(TicketSalt) secret found on the Icinga 2 master,
        passing both values to P(netways.icinga.icinga2_ticket#filter).
        Example: V(ticket: "{{ 'myCommonName' | netways.icinga.icinga2_ticket(ticketsalt='mySuperSecretTicketSalt'\) }}")
    type: str
  enable_feature:
    description:
      - Whether the C(api) feature should be enabled.
      - This does not configure the C(ApiListener) object found in the C(api) feature, but merely enables it.
        If you need to configure the feature, you can use P(netways.icinga.icinga2#role) to do so
        or use other modules like M(ansible.builtin.template) to generate a configuration according to your needs.
    default: true
    type: bool
  zones:
    description:
      - Defines C(zones.conf).
        If left empty, C(zones.conf) will stay untouched.
    default: []
    type: list
    elements: dict
    suboptions:
      name:
        description:
          - Defines the name of the zone.
        type: str
      global:
        description:
          - Whether the zone is a global zone.
        default: false
        type: bool
        aliases:
          - _global
      parent:
        description:
          - Defines the parent zone of O(zones[].name).
        type: str
      endpoints:
        description:
          - Defines the Icinga 2 endpoint objects.
        type: list
        elements: dict
        suboptions:
          cn:
            description:
              - Defines the endpoint object's name.
            type: str
            aliases:
              - name
          host:
            description:
              - Defines the endpoint object's C(host) attribute.
            type: str
          port:
            description:
              - Defines the endpoint object's C(port) attribute.
            type: int
  force_new_ca:
    description:
      - If O(mode=master) and O(force_new_ca=true), enforces the recreation of the CA certificate and key.
    default: false
    type: bool
  force_new_cert:
    description:
      - If O(mode=master) or O(mode=agent), and O(force_new_cert=true), enforces the recreation of the host's certificate and key.
    default: false
    type: bool
  fingerprint:
    description:
      - The fingerprint of the CA's certificate. This is used for validation.
    type: str
  ignore_fingerprint:
    description:
      - If O(ignore_fingerprint=true), no validation using the O(fingerprint) takes place.
    default: false
    type: bool

requirements:
    - icinga2

seealso:
    - name: Icinga 2 distributed monitoring
      description: Official documentation about distributed monitoring with Icinga 2.
      link: https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
'''

EXAMPLES = r'''
- name: Agent setup using on-demand signing
  netways.icinga.icinga2_api:
    mode: agent
    cn: "agent.example.com"
    host: "master.example.com"
    fingerprint: "fb7ebd67bb1b69eba4edec1204683b636d17b7393dad84f8c8ee66c5a1ad84ba"
    zones:
      # Define parent zone and connection details
      - name: "master"
        endpoints:
          - cn: "master.example.com"
            host: "10.0.0.30"
      # Define own zone
      - name: "agent.example.com"
        parent: "master"
        endpoints:
          - cn: "agent.example.com"


- name: Satellite setup using a ticket
  netways.icinga.icinga2_api:
    mode: agent
    cn: "satellite.example.com"
    host: "master.example.com"
    ticket: "{{ 'satellite.example.com' | netways.icinga.icinga2_ticket(ticketsalt='mySecretTicketSalt') }}"
    fingerprint: "fb7ebd67bb1b69eba4edec1204683b636d17b7393dad84f8c8ee66c5a1ad84ba"
    zones:
      # Define parent zone and connection details
      - name: "master"
        endpoints:
          - cn: "master.example.com"
            host: "10.0.0.30"
      # Define own satellite zone called 'satellite'
      - name: "satellite"
        parent: "master"
        endpoints:
          - cn: "satellite.example.com"
      # Global zones as needed
      - name: "global-templates"
        global: true
      - name: "director-global"
        global: true


- name: Master setup defining multiple satellite zones and global zones
  netways.icinga.icinga2_api:
    mode: master
    cn: "master.example.com"
    zones:
      # Define master zone
      - name: "master"
        endpoints:
          - cn: "master.example.com"
      # Define first satellite zone called 'us'
      - name: "us"
        parent: "master"
        endpoints:
          - cn: "us-satellite.example.com"
            host: "us-satellite.example.com"
      # Define second satellite zone called 'de'
      - name: "de"
        parent: "master"
        endpoints:
          - cn: "de-satellite.example.com"
            host: "de-satellite.example.com"
      # Global zones
      - name: "global-templates"
        global: true
      - name: "director-global"
        global: true
'''

RETURN = r'''
cn:
  description:
    - The common name used.
  type: str
  returned: always
  sample: example.com
ca_fingerprint:
  description:
    - The sha256 fingerprint of the C(ca.crt).
  type: str
  returned: always
  sample: fb7ebd67bb1b69eba4edec1204683b636d17b7393dad84f8c8ee66c5a1ad84ba
cert_fingerprint:
  description:
    - The sha256 fingerprint of this host's certificate.
  type: str
  returned: always
  sample: 53f33316caacd4342a12c130e5fa6d7a619565bd730ac58ef98f8b38a7e03e37
'''

import filecmp
import shutil
import socket
import glob
import os
import re


def verify_cert(module, ca_path, cert_path):
    cmd = [
        'icinga2',
        'pki',
        'verify',
        '--cacert', ca_path,
        '--cert', cert_path,
    ]
    rc, stdout, stderr = module.run_command(
        cmd,
        executable=None,
        use_unsafe_shell=False,
        encoding=None,
        data=None,
        binary_data=True,
        expand_user_and_vars=True,
    )
    if rc != 0:
        return False
    return True


def get_fingerprint(module, path):
    fingerprint_pattern = r'Fingerprint:\s*(.*)$'
    if os.path.isfile(path):
        cmd = [
            'icinga2',
            'pki',
            'verify',
            '--cert', path,
        ]
        rc, stdout, stderr = module.run_command(
            cmd,
            executable=None,
            use_unsafe_shell=False,
            encoding=None,
            data=None,
            binary_data=True,
            expand_user_and_vars=True,
        )
        match = re.search(fingerprint_pattern, str(stdout).strip('"'))
        if match:
            # Normalize fingerprint
            fingerprint = match.group(1).replace('\\n', '').replace(' ', '').lower()
            return fingerprint
        return None


def get_return_values(module, cn, ca_directory, certs_directory):
    ### Get CA and certificate fingerprints
    rv = dict(
        cn = cn,
        ca_fingerprint = None,
        cert_fingerprint = None,
    )
    rv['ca_fingerprint'] = get_fingerprint(module, os.path.join(certs_directory, 'ca.crt'))
    rv['cert_fingerprint'] = get_fingerprint(module, os.path.join(certs_directory, cn + '.crt'))
    return rv


def configure(module, cn, zones, enable_feature, sysconf_directory):
    ret = dict(
        changed = False,
    )

    ### Ensure const NodeName is set to given CN
    with open(os.path.join(sysconf_directory, 'constants.conf'), 'r') as constants:
        lines = constants.readlines()

    new_lines = list()
    pattern = '^const NodeName.*$'
    target = 'const NodeName = "{}"'.format(cn)

    for line in lines:
        if re.search(pattern, line):
            if line.rstrip('\n') != target:
                new_lines.append(target + '\n')
                ret['changed'] = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)


    if not any(re.search(pattern, line) for line in lines):
        new_lines.append(target + '\n')
        changed = True

    with open(os.path.join(sysconf_directory, 'constants.conf'), 'w') as constants:
        constants.writelines(new_lines)


    ### Define zones.conf
    zones_conf = list()

    # Don't change zones.conf if not asked
    if not zones:
        return ret

    for zone in zones:
        # Validate zone is either global or contains endpoints
        if zone['_global'] and zone['endpoints']:
            ret['fail_msg'] = 'Zone \'{}\' cannot be global and contain endpoints.'.format(zone['name'])
            break

        if zone['_global']:
            zones_conf.append('object Zone "{}" {{'.format(zone['name']))
            zones_conf.append('  global = true')
            zones_conf.append('}')
            zones_conf.append('')
        else:
            # Add endpoints
            for endpoint in zone['endpoints']:
                zones_conf.append('object Endpoint "{}" {{'.format(endpoint['cn']))
                if endpoint['host']:
                    zones_conf.append('  host = "{}"'.format(endpoint['host']))
                if endpoint['port']:
                    zones_conf.append('  port = "{}"'.format(endpoint['port']))
                zones_conf.append('}')
                zones_conf.append('')

            # Add zone
            zones_conf.append('object Zone "{}" {{'.format(zone['name']))
            zones_conf.append('  endpoints = [')
            for endpoint in zone['endpoints']:
                zones_conf.append('    "{}",'.format(endpoint['cn']))
            zones_conf.append('  ]')
            if zone['parent']:
                zones_conf.append('  parent = "{}"'.format(zone['parent']))
            zones_conf.append('}')
            zones_conf.append('')
    new_zones = '\n'.join(zones_conf)

    current_zones = ""
    if os.path.isfile(os.path.join(sysconf_directory, 'zones.conf')):
        with open(os.path.join(sysconf_directory, 'zones.conf'), 'r') as zones_file:
            current_zones = zones_file.read()

    if new_zones != current_zones:
        with open(os.path.join(sysconf_directory, 'zones.conf'), 'w') as zones_file:
            zones_file.write(new_zones)
            ret['changed'] = True

    # Enable feature
    if enable_feature:
        cmd = [
            'icinga2',
            'feature',
            'enable',
            'api',
        ]
        rc, stdout, stderr = module.run_command(
            cmd,
            executable=None,
            use_unsafe_shell=False,
            encoding=None,
            data=None,
            binary_data=True,
            expand_user_and_vars=True,
        )
        if 'Enabling feature api.' in stdout.decode():
            ret['changed'] = True
        elif rc != 0:
            ret['fail_msg'] = stdout.decode().strip()

    return ret


def master_setup(module, cn, ca_directory, certs_directory, force_new_ca=False):
    ret = dict(
        changed = False,
    )

    ### Generate CA
    cmd = [
        'icinga2',
        'pki',
        'new-ca',
    ]

    if force_new_ca:
        os.remove(os.path.join(ca_directory, 'ca.key'))
        os.remove(os.path.join(ca_directory, 'ca.crt'))
        os.remove(os.path.join(certs_directory, 'ca.crt'))

    if not glob.glob(os.path.join(ca_directory, 'ca.key')):
        rc, stdout, stderr = module.run_command(
            cmd,
            executable=None,
            use_unsafe_shell=False,
            encoding=None,
            data=None,
            binary_data=True,
            expand_user_and_vars=True,
        )
        if 'information/base: Writing private key to \'{}\''.format(os.path.join(ca_directory, 'ca.key')) in str(stdout):
            ret['changed'] = True
        elif 'critical/cli: Please re-run this command as a privileged user' in str(stdout):
            ret['fail_msg'] = 'This module has to be run as a privileged user or as the \'nagios\' user.'
    elif not glob.glob(os.path.join(ca_directory, 'ca.crt')):
        module.warn(
            '{} is already present while {} is missing. Not generating a new CA.'.format(
                os.path.join(ca_directory, 'ca.key'),
                os.path.join(ca_directory, 'ca.crt')
            )
        )

    # Ensure '/var/lib/icinga2/certs/ca.crt' is up to date since this will be returned upon an agent's request (pki request)
    if not glob.glob(os.path.join(certs_directory, 'ca.crt')) or not filecmp.cmp(os.path.join(ca_directory, 'ca.crt'), os.path.join(certs_directory, 'ca.crt')):
        shutil.copy(
            os.path.join(ca_directory, 'ca.crt'),
            os.path.join(certs_directory, 'ca.crt')
        )

    # Sign own CSR
    if not verify_cert(module, os.path.join(ca_directory, 'ca.crt'), os.path.join(certs_directory, cn + '.crt')):
        cmd = [
            'icinga2',
            'pki',
            'sign-csr',
            '--csr', os.path.join(certs_directory, cn + '.csr'),
            '--cert', os.path.join(certs_directory, cn + '.crt'),
        ]
        rc, stdout, stderr = module.run_command(
            cmd,
            executable=None,
            use_unsafe_shell=False,
            encoding=None,
            data=None,
            binary_data=True,
            expand_user_and_vars=True,
        )
        ret['changed'] = True

    return ret


def agent_setup(module, cn, host, port, ticket, fingerprint, ignore_fingerprint, certs_directory, force_new_cert=False):
    ret = dict(
        changed = False,
    )

    ### Get parent certificate
    cmd = [
        'icinga2',
        'pki',
        'save-cert',
        '--host', host,
        '--port', str(port),
        '--trustedcert', os.path.join(certs_directory, 'trusted-parent.crt'),
    ]
    if force_new_cert or not glob.glob(os.path.join(certs_directory, 'trusted-parent.crt')):
        rc, stdout, stderr= module.run_command(
            cmd,
            executable=None,
            use_unsafe_shell=False,
            encoding=None,
            data=None,
            binary_data=True,
            expand_user_and_vars=True,
        )
        if 'Failed to fetch certificate from host.' in str(stdout):
            ret['fail_msg'] = stdout.decode().strip()
            return ret
        ret['changed'] = True


    ### Talk to master
    # This one also makes the node receive the new certificate once it's signed

    # Potential answers
    # information/cli: Writing CA certificate to file '/var/lib/icinga2/certs/ca.crt'.
    # information/cli: Writing signed certificate to file '/var/lib/icinga2/certs/<node_name>.crt'.
    #   → RC X
    #   → First connection after certificate is signed
    #
    # Could not fetch valid response. Please check the master log.
    #   → RC X 
    #   → If parent is available but does not know the own node's endpoint
    #
    # The certificates for CN '<node_name>' and its root CA are valid and uptodate. Skipping automated renewal.
    #   → RC 1
    #   → Connected normally, after getting valid certificate

    cmd = [
        'icinga2',
        'pki',
        'request',
        '--host', host,
        '--port', str(port),
        '--trustedcert', os.path.join(certs_directory, 'trusted-parent.crt'),
        '--ca', os.path.join(certs_directory, 'ca.crt'),
        '--key', os.path.join(certs_directory, cn + '.key'),
        '--cert', os.path.join(certs_directory, cn + '.crt'),
    ]
    if ticket:
        cmd.extend(['--ticket', ticket])

    # Make new request only if own cert not valid
    if not verify_cert(module, os.path.join(certs_directory, 'ca.crt'), os.path.join(certs_directory, cn + '.crt')):
        rc, stdout, stderr = module.run_command(
            cmd,
            executable=None,
            use_unsafe_shell=False,
            encoding=None,
            data=None,
            binary_data=True,
            expand_user_and_vars=True,
        )
        ret['changed'] = True

    # WIP: Trusted parent cert could be wrong at this point because parent might have forcefully created a new cert
    # critical/cli: Peer certificate does not match trusted certificate.

    # Validate fingerprint
    present_fingerprint = get_fingerprint(module, os.path.join(certs_directory, 'ca.crt'))
    if not ignore_fingerprint and fingerprint != present_fingerprint:
        ret['fail_msg'] = 'CA fingerprint \'{}\' on host did not match provided fingerprint \'{}\'.'.format(
            present_fingerprint,
            fingerprint,
        )

    return ret


def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            mode=dict(default='agent', choices=['agent', 'satellite', 'master', 'config'], type='str'),
            cn=dict(type='str'),
            host=dict(default=None, type='str', aliases=['parent_host']),
            port=dict(default=5665, type='int', aliases=['parent_port']),
            ticket=dict(default=None, type='str', no_log=True),
            enable_feature=dict(default=True, type='bool'),
            zones=dict(
                default=list(),
                type='list',
                elements='dict',
                options=dict(
                    name=dict(required=True, type='str'),
                    _global=dict(default=False, type='bool', aliases=['global']),
                    parent=dict(default=None, type='str'),
                    endpoints=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            cn=dict(required=True, type='str', aliases=['name']),
                            host=dict(default=None, type='str'),
                            port=dict(default=None, type='int'),
                        ),
                    ),
                ),
                required_if=[
                    ['global', False, ['endpoints'], False],
                    ['_global', False, ['endpoints'], False],
                ],
            ),
            force_new_ca=dict(default=False, type='bool'),
            force_new_cert=dict(default=False, type='bool'),
            fingerprint=dict(type='str'),
            ignore_fingerprint=dict(default=False, type='bool'),
        ),
        required_if=[
            ['mode', 'agent', ['host'], False],
            ['mode', 'satellite', ['host'], False],
        ]
    )

    sysconf_directory = '/etc/icinga2'
    data_directory    = '/var/lib/icinga2'
    ca_directory      = os.path.join(data_directory, 'ca')
    certs_directory   = os.path.join(data_directory, 'certs')

    cn             = module.params['cn']
    mode           = module.params['mode']
    zones          = module.params['zones']
    force_new_ca   = module.params['force_new_ca']
    force_new_cert = module.params['force_new_cert']
    enable_feature = module.params['enable_feature']

    if not cn:
        cn = socket.getfqdn()

    if mode == 'agent':
        host               = module.params['host']
        port               = module.params['port']
        ticket             = module.params['ticket']
        fingerprint        = module.params['fingerprint']
        ignore_fingerprint = module.params['ignore_fingerprint']

    ret = dict(
        changed = False,
    )

    ### Create certs/ if not present
    if os.path.isdir(data_directory) and not os.path.isdir(os.path.join(certs_directory)):
        stat_info = os.stat(data_directory)
        uid = stat_info.st_uid
        gid = stat_info.st_gid
        os.mkdir(certs_directory)
        os.chown(certs_directory, uid, gid)
        os.chmod(certs_directory, 0o700)
        ret['changed'] = True

    ### Create private key and certificate
    if force_new_cert or any(not os.path.isfile(os.path.join(certs_directory, file)) for file in [cn + '.key', cn + '.crt', cn + '.csr']):
        cmd = [
            'icinga2',
            'pki',
            'new-cert',
            '--cn', cn,
            '--key', os.path.join(certs_directory, cn + '.key'),
            '--cert', os.path.join(certs_directory, cn + '.crt'),
            '--csr', os.path.join(certs_directory, cn + '.csr'),
        ]
        rc, stdout, stderr = module.run_command(
            cmd,
            executable=None,
            use_unsafe_shell=False,
            encoding=None,
            data=None,
            binary_data=True,
            expand_user_and_vars=True,
        )
        ret['changed'] = True

    # Return values for the given mode + config
    mode_ret = dict()
    config_ret = dict()

    if mode == 'agent':
        mode_ret = agent_setup(module, cn, host, port, ticket, fingerprint, ignore_fingerprint, certs_directory, force_new_cert)
    elif mode == 'master':
        mode_ret = master_setup(module, cn, ca_directory, certs_directory, force_new_ca)

    config_ret = configure(module, cn, zones, enable_feature, sysconf_directory)
    module.warn("config ret " + str(config_ret))

    ### Collect information for return values
    ret.update(get_return_values(module, cn, ca_directory, certs_directory))

    # this one actually creates / pulls ca.crt
    #icinga2 pki request --host 192.168.122.113 --port 5665 --trustedcert /var/lib/icinga2/certs/trusted-parent.crt --ca /var/lib/icinga2/certs/ca.crt --key /var/lib/icinga2/certs/ansible-ubuntu24.key --cert /var/lib/icinga2/certs/ansible-ubuntu24.crt


    # Verify / test
    # While 
    # icinga2 pki verify --cert /var/lib/icinga2/certs/ansible-ubuntu24.crt  --cacert /var/lib/icinga2/certs/ca.crt → RC 2
    # still pending

    # Potential answers
    # critical/cli: CRITICAL: Certificate with CN 'ansible-ubuntu24' is NOT signed by CA: self-signed certificate (code 18)
    #   → RC 2
    #   → Error until certificate is signed
    #

    # Check if either setup or configuration had changes
    module.warn("mode" + str(mode_ret))
    module.warn("config" + str(config_ret))
    if any(r['changed'] for r in (mode_ret, config_ret) if 'changed' in r):
        ret['changed'] = True

    # Check if either setup or configuration had failures
    if 'fail_msg' in mode_ret:
        module.fail_json(
            **ret,
            msg=mode_ret['fail_msg']
        )
    elif 'fail_msg' in config_ret:
        module.fail_json(
            **ret,
            msg=config_ret['fail_msg']
        )

    module.exit_json(
        **ret,
    )


if __name__ == '__main__':
    main()
