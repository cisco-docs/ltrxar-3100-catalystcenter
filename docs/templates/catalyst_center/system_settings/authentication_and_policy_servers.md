# Authentication and Policy Servers

*Location in GUI*:
`System` » `Settings` » `External Services` » `Authentication and Policy Servers`

{{ doc_gen }}

Authentication and Policy Servers define the global ISE and AAA server integrations at the system level, including RADIUS/TACACS+ protocol settings, pxGrid connectivity, and trust/certificate configuration. These are distinct from the site-level [AAA Server settings](/docs/data_models/catalyst_center/network_settings/aaa_servers) which assign servers to specific sites. Applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic ISE server configuration with RADIUS protocol, including pxGrid integration for security context sharing and standard authentication settings:

```yaml
catalyst_center:
  system_settings:
    authentication_and_policy_servers:
      ise:
        ip_address: 198.18.133.27
        shared_secret: "Shared12345"
        username: "admin"
        password: "RandomPass12345"
        fqdn: ise.example.net
        pxgrid_enabled: true
        use_catc_cert_for_pxgrid: false
        retries: 3
        timeout: 4
        protocols:
          radius:
            authentication_port: 1812
            accounting_port: 1813
```

Example-2: ISE server with TACACS and RADIUS key wrap encryption for enhanced security, demonstrating the use of encryption and message keys to protect shared secrets in transit:

```yaml
catalyst_center:
  system_settings:
    authentication_and_policy_servers:
      ise:
        ip_address: 198.18.133.27
        shared_secret: "Shared12345"
        username: "admin"
        password: "RandomPass12345"
        fqdn: ise.example.net
        pxgrid_enabled: true
        use_catc_cert_for_pxgrid: false
        retries: 3
        timeout: 4
        protocols:
          tacacs:
            port: 49
          radius:
            authentication_port: 1812
            accounting_port: 1813
            enable_key_wrap:
              encryption_key: "qweqweqweqweqwe1"
              message_key: "dsdsd123454545454545"
```

Example-3: Comprehensive deployment with ISE as primary policy server and multiple AAA servers for redundancy, demonstrating enterprise-grade authentication infrastructure with pxGrid integration, key wrap encryption, and geographically distributed AAA servers for resilience:

```yaml
catalyst_center:
  system_settings:
    authentication_and_policy_servers:
      ise:
        ip_address: 198.18.133.27
        shared_secret: "Shared12345"
        username: "admin"
        password: "RandomPass12345"
        fqdn: ise.example.net
        pxgrid_enabled: true
        use_catc_cert_for_pxgrid: false
        retries: 3
        timeout: 4
        protocols:
          tacacs:
            port: 49
          radius:
            authentication_port: 1812
            accounting_port: 1813
            enable_key_wrap:
              encryption_key: "qweqweqweqweqwe1"
              message_key: "dsdsd123454545454545"
      aaa:
        - ip_address: 198.18.133.111
          shared_secret: "Shared12345"
          retries: 3
          timeout: 5
          protocols:
            tacacs:
              port: 49
            radius:
              authentication_port: 1812
              accounting_port: 1813
        - ip_address: 198.18.133.112
          shared_secret: "Shared12345"
          retries: 3
          timeout: 5
          protocols:
            tacacs:
              port: 49
            radius:
              authentication_port: 1812
              accounting_port: 1813
        - ip_address: 198.18.133.113
          shared_secret: "Shared12345"
          retries: 2
          timeout: 5
          protocols:
            tacacs:
              port: 49
            radius:
              authentication_port: 1812
              accounting_port: 1813
              enable_key_wrap:
                encryption_key: "qweqweqweqweasd1"
                message_key: "dsdsd123454545454567"
```

