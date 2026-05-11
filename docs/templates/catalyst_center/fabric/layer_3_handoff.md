# Layer 3 Handoff

*Location in GUI*:
`Provision` » `SD-Access` » `Fabric Sites` » `Fabric Infrastructure` » `Border Node` » `Configure` » `Layer 3 Handoff`

{{ doc_gen }}

Layer 3 Handoffs enable routing between SD-Access fabric [Virtual Networks](/docs/data_models/catalyst_center/fabric/layer_3_virtual_network) and external Layer 3 infrastructure through [Border Devices](/docs/data_models/catalyst_center/fabric/border_device). Handoffs are associated with a [Transit](/docs/data_models/catalyst_center/fabric/transit) (IP-based or SDA) and define per-VN routing parameters such as VLAN, interface, and local/remote autonomous system numbers. This resource is **SDA fabric only**.

### Examples

Example-1: Basic Custom Layer 3 Handoff with Multiple Virtual Networks

This example demonstrates how to configure a basic Layer 3 handoff on an SD-Access border device for connecting fabric virtual networks to external Layer 3 infrastructure. Layer 3 handoffs enable routing between SD-Access fabric virtual networks and external networks through IP Transit connections.

The Layer 3 handoff configuration includes:
* Border device specification (BR01) with Layer 3 and Layer 2 functionality
* IP Transit name (IP_TRANSIT) for external connectivity identification
* Physical interface assignment (TenGigabitEthernet1/1/4) for high-bandwidth connectivity
* Multiple virtual network mappings with dedicated IP addressing and VLAN segmentation
* Point-to-point IP addressing for each virtual network (local and peer IP addresses)
* VLAN tagging (120, 121, 122) for traffic segregation across virtual networks

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
          - LAYER_2
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65001
        l3_handoffs:
          - name: IP_TRANSIT
            interfaces:
              - name: TenGigabitEthernet1/1/4
                virtual_networks:
                  - name: SDA_VN_USERS
                    local_ip_address: 10.0.0.1/24
                    peer_ip_address: 10.0.0.2/24
                    vlan: 120
                  - name: SDA_VN_PRINTERS
                    local_ip_address: 11.0.0.1/24
                    peer_ip_address: 11.0.0.2/24
                    vlan: 121
                  - name: SDA_VN_CORPORATE
                    local_ip_address: 12.0.0.1/24
                    peer_ip_address: 12.0.0.2/24
                    vlan: 122
```

`Note` The `l3_handoffs name` must match the name of the IP Transit.

Example-2: Single Virtual Network Custom Layer 3 Handoff

This example shows how to configure a simplified Layer 3 handoff with a single virtual network for environments  with basic external connectivity requirements and single-tenant scenarios including tcp-mss adjustment.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: true
        local_autonomous_system_number: 65001
        l3_handoffs:
          - name: CORPORATE_TRANSIT
            interfaces:
              - name: GigabitEthernet1/0/1
                virtual_networks:
                  - name: CORPORATE_VN
                    local_ip_address: 192.168.1.1/30
                    peer_ip_address: 192.168.1.2/30
                    vlan: 100
                    tcp_mss_adjustment: 1400

```


Example-3: Virtual Network Layer 3 Handoff using a Pre-defined handoff pool `HANDOFF_POOL`

This example shows how to configure a simplified Layer 3 handoff with a single virtual network for environments  with basic external connectivity requirements.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65001
        external_handoff_pool: HANDOFF_POOL
        l3_handoffs:
          - name: BGP65002
            interfaces:
              - name: GigabitEthernet1/0/15
                virtual_networks:
                  - name: Campus
                    vlan: 330
                  - name: Guest
                    vlan: 430
```


Example-4: Virtual Network Layer 3 Handoff using combination of `Custom` and Pre-defined handoff pool named `HANDOFF_POOL`


`Note` : Custom handoff allows the Administrator to define the local handoff_ip_address to be configured on the Border, whereas using a predefined handoff pool uses Catalyst Center's Logic to create the handoff and requires the pool to be already configured and reserved at that site


This example shows how to configure a Layer 3 handoff using custom and predefined handoff pool on different handoff interfaces on the same device.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65001
        external_handoff_pool: HANDOFF_POOL
        l3_handoffs:
          - name: BGP65002
            interfaces:
              - name: GigabitEthernet1/0/15
                virtual_networks:
                  - name: Campus
                    vlan: 330
                  - name: Guest
                    vlan: 430
                  - name: Printers
                    vlan: 530

              - name: GigabitEthernet1/0/17
                virtual_networks:
                  - name: BYOD
                    local_ip_address: 172.18.100.1/24
                    peer_ip_address: 172.18.100.2/24
                    vlan: 650
```

Example-5: High-Availability Custom Layer 3 Handoff with Redundant Interfaces

This example demonstrates how to configure Layer 3 handoffs across multiple physical interfaces for high availability and load balancing in critical network environments.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
          - LAYER_2
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65001
        l3_handoffs:
          - name: PRIMARY_TRANSIT
            interfaces:
              - name: TenGigabitEthernet1/1/1
                virtual_networks:
                  - name: PRODUCTION_VN
                    local_ip_address: 10.1.1.1/30
                    peer_ip_address: 10.1.1.2/30
                    vlan: 101
              - name: TenGigabitEthernet1/1/2
                virtual_networks:
                  - name: PRODUCTION_VN
                    local_ip_address: 10.1.2.1/30
                    peer_ip_address: 10.1.2.2/30
                    vlan: 102
```

Example-6: Multi-Border Custom Layer 3 Handoff Configuration

This example shows how to configure Layer 3 handoffs across multiple border devices for distributed fabric architecture with redundant external connectivity points.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
          - LAYER_2
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65001
        l3_handoffs:
          - name: NORTH_TRANSIT
            interfaces:
              - name: TenGigabitEthernet1/1/1
                virtual_networks:
                  - name: ENTERPRISE_VN
                    local_ip_address: 172.16.1.1/30
                    peer_ip_address: 172.16.1.2/30
                    vlan: 201
      - name: BR02
        border_types:
          - LAYER_3
          - LAYER_2
        default_exit: false
        import_external_routes: false
        local_autonomous_system_number: 65001
        l3_handoffs:
          - name: SOUTH_TRANSIT
            interfaces:
              - name: TenGigabitEthernet1/1/1
                virtual_networks:
                  - name: ENTERPRISE_VN
                    local_ip_address: 172.16.2.1/30
                    peer_ip_address: 172.16.2.2/30
                    vlan: 202
```

Example-7: Custom Layer 3 Handoff with External Route Import

This example demonstrates how to configure a Layer 3 handoff with external route import enabled for learning routes from external networks and propagating them throughout the SD-Access fabric.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
          - LAYER_2
        default_exit: true
        import_external_routes: true
        local_autonomous_system_number: 65001
        l3_handoffs:
          - name: WAN_TRANSIT
            interfaces:
              - name: TenGigabitEthernet1/1/3
                virtual_networks:
                  - name: BRANCH_CONNECTIVITY_VN
                    local_ip_address: 203.0.113.1/30
                    peer_ip_address: 203.0.113.2/30
                    vlan: 300
                  - name: INTERNET_ACCESS_VN
                    local_ip_address: 198.51.100.1/30
                    peer_ip_address: 198.51.100.2/30
                    vlan: 301
```

Example-8: Service Provider Custom Layer 3 Handoff Configuration

This example shows how to configure Layer 3 handoffs for service provider environments with customer-specific virtual networks and multi-tenant isolation requirements.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: SP_BR01
        border_types:
          - LAYER_3
          - LAYER_2
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65100
        l3_handoffs:
          - name: CUSTOMER_A_TRANSIT
            interfaces:
              - name: TenGigabitEthernet1/1/5
                virtual_networks:
                  - name: CUSTOMER_A_PROD_VN
                    local_ip_address: 10.100.1.1/30
                    peer_ip_address: 10.100.1.2/30
                    vlan: 1001
                  - name: CUSTOMER_A_DEV_VN
                    local_ip_address: 10.100.2.1/30
                    peer_ip_address: 10.100.2.2/30
                    vlan: 1002
          - name: CUSTOMER_B_TRANSIT
            interfaces:
              - name: TenGigabitEthernet1/1/6
                virtual_networks:
                  - name: CUSTOMER_B_PROD_VN
                    local_ip_address: 10.200.1.1/30
                    peer_ip_address: 10.200.1.2/30
                    vlan: 2001
```
