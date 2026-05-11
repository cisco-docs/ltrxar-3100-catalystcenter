# Building

*Location in GUI*:
`Design` » `Network Hierarchy`

{{ doc_gen }}

Buildings represent physical locations within the site hierarchy, nested under [Areas](/docs/data_models/catalyst_center/sites/area). They define geographic coordinates, address details, and can carry device credentials, network settings, and IP pool reservations inherited by their [Floors](/docs/data_models/catalyst_center/sites/floor). Buildings are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic building configuration with essential geographic information including coordinates and address for physical location mapping:

```yaml
catalyst_center:
  sites:
    buildings:
      - name: Corporate Headquarters
        parent_name: Global/Americas/USA/California
        latitude: 37.4419
        longitude: -122.1430
      - name: London Office
        parent_name: Global/EMEA/United Kingdom
        address: 25 Canada Square, London E14 5LQ, UK
        country: United Kingdom
```

Example-2: Comprehensive building deployment with complete credential assignments, network settings, IP pool reservations, and detailed geographic information for enterprise facility management:

```yaml
catalyst_center:
  sites:
    buildings:
      - name: Global Headquarters
        parent_name: Global/Americas/USA/California/San Jose
        latitude: 37.3382
        longitude: -121.8863
        address: 170 West Tasman Drive, San Jose, CA 95134, USA
        country: United States
        cli_credentials: GLOBAL_CLI_ADMIN
        snmpv3_credentials: SECURE_SNMPV3_AUTHPRIV
        snmpv2_read_credentials: GLOBAL_SNMP_READ
        snmpv2_write_credentials: GLOBAL_SNMP_WRITE
        https_read_credentials: API_READ_ACCESS
        https_write_credentials: API_WRITE_ACCESS
        network_settings:
          aaa_servers: ENTERPRISE_AAA_SETTINGS
          network: ENTERPRISE_NETWORK_CONFIG
          telemetry: GLOBAL_COMPREHENSIVE_TELEMETRY
        ip_pools_reservations:
          - CORPORATE_POOL
          - MGMT_NETWORK_POOL
          - SERVICE_NETWORK_POOL
      - name: European Data Center
        parent_name: Global/EMEA/Netherlands/Amsterdam
        latitude: 52.3676
        longitude: 4.9041
        address: Science Park 140, 1098 XG Amsterdam, Netherlands
        country: Netherlands
        cli_credentials: EMEA_CLI_ADMIN
        snmpv3_credentials: STANDARD_SNMPV3_AUTHNOPRIV
        snmpv2_read_credentials: EMEA_SNMP_READ
        https_read_credentials: MONITORING_API_ACCESS
        network_settings:
          aaa_servers: EMEA_AAA_SETTINGS
          network: EMEA_NETWORK_SETTINGS
          telemetry: DC_ADVANCED_TELEMETRY
        ip_pools_reservations:
          - CAMPUS_LAN_AUTO
          - CAMPUS_AP_POOL
          - CAMPUS_EXTENDED_NODE_POOL
      - name: APAC Branch Office
        parent_name: Global/APAC/Singapore
        latitude: 1.2966
        longitude: 103.7764
        address: 1 Raffles Place, Singapore 048616
        country: Singapore
        cli_credentials: BRANCH_CLI_READONLY
        snmpv2_read_credentials: BRANCH_SNMP_READ
        network_settings:
          network: BASIC_NETWORK_SETTINGS
          telemetry: BRANCH_BASIC_TELEMETRY
        ip_pools_reservations:
          - BRANCH_WAN_POOL
```
