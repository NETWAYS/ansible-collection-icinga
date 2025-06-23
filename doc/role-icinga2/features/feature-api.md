## Feature API

The API Feature configures the API. The feature will manage
certificate, private key and CA certificate or will create
a certificate signing requests. It also manages the **zones.conf**.

All attributes of the object type [ApiListener](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#apilistener) can be added as keys.

All non Icinga attributes to configure the feature are explained below.

Example how to install an Agent:

```yaml
icinga2_features:
  - name: api
    force_newcert: false
    ca_host: icinga-server.localdomain
    endpoints:
      - name: NodeName
    zones:
      - name: ZoneName
        endpoints:
          - NodeName
```

Example how to install a master/server instance:

```yaml
icinga2_features:
  - name: api
    force_newcert: false
    ca_host: none
    endpoints:
      - name: NodeName
    zones:
      - name: ZoneName
        endpoints:
          - NodeName
```

### Instance with Certificate Authority

To create an instance with a local CA, the API Feature parameter `ca_host` should be `none`.

```yaml
ca_host: none
```

### Generate Certificate Signing Requests

Create Signing Request to get a certificate managed by the parameter `ca_host` and `ca_host_port`. If
set to the master/server hostname, FQDN or IP, the node setup tries to connect
via API an retrieve the trusted certificate.

> [!INFO]
> Ansible will delegate the ticket creation to the CA host. You can change this behaviour by setting 'icinga2_delegate_host' to match another Ansible alias.

```yaml
ca_host: icinga-server.localdomain
ca_host_port: 5665
```

> [!INFO]
> In case your agent can't connect to the CA host/master, you can change ca_host to your satellite.
> In addition you can use the variables `icinga2_delegate_host`
> and `ticket_salt` to delegate ticket creation to one of your satellites instead.
> But is will also work because the delegation task will be initiated by the Ansible controlhost.

Example if connection and ticket creation should be on the satellite:

```yaml
icinga2_features:
  - name: api
    ca_host: icinga-satellite.localdomain
    ticket_salt: "{{ icinga2_constants.ticket_salt }}"
  [...]
icinga2_delegate_host: icinga-satellite.localdomain
```
Example if agent should connect to satellite and the tickets are generated on the
master host.

```yaml
icinga2_features:
  - name: api
    ca_host: icinga-satellite.localdomain
    ticket_salt: "{{ icinga2_constants.ticket_salt }}"
  [...]
icinga2_delegate_host: icinga-master.localdomain
```

By default the FQDN is used as certificate common name, to put a name
yourself:

```yaml
cert_name: myown-commonname.fqdn
```

To force a new request set `force_newcert` to `true`:

```yaml
force_newcert: true
```

To increase your security set `ca_fingerprint` to validate the certificate of the `ca_host`:

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

### Use your own ready-made certificate

If you want to use certificates which aren't created by **Icinga 2 CA**, then use
the following variables to point the role to your own certificates.

```yaml
ssl_cacert: ca.crt
ssl_cert: certificate.crt
ssl_key: certificate.key
```

> **_NOTE:_** All three parameters have to be set otherwise a signing request is built
and `ca_host` must be defined.

The role will copy the files from your Ansible controller node to
**/var/lib/icinga2/certs** on the remote host. File names are
set to by the parameter `cert_name` (by default FQDN).

```yaml
icinga2_features:
  - name: api
    cert_name: host.example.org
    ssl_ca: /home/ansible/certs/ca.crt
    ssl_cert: /home/ansible/certs/host.crt
    ssl_key: /home/ansible/certs/host.key
    endpoints:
      - name: NodeName
    zones:
      - name: ZoneName
        endpoints:
          - NodeName
```

### Feature variables

* `ca_host: string`
  * Use to decide where to gather the certificates. When set to **None**, Ansible will create a local Certificate Authority on the Host. Use **hostname** or **ipaddress** as value.

* `force_newcert: boolean`
  * Force new certificates on the destination hosts.

* `cert_name: string`
  * Common name of Icinga client/server instance. Default is **ansible_fqdn**.

* `ssl_ca: string`
  * Path to the ca file when using manual certificates

* `ssl_cert: string`
  * Path to the certificate file when using manual certificates.

* `ssl_key: string`
  * Path to the certificate key file when using manual certificates.

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
