## Feature API

The API feature configures the API. The feature will manage
certificate, private key and CA certificate or will create
a certificate signing requests. It also manages the **zones.conf**.

All attributes of the object type [ApiListener](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apilistener) can be added as keys.

All non Icinga attributes to configure the feature are explained below.

Example how to install an Agent:

> Replace `<PLACEHOLDERS>` according to your environment.

```yaml
icinga2_features:
  - name: api
    force_newcert: false
    parent_host: <ParentNodeFQDN/IPAddress>
    endpoints:
      - name: NodeName
      - name: <ParentNodeName>
        host: <ParentIPAddress>
    zones:
      - name: ZoneName
        parent: <ParentZoneName>
        endpoints:
          - NodeName
      - name: <ParentZoneName>
        endpoints:
          - <ParentNodeName>
```

Example how to install a master/server instance:

```yaml
icinga2_features:
  - name: api
    force_newcert: false
    parent_host: none
    endpoints:
      - name: NodeName
    zones:
      - name: ZoneName
        endpoints:
          - NodeName
```

### Instance with Certificate Authority

To create an instance with a local CA, the API feature parameter `parent_host` should be `none`.

```yaml
parent_host: none
```

### Agent Setup

An agent (or satellite) setup can work in four different ways.

In all cases of auto-signing the master instance must have a secret `TicketSalt` defined.

**On-demand signing:**  
The agent creates a CSR locally and then request signing via API.  
Manual signing on the master instance is necessary.  
For this, pass an empty ticket `ticket: ""`.  
The `netways.icinga.icinga2_api` module used here will report changes with each execution until the certificate is signed.

**Auto-signing with ticket:**  
The agent can pass a ticket which the master instance can validate.  
If the validation is successful, the agent receives its signed certificate.  
You can use the `netways.icinga.icinga2_ticket` filter to create a valid ticket if you know the secret `TicketSalt`.  
Example: `ticket: "{{ <common_name> | netways.icinga.icinga2_ticket(ticketsalt='<secret_ticket_salt>') }}"`

**Auto-signing without ticket:**  
Before the agent requests its certificate, the ticket is generated on the master instance.  
For this to work `parent_host` must be the master since ticket creation is delegated to `parent_host`.  
If the `parent_host` is not the master, `icinga2_delegate_host: <inventory_hostname of master>` can be set to delegate there instead.  

**Auto-signing with reverse connection:**  
Used in environments where the agent cannot connect to its parent but the parent can connect to the agent.  
Here delegation to `parent_host` (or `icinga2_delegate_host`) is used to retrieve the CA certificate and generate a ticket.  
This is used if `delegate_pki: true`.

### Generate Certificate Signing Requests

Create Signing Request to get a certificate managed by the parameter `parent_host` and `parent_port`. If
set to the master/server hostname, FQDN or IP, the node setup tries to connect
via API and retrieve the trusted certificate.

> [!INFO]
> Ansible will delegate the ticket creation to the `parent_host`. You can change this behaviour by setting 'icinga2_delegate_host' to match another Ansible alias.

```yaml
parent_host: icinga-server.localdomain
parent_port: 5665
```

Example if connection should be established to the satellite, resulting in on-demand certificate signing:

```yaml
icinga2_features:
  - name: api
    parent_host: icinga-satellite.localdomain
    ticket: ""
  [...]
```

> In the above case, the `parent_host` is a satellite which does not have the secret `TicketSalt`, so we cannot delegate there for ticket creation.

Example if agent should connect to satellite and the tickets are generated on the master host.

```yaml
icinga2_features:
  - name: api
    parent_host: icinga-satellite.localdomain
  [...]
icinga2_delegate_host: icinga-master.localdomain
```

By default the FQDN is used as certificate common name, to put a name yourself:

```yaml
cert_name: myown-commonname.fqdn
```

To force a new request set `force_newcert` to `true`:

```yaml
force_newcert: true
```

To increase your security set `ca_fingerprint` to validate the CA certificate:

```yaml
ca_fingerprint: "00 DE AD BE EF"
# alternatively
ca_fingerprint: "00:DE:AD:BE:EF"
# or lowercase
ca_fingerprint: "00 de ad be ef"
```

The fingerprint can be retrieved with OpenSSL:

```bash
openssl x509 -noout -fingerprint -sha256 -inform pem -in /path/to/ca.crt
```

### Top-down connections

Use `delegate_pki: true` when the agent cannot initiate a connection to the CA host / master, but the parent / master can connect inbound to the agent.

In this mode, the role:

- fetches `ca.crt` from the `parent_host` via Ansible and copies it to the agent
- generates a self-signed certificate on the agent
- creates a ticket on the `parent_host` via `delegate_to`
- writes the ticket to `{{ icinga2_cert_path }}/ticket`

Icinga then completes certificate signing automatically when the parent connects to the agent and the cluster handshake starts. This is not a fully offline / disconnected workflow.

```yaml
icinga2_features:
  - name: api
    parent_host: icinga-master.localdomain
    delegate_pki: true
    endpoints:
      - name: icinga-agent.localdomain
      - name: icinga-master.localdomain
        # no host here: agent cannot initiate connection anyway
    zones:
      - name: icinga-agent.localdomain
        endpoints:
          - icinga-agent.localdomain
        parent: master
      - name: master
        endpoints:
          - icinga-master.localdomain
### Use your own ready-made certificate

If you want to use certificates which aren't created by **Icinga 2 CA**, then use
the following variables to point the role to your own certificates.

```yaml
ssl_cacert: ca.crt
ssl_cert: certificate.crt
ssl_key: certificate.key
```

> **_NOTE:_** All three parameters have to be set otherwise a signing request is built
and `parent_host` must be defined.

The role will copy the files from your Ansible controller node to
**/var/lib/icinga2/certs** on the remote host. File names are
set to by the parameter `cert_name` (by default FQDN).

If the certificates and the key are already present on the remote host,
you can set `ssl_remote_source: true` to change the above behavior.

```yaml
icinga2_features:
  - name: api
    cert_name: host.example.org
    ssl_cacert: /home/ansible/certs/ca.crt
    ssl_cert: /home/ansible/certs/host.crt
    ssl_key: /home/ansible/certs/host.key
    ssl_remote_source: false
    endpoints:
      - name: NodeName
    zones:
      - name: ZoneName
        endpoints:
          - NodeName
```

### Feature variables

* `parent_host: string`
  * Use to decide where to gather the certificates. When set to **none**, Ansible will create a local Certificate Authority on the Host. Use **hostname** or **ipaddress** as value.

* `force_newcert: boolean`
  * Force new certificates on the destination hosts.

* `force_newca: boolean`
  * Force new CA on the destination hosts (master instance).

* `ticket: string`
  * A valid ticket for the given `cert_name`. Used for auto-signing the CSR. Can be generated using the `netways.icinga.icinga2_ticket` filter. If `ticket: ""`, on-demand signing is used.

* `delegate_pki: boolean`
  * Skip outbound `pki save-cert` and `pki request` on the agent. Provision `ca.crt` and ticket through Ansible delegation and rely on Icinga CSR auto-signing when the parent connects inbound.

* `cert_name: string`
  * Common name of Icinga client/server instance. Default is **ansible_facts['fqdn']**.

* `ca_fingerprint: string`
  * SHA256 fingerprint of the CA certificate. If defined, the fingerprint is validated.

* `ssl_cacert: string`
  * Path to the ca file when using manual certificates

* `ssl_cert: string`
  * Path to the certificate file when using manual certificates.

* `ssl_key: string`
  * Path to the certificate key file when using manual certificates.

* `ssl_remote_source: boolean`
  * Whether to copy the certificates and key from the remote host instead of from the Ansible controller.

* `endpoints: list of dicts`
  * Defines endpoints in **zones.conf**, each endpoint is required to have a name and optional a host or port.<br>
    * `name: string`
    * `host: string`
    * `port: number`

* `zones: list of dicts`
  * Defines zones in **zones.conf**, each zones is required to have a name and endpoints. The parameter global is optional.
    * `name: string`
    * `endpoints: list`
    * `global: boolean`
    * `parent: string`
