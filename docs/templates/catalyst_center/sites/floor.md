# Floor

*Location in GUI*:
`Design` » `Network Hierarchy`

{{ doc_gen }}

Floors represent the lowest level of the site hierarchy, nested under [Buildings](/docs/data_models/catalyst_center/sites/building). They define physical dimensions (height, length, width), RF model for wireless planning, and can carry their own device credentials, network settings, and IP pool reservations. Floors are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic floor configuration with essential physical dimensions and RF modeling for wireless planning in typical office environments. the default units_of_measure is `feet`.

```yaml
catalyst_center:
  sites:
    floors:
      - name: Ground Floor
        parent_name: Global/Americas/USA/California/Corporate Headquarters
        floor_number: 0
        height: 18
        length: 500
        width: 300
        rf_model: Cubes And Walled Offices
      - name: Second Floor
        parent_name: Global/EMEA/United Kingdom/London Office
        floor_number: 2
        height: 15
        length: 400
        width: 250
        rf_model: Drywall Office Only
      - name: Data Center Floor
        parent_name: Global/APAC/Singapore/APAC Branch Office
        floor_number: -1
        height: 25
        length: 800
        width: 400
        rf_model: Indoor High Ceiling
```

Example-2: Comprehensive floor deployment with complete physical specifications, RF modeling, credential assignments, network settings, and IP pool reservations for enterprise facility management and wireless optimization:

```yaml
catalyst_center:
  sites:
    floors:
      - name: Executive Floor
        parent_name: Global/Americas/USA/California/San Jose/Global Headquarters
        floor_number: 20
        height: 19
        length: 60
        width: 45
        units_of_measure: feet
        rf_model: Cubes And Walled Offices
        cli_credentials: GLOBAL_CLI_ADMIN
        snmpv3_credentials: SECURE_SNMPV3_AUTHPRIV
        snmpv2_read_credentials: GLOBAL_SNMP_READ
        https_read_credentials: API_READ_ACCESS
        network_settings:
          aaa_servers: ENTERPRISE_AAA_SETTINGS
          network: ENTERPRISE_NETWORK_CONFIG
          telemetry: GLOBAL_COMPREHENSIVE_TELEMETRY
        ip_pools_reservations:
          - CORPORATE_POOL
          - MGMT_NETWORK_POOL
      - name: Engineering Lab
        parent_name: Global/EMEA/Netherlands/Amsterdam/European Data Center
        floor_number: 3
        height: 5
        length: 100
        width: 60
        units_of_measure: meters
        rf_model: Indoor High Ceiling
        cli_credentials: EMEA_CLI_ADMIN
        snmpv2_read_credentials: EMEA_SNMP_READ
        https_read_credentials: MONITORING_API_ACCESS
        network_settings:
          network: EMEA_NETWORK_SETTINGS
          telemetry: DC_ADVANCED_TELEMETRY
        ip_pools_reservations:
          - CAMPUS_LAN_AUTO
          - CAMPUS_AP_POOL
      - name: Open Workspace
        parent_name: Global/APAC/Singapore/APAC Branch Office
        floor_number: 5
        height: 12
        length: 115
        width: 650
        units_of_measure: feet
        rf_model: Free Space
        cli_credentials: BRANCH_CLI_READONLY
        network_settings:
          network: BASIC_NETWORK_SETTINGS
        ip_pools_reservations:
          - BRANCH_WAN_POOL
      - name: Warehouse Floor
        parent_name: Global/Americas/USA/Texas/Distribution Center
        floor_number: 1
        height: 40
        length: 650
        width: 500
        units_of_measure: feet
        rf_model: Outdoor Open Space
        snmpv2_read_credentials: BRANCH_SNMP_READ
        network_settings:
          telemetry: BRANCH_BASIC_TELEMETRY
```
