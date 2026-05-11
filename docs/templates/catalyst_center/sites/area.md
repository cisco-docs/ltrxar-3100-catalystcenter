# Area

*Location in GUI*:
`Design` » `Network Hierarchy`

{{ doc_gen }}

Areas represent the top-level organizational containers in the Catalyst Center site hierarchy (e.g., regions, countries, campuses). They group [Buildings](/docs/data_models/catalyst_center/sites/building) and other Areas, and can have device credentials, network settings, and IP pool reservations inherited by all child sites. Areas are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic area configuration creating a simple geographic hierarchy with minimal settings for regional organization:

```yaml
catalyst_center:
  sites:
    areas:
      - name: Americas
        parent_name: Global
      - name: EMEA
        parent_name: Global
      - name: APAC
        parent_name: Global
      - name: USA
        parent_name: Global/Americas
      - name: Canada
        parent_name: Global/Americas
```

Example-2: Comprehensive area deployment with complete credential assignments, network settings, and IP pool reservations for enterprise-grade site management across multiple geographic regions:

```yaml
catalyst_center:
  sites:
    areas:
      - name: North America
        parent_name: Global/Americas
        cli_credentials: AMERICAS_CLI_ADMIN
        snmpv3_credentials: SECURE_SNMPV3_AUTHPRIV
        snmpv2_read_credentials: AMERICAS_SNMP_READ
        snmpv2_write_credentials: AMERICAS_SNMP_WRITE
        https_read_credentials: API_READ_ACCESS
        https_write_credentials: API_WRITE_ACCESS
        network_settings:
          aaa_servers: AMERICAS_AAA_SETTINGS
          network: AMERICAS_NETWORK_SETTINGS
          telemetry: AMERICAS_TELEMETRY
        ip_pools_reservations:
          - CORPORATE_POOL
          - MGMT_NETWORK_POOL
      - name: Europe
        parent_name: Global/EMEA
        cli_credentials: EMEA_CLI_ADMIN
        snmpv3_credentials: STANDARD_SNMPV3_AUTHNOPRIV
        snmpv2_read_credentials: EMEA_SNMP_READ
        https_read_credentials: MONITORING_API_ACCESS
        network_settings:
          aaa_servers: EMEA_AAA_SETTINGS
          network: EMEA_NETWORK_SETTINGS
          telemetry: ENTERPRISE_TELEMETRY
        ip_pools_reservations:
          - CAMPUS_LAN_AUTO
          - CAMPUS_AP_POOL
      - name: Asia Pacific
        parent_name: Global/APAC
        cli_credentials: APAC_CLI_ADMIN
        snmpv2_read_credentials: APAC_SNMP_READ
        network_settings:
          network: APAC_NETWORK_SETTINGS
          telemetry: BASIC_TELEMETRY
        ip_pools_reservations:
          - BRANCH_WAN_POOL
          - SERVICE_NETWORK_POOL
```
