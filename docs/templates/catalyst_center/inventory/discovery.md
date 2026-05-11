# Discovery

*Location in GUI*:
`Tools` » `Discovery`

{{ doc_gen }}

Discovery automates the process of finding and adding network devices to the Catalyst Center inventory using CDP, LLDP, or IP range-based scanning. Discovered devices use the [Device Credentials](/docs/data_models/catalyst_center/network_settings/device_credentials) configured at the site level. After discovery, devices can be [assigned to sites](/docs/data_models/catalyst_center/inventory/assign_device_to_site) and provisioned. Applicable to both SDA fabric and non-fabric deployments.

### Examples


**Prerequisite**: CLI, SNMP, HTTPS credentials listed under global_credential_list needs to exists in Catalyst Center or you can define them using following example:



Example-1: Device Credentials for Discovery Authentication

This example shows how to configure the CLI credentials required for network device discovery. These credentials can be created using the Data model before being referenced in discovery jobs to ensure proper device authentication and access.

The CLI credentials configuration includes:
* CLI Credential name (dnacadmin) and SNMP credentials that will be referenced in the discovery global credential list
* Foundation for secure device discovery and subsequent management operations

```yaml
---
catalyst_center:
  network_settings:
    device_credentials:
      cli_credentials:
        - name: dnacadmin
          username: dnacadmin
          password: C1sco12345
          enable: C1sco12345
      snmpv2_read_credentials:
        - name: GLOBAL_SNMP_READ
          description: "Global monitoring read access"
          read_community: RO
      snmpv2_write_credentials:
        - name: GLOBAL_SNMP_WRITE
          description: "Global configuration write access"
          write_community: RW
      snmpv3_credentials:
        - name: SECURE_SNMPV3_AUTHPRIV
          auth_type: SHA
          privacy_type: AES128
          snmp_mode: AUTHPRIV
          username: secureuser
          auth_password: SecureAuth2025!
          privacy_password: SecurePriv2025!
      https_read_credentials:
        - name: HTTP_READ_ACCESS
          username: apphost_http_read
          password: ApiRead2025!
          port: 443
      https_write_credentials:
        - name: HTTP_WRITE_ACCESS
          username: apphost_http_write
          password: ApiWrite2025!
          port: 443

```

Example-2: Basic IP Range Discovery

This example demonstrates how to configure basic network device discovery using an IP address range in Catalyst Center. Network discovery is the foundational process for identifying and onboarding network devices into the Catalyst Center inventory for centralized management and monitoring.

The discovery configuration includes:
* Discovery name (Discovery1) for identification and tracking of discovery jobs
* Range type discovery for scanning contiguous IP address blocks
* Global credential list (dnacadmin) referencing pre-configured CLI and SNMP credentials for device authentication
* IP address range (198.18.130.1-198.18.130.10) defining the scope of network devices to discover
* Preferred IP method set to None for automatic IP selection during discovery
* Protocol order (SSH, Telnet) specifying connection priority for device authentication
* Timeout setting (60 seconds) for discovery connection attempts and device response

```yaml
catalyst_center:
  inventory:
    discovery:
      - name: Discovery1
        type: Range
        global_credential_list:
          - dnacadmin
          - GLOBAL_SNMP_READ
          - GLOBAL_SNMP_WRITE
        ip_address_list: "198.18.130.1-198.18.130.10"
        preferred_mgmt_ip_method: None
        protocol_order: SSH,Telnet
        time_out: 60
```



Example-3: Multi-Network Discovery with Different Credential Sets

This example demonstrates how to configure multiple discovery jobs targeting different network segments with specific credential sets for diverse network environments and security requirements.

```yaml
catalyst_center:
  inventory:
    discovery:
      - name: CAMPUS_CORE_DISCOVERY
        type: Range
        global_credential_list:
          - campus-admin
          - GLOBAL_SNMP_READ
          - GLOBAL_SNMP_WRITE
        ip_address_list: "10.1.0.1-10.1.0.50"
        preferred_mgmt_ip_method: UseLoopBack
        protocol_order: SSH
        time_out: 90
        enable_password_list:
          - campus-enable
      - name: BRANCH_NETWORK_DISCOVERY
        type: Range
        global_credential_list:
          - branch-readonly
          - SECURE_SNMPV3_AUTHPRIV
        ip_address_list: "192.168.100.1-192.168.100.254"
        preferred_mgmt_ip_method: UseLoopBack
        protocol_order: SSH,Telnet
        time_out: 45
```

Example-4: CIDR-Based Discovery for Large Network Segments

This example shows how to configure discovery using CIDR notation for efficient scanning of large network segments, suitable for enterprise environments with substantial network infrastructure.

```yaml
catalyst_center:
  inventory:
    discovery:
      - name: ENTERPRISE_WIDE_DISCOVERY
        type: CIDR
        global_credential_list:
          - enterprise-admin
          - monitoring-readonly
          - SECURE_SNMPV3_AUTHPRIV
        ip_address_list: "172.16.0.0/16"
        preferred_mgmt_ip_method: None
        protocol_order: SSH
        time_out: 120
```

Example-5: Single Device Discovery with SNMP Integration

This example demonstrates how to configure discovery for specific devices with comprehensive SNMP integration for enhanced device monitoring and management capabilities during the discovery process. The SNMP configuration is referenced in the `global_credential_list`

```yaml
catalyst_center:
  inventory:
    discovery:
      - name: CRITICAL_DEVICE_DISCOVERY
        type: Single
        global_credential_list:
          - critical-admin
          - SECURE_SNMPV3_AUTHPRIV
        ip_address_list: "10.10.10.1"
        preferred_mgmt_ip_method: None
        protocol_order: SSH
        time_out: 180
```

Example-6: Comprehensive Multi-Protocol Discovery Job

This example shows how to configure a comprehensive discovery job with multiple authentication protocols and credential fallback options for complex network environments with diverse device types and configurations.

```yaml
catalyst_center:
  inventory:
    discovery:
      - name: COMPREHENSIVE_DISCOVERY
        type: Range
        global_credential_list:
          - primary-admin
          - secondary-admin
          - GLOBAL_SNMP_READ
          - GLOBAL_SNMP_WRITE
          - SECURE_SNMPV3_AUTHPRIV
        ip_address_list: "10.0.0.1-10.0.255.254"
        preferred_mgmt_ip_method: Management
        protocol_order: SSH,Telnet
        time_out: 300
        retry: 3
        netconf_port: "830"

      - name: Discovery_10_9_1_15
        type: Single
        global_credential_list:
          - primary-admin
          - secondary-admin
          - GLOBAL_SNMP_READ
          - GLOBAL_SNMP_WRITE
          - SECURE_SNMPV3_AUTHPRIV
        ip_address_list: '10.9.1.15'
        preferred_mgmt_ip_method: UseLoopBack
        protocol_order: SSH,Telnet
        time_out: 300
        retry: 3
        netconf_port: "830"

      - name: Discovery_CDP_Seed_Device
        type: CDP
        global_credential_list:
          - primary-admin
          - secondary-admin
          - GLOBAL_SNMP_READ
          - GLOBAL_SNMP_WRITE
          - SECURE_SNMPV3_AUTHPRIV
        ip_address_list: '10.9.0.1'
        preferred_mgmt_ip_method: UseLoopBack
        protocol_order: SSH,Telnet
        time_out: 300
        cdp_level: 5
        retry: 3
        netconf_port: "830"

      - name: Discovery_Muliti_Range
        type: Multi Range
        global_credential_list:
          - primary-admin
          - secondary-admin
          - GLOBAL_SNMP_READ
          - GLOBAL_SNMP_WRITE
          - SECURE_SNMPV3_AUTHPRIV
        ip_address_list: '10.9.1.16-10.9.1.16,10.9.1.19-10.9.1.20'
        preferred_mgmt_ip_method: UseLoopBack
        protocol_order: SSH,Telnet
        time_out: 300
        retry: 3
        netconf_port: "830"

```
