# Telemetry

*Location in GUI*:
`Design` » `Network Settings` » `Telemetry`

{{ doc_gen }}

Telemetry settings configure network monitoring and analytics data collection from managed devices, including wired and wireless data collection, SNMP traps, syslog, and NetFlow. Telemetry can use Catalyst Center itself or external collectors. Settings are assigned to sites and inherited down the hierarchy. Applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic telemetry configuration enabling wired data collection and using Catalyst Center as the primary collector for network monitoring and analytics:

```yaml
catalyst_center:
  network_settings:
    telemetry:
      - name: BASIC_TELEMETRY
        wired_data_collection: true
        wireless_telemetry: false
        enable_netflow_collector_on_devices: false
        catalyst_center_as_network_collector: true
        catalyst_center_as_snmp_server: true
        catalyst_center_as_syslog_server: true
```

Example-2: Enterprise telemetry setup with comprehensive monitoring including both wired and wireless data collection, NetFlow enabled, and external SNMP and syslog servers for centralized logging and monitoring:

```yaml
catalyst_center:
  network_settings:
    telemetry:
      - name: ENTERPRISE_TELEMETRY
        wired_data_collection: true
        wireless_telemetry: true
        enable_netflow_collector_on_devices: true
        catalyst_center_as_network_collector: true
        catalyst_center_as_snmp_server: false
        catalyst_center_as_syslog_server: false
        snmp_servers:
          - 10.100.5.10
          - 10.100.5.11
        syslog_servers:
          - 10.100.5.20
          - 10.100.5.21
```

Example-3: Comprehensive global telemetry deployment with multiple configurations for different monitoring requirements including dedicated NetFlow collectors, mixed internal and external monitoring servers, and region-specific telemetry settings for worldwide enterprise infrastructure:

```yaml
catalyst_center:
  network_settings:
    telemetry:
      - name: GLOBAL_COMPREHENSIVE_TELEMETRY
        wired_data_collection: true
        wireless_telemetry: true
        enable_netflow_collector_on_devices: true
        catalyst_center_as_network_collector: false
        netflow_collector_ip_address: 172.16.100.50
        netflow_collector_port: 9995
        catalyst_center_as_snmp_server: true
        catalyst_center_as_syslog_server: true
        snmp_servers:
          - 172.16.100.10
          - 172.16.100.11
          - 172.16.100.12
        syslog_servers:
          - 172.16.100.20
          - 172.16.100.21
          - 172.16.100.22
      - name: BRANCH_BASIC_TELEMETRY
        wired_data_collection: true
        wireless_telemetry: false
        enable_netflow_collector_on_devices: false
        catalyst_center_as_network_collector: true
        catalyst_center_as_snmp_server: true
        catalyst_center_as_syslog_server: true
        syslog_servers:
          - 172.16.200.10
      - name: DC_ADVANCED_TELEMETRY
        wired_data_collection: true
        wireless_telemetry: false
        enable_netflow_collector_on_devices: true
        catalyst_center_as_network_collector: false
        netflow_collector_ip_address: 172.16.150.100
        netflow_collector_port: 2055
        catalyst_center_as_snmp_server: false
        catalyst_center_as_syslog_server: false
        snmp_servers:
          - 172.16.150.10
          - 172.16.150.11
        syslog_servers:
          - 172.16.150.20
          - 172.16.150.21
```

Example-4: Site assignment configuration demonstrating how to apply different telemetry settings based on site type, monitoring requirements, and infrastructure complexity:

```yaml
catalyst_center:
  sites:
    areas:
      - name: Corporate Region
        parent_name: Global/Americas
        network_settings:
          telemetry: GLOBAL_COMPREHENSIVE_TELEMETRY
      - name: Branch Regions
        parent_name: Global/Americas/Branches
        network_settings:
          telemetry: BRANCH_BASIC_TELEMETRY
    buildings:
      - name: Corporate Headquarters
        parent_name: Global/Americas/USA/California/San Jose
        network_settings:
          telemetry: ENTERPRISE_TELEMETRY
      - name: Data Center
        parent_name: Global/Americas/USA/Texas/Dallas
        network_settings:
          telemetry: DC_ADVANCED_TELEMETRY
      - name: Branch Office
        parent_name: Global/Americas/USA/Florida/Miami
        network_settings:
          telemetry: BASIC_TELEMETRY
```