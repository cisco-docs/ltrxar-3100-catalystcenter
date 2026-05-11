# AAA Servers

*Location in GUI*:
`Design` » `Network Settings` » `Servers`

{{ doc_gen }}

AAA Server settings define the RADIUS and TACACS+ server configurations used for network device authentication and client/endpoint authentication at the site level. These are distinct from the global [Authentication and Policy Servers](/docs/data_models/catalyst_center/system_settings/authentication_and_policy_servers) — AAA settings are assigned to sites and inherited down the hierarchy. Applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic AAA server configuration using ISE with RADIUS protocol for both network device authentication and client/endpoint authentication, deployed with primary server IP for centralized authentication services:

```yaml
catalyst_center:
  network_settings:
    aaa_servers:
      - name: BASIC_ISE_AAA
        network_aaa:
          server_type: ISE
          protocol: RADIUS
          primary_ip: 198.18.133.27
        client_and_endpoint_aaa:
          server_type: ISE
          protocol: RADIUS
          primary_ip: 198.18.133.27
```

Example-2: Enterprise AAA configuration with high availability setup using primary and secondary ISE servers, including PAN (Primary Administration Node) configuration across European corporate locations:

```yaml
catalyst_center:
  network_settings:
    aaa_servers:
      - name: ENTERPRISE_ISE_HA
        network_aaa:
          server_type: ISE
          protocol: RADIUS
          primary_ip: 10.1.100.10
          secondary_ip: 10.1.100.11
          pan: 10.1.100.5
        client_and_endpoint_aaa:
          server_type: ISE
          protocol: RADIUS
          primary_ip: 10.1.100.10
          secondary_ip: 10.1.100.11
          pan: 10.1.100.5
```

Example-3: Comprehensive multi-protocol AAA deployment demonstrating ISE for RADIUS-based client authentication and traditional AAA server for TACACS+ network device management, with complete redundancy configuration including primary/secondary servers, PAN nodes, and protocol-specific shared secret for TACACS:

```yaml
catalyst_center:
  network_settings:
    aaa_servers:
      - name: GLOBAL_ISE_RADIUS
        client_and_endpoint_aaa:
          server_type: ISE
          protocol: RADIUS
          primary_ip: 192.168.10.100
          secondary_ip: 192.168.10.101
          pan: 192.168.10.50
      - name: GLOBAL_TACACS_MGMT
        network_aaa:
          server_type: AAA
          protocol: TACACS
          primary_ip: 192.168.20.100
          secondary_ip: 192.168.20.101
          shared_secret: "TacacsMgmtSecret321"
      - name: BRANCH_SIMPLE_AAA
        network_aaa:
          server_type: AAA
          protocol: RADIUS
          primary_ip: 172.16.1.10
        client_and_endpoint_aaa:
          server_type: AAA
          protocol: RADIUS
          primary_ip: 172.16.1.10
```

Example-4: Site assignment configuration showing how to apply AAA server settings to specific locations in the site hierarchy:

```yaml
catalyst_center:
  sites:
    areas:
      - name: Corporate Campus
        parent_name: Global/Americas/USA/California
        network_settings:
          aaa_servers: ENTERPRISE_ISE_HA
      - name: Branch Office
        parent_name: Global/Americas/USA/Texas
        network_settings:
          aaa_servers: BRANCH_SIMPLE_AAA
    buildings:
      - name: Data Center
        parent_name: Global/Europe/Germany/Munich
        network_settings:
          aaa_servers: GLOBAL_TACACS_MGMT
```