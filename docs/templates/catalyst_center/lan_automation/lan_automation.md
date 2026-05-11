# LAN Automation

*Location in GUI*:
`Provision` » `Network Devices` » `LAN Automation`

{{ doc_gen }}

LAN Automation simplifies the deployment of access layer switches by automatically discovering, configuring, and onboarding new devices into the network. It uses a seed device (typically a distribution switch) to discover downstream switches via CDP/LLDP, assigns IP addresses from a dedicated LAN-type [IP Pool](/docs/data_models/catalyst_center/network_settings/ip_pool), and provisions them into the site hierarchy. This resource is primarily used in **SDA fabric** deployments for automated underlay provisioning.

### Examples

Before running LAN Automation, the IP pool used for LAN automation (eg. `LAN_AUTO_POol`) with type `LAN` must be created and assigned to the site:

Example-1: Basic LAN Automation for Edge Switch Discovery

This example demonstrates how to configure LAN Automation in Catalyst Center for automated discovery and assignment of access switches. LAN Automation simplifies the deployment of access layer switches by automatically discovering, configuring, and on-boarding new devices into the network infrastructure.

The LAN Automation configuration includes:
* Automation name (EDGE_SWITCHES) for identification and workflow tracking
* START status to initiate the automated discovery process
* Device type targeting for switch discovery and provisioning
* Site hierarchy assignment (Global/Poland/Krakow) for discovered devices
* Primary device configuration with management IP and interface specifications
* IP pool assignment (LAN_AUTO_Pool) for automated IP address allocation
* Hostname prefix (lan-EN) for systematic device naming convention
* Discovery parameters including level (2 hops) and timeout (20 minutes)
* Specific device discovery with serial numbers and management addresses

```yaml
---
catalyst_center:
  lan_automation:
    - name: EDGE_SWTICHES
      status: START
      type: devices
      discovered_device_site_name_hierarchy: Global/Poland/Krakow
      primary_device_management_ip_address: 198.18.130.10
      secondary_device_management_ip_address: 198.18.130.20
      primary_device_interface_names:
        - GigabitEthernet1/0/20
      ip_pools:
        - name: LAN_AUTO_Pool
          role: PRINCIPAL_IP_ADDRESS_POOL
      host_name_prefix: lan-EN
      advertise_lan_automation_routes_into_bgp: false
      multicast_enabled: true
      discovery_level: 2
      discovery_timeout: 20
      discovery_devices:
        - device_serial_number: "FOC12345678"
          device_host_name: "EDGE01"
          device_site_name_hierarchy: Global/Poland/Krakow/Bld A
          device_management_ip_address: "192.168.252.10"
```

Example-2: IP Pool Configuration for LAN Automation

This example shows how to configure the IP pool required for LAN Automation. The IP pool must be created and reserved before running LAN Automation to ensure proper IP address allocation for discovered devices.

The IP pool configuration includes:
* Parent pool (Overlay) with IPv4 address space covering the entire network range
* LAN Automation specific reservation (LAN_AUTO) with LAN type designation
* Subnet allocation (192.168.252.0/24) for automated device management addressing
* Gateway specification (192.168.252.1) for network connectivity and routing

```yaml
---
catalyst_center:
  network_settings:
    ip_pools:
      - name: Overlay
        ip_address_space: IPv4
        ip_pool_cidr: 192.168.0.0/16
        ip_pools_reservations:
          - name: LAN_AUTO
            type: LAN
            prefix_length: 24
            subnet: 192.168.252.0
            gateway: 192.168.252.1
```

Example-3: Site Hierarchy and IP Pool Assignment

This example demonstrates how to configure the site hierarchy and assign IP pool reservations to the appropriate sites for LAN Automation deployment. Proper site organization ensures discovered devices are placed in the correct network locations.

```yaml
---
catalyst_center:
  sites:
    areas:
      - name: Poland
        parent_name: Global
      - name: Krakow
        parent_name: Global/Poland
        ip_pools_reservations:
          - LAN_AUTO
```

Example-4: Multi-Site LAN Automation with Different Discovery Levels

This example shows how to configure LAN Automation for multiple sites with different discovery requirements and network topologies, enabling scalable automated deployment across diverse locations.

```yaml
---
catalyst_center:
  lan_automation:
    - name: CAMPUS_DISTRIBUTION_DISCOVERY
      status: START
      type: devices
      discovered_device_site_name_hierarchy: Global/NorthAmerica/Campus
      primary_device_management_ip_address: 10.1.1.10
      secondary_device_management_ip_address: 10.1.1.20
      primary_device_interface_names:
        - TenGigabitEthernet1/0/1
        - TenGigabitEthernet1/0/2
      ip_pools:
        - name: LAN_AUTO_Pool
          role: PRINCIPAL_IP_ADDRESS_POOL
      host_name_prefix: campus-dist-
      advertise_lan_automation_routes_into_bgp: true
      multicast_enabled: true
      discovery_level: 3
      discovery_timeout: 30
      discovery_devices:
        - device_serial_number: "FDO12345678"
          device_host_name: "DIST-SW01"
          device_site_name_hierarchy: Global/NorthAmerica/Campus/Building A
          device_management_ip_address: "10.1.10.10"
        - device_serial_number: "FDO87654321"
          device_host_name: "DIST-SW02"
          device_site_name_hierarchy: Global/NorthAmerica/Campus/Building B
          device_management_ip_address: "10.1.20.10"
```

Example-5: Branch Office LAN Automation with Limited Discovery and stacked switch

This example demonstrates how to configure LAN Automation for branch office environments with link overlapping pool and limited discovery scope, suitable for smaller remote locations with basic switching requirements. It also demonstrates how to configure LAN Automation for stacked switch discovery. The `device_serial_number` field accepts comma-separated serial numbers to identify all members of a switch stack as a single logical device.

```yaml
---
catalyst_center:
  lan_automation:
    - name: Automate_Edge_Switches
      status: START
      type: devices
      discovered_device_site_name_hierarchy: Global/Canada/BLD1
      primary_device_management_ip_address: 198.18.130.10
      secondary_device_management_ip_address: 181.1.1.40
      primary_device_interface_names:
        - GigabitEthernet1/0/20
      ip_pools:
        - name: LAN_AUTO_Pool
          role: PRINCIPAL_IP_ADDRESS_POOL
        - name: LAN_AUTO_P2P_LINKS
          role: LINK_OVERLAPPING_IP_POOL
      multicast_enabled: true
      host_name_prefix: EN
      advertise_lan_automation_routes_into_bgp: true
      discovery_level: 2
      discovery_timeout: 20
      discovery_devices:
        - device_serial_number: "FOC12345678,FOC12345679,FOC12345670"
          device_host_name: "EDGE01"
          device_site_name_hierarchy: "Global/Canada/BLD1"
          device_management_ip_address: "192.168.252.10"
```
