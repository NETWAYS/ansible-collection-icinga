## Module SSO

The Icinga SSO Web Module allows for logins via OIDC providers.

## Configuration

The general module parameter like `enabled` and `source` can be applied here.

For every config file, create a dictionary with sections as keys and the parameters as values. For all parameters please check the [module documentation](https://icinga.com/docs/icinga-sso/latest/doc/03-Configuration/).  
For the providers themselves, the `icingaweb2` role properly converts a given list to a dictionary for further processesing.
Be sure to provide a list of dictionaries, each defining one OIDC provider.

```yaml
icingaweb2_modules:
  sso:
    enabled: true
    source: package
    providers:
      - name: firstOIDCprovider
        base_url: "https://git.icinga.com/.well-known/openid-configuration"
        client_id: "deadbeefc0decafecafec0debeefdead"
        client_secret: "gloas-cafec0debeefdeaddeadbeefc0decafe"
        scopes: "openid profile offline_access groups"
        redirect_url: "https://example.com/sso/oidc/redirection-endpoint"
        username_claim: "preferred_username"
        map_groups: "y"
        groups_claim: "groups"
      - name: "secondOIDCprovider"
        ...
```
