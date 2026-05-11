# Layer 2 Handoff

*Location in GUI*:
`Provision` » `SD-Access` » `Fabric Sites` » `Fabric Infrastructure` » `Border Node` » `Configure` » `Layer 2 Handoff`

{{ doc_gen }}

Layer 2 Handoffs extend [Layer 2 Virtual Networks](/docs/data_models/catalyst_center/fabric/layer_2_virtual_network) beyond the SD-Access fabric boundary through [Border Devices](/docs/data_models/catalyst_center/fabric/border_device). They enable VLAN bridging to external networks for legacy systems or applications requiring Layer 2 adjacency, and can be combined with [Anycast Gateways](/docs/data_models/catalyst_center/fabric/anycast_gateway) for distributed gateway services. This resource is **SDA fabric only**.

### Examples

Example-1: Layer 2 Handoff with Anycast Gateway Configuration

This example demonstrates how to configure a Layer 2 handoff with anycast gateway functionality on an SD-Access border device. Anycast gateway enables distributed Layer 3 services across the fabric while maintaining Layer 2 extension to external networks for legacy systems or specialized applications.

The L2 handoff with anycast gateway configuration includes:
* Border device specification (BR01) with dual Layer 2 and Layer 3 functionality
* External VLAN (400) for network extension beyond the fabric boundary
* l3_virtual_network name (Campus) that must match the L3 virtual network configuration
* Integration with fabric-wide Layer 3 services while providing Layer 2 connectivity

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
        l2_handoffs:
          l2_with_anycast_gateway:
            - l3_virtual_network: Campus
              ip_pool_name: USERS
              external_vlan: 400
              interfaces:
                - GigabitEthernet1/0/8

```

To create L2 handoff with anycast gateway, `ip_pool_name` has to match `ip_pool_name` name configured under `anycast_gateways`:

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Krakow
        authentication_template:
          name: No Authentication
        pub_sub_enabled: true
        l3_virtual_networks:
          - Campus
```

Example-2: Layer 2 Handoff without Anycast Gateway Configuration

This example shows how to configure a Layer 2 handoff without anycast gateway functionality for pure Layer 2 extension scenarios. This configuration is suitable for extending VLANs to external networks where Layer 3 services remain centralized or where legacy Layer 2 requirements must be maintained.

The L2 handoff without anycast gateway configuration includes:
* VLAN specification (L2_VLAN_USERS) with external VLAN mapping (500) for network segmentation
* Physical interface assignment for Layer 2 connectivity to external infrastructure
* VLAN name matching requirement with L2 virtual network configuration
* Pure Layer 2 extension without distributed gateway functionality

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
        l2_handoffs:
          l2_without_anycast_gateway:
            vlans:
              - name: L2_VLAN_USERS
                external_vlan: 500
            interfaces:
              - GigabitEthernet1/0/6

```

To create L2 handoff without anycast gateway, name of vlan has to match vlan name created under `l2_virtual_networks`:

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Krakow
        authentication_template:
          name: No Authentication
        pub_sub_enabled: true
        l2_virtual_networks:
          - name: L2_SDA_VN_1
            vlan_name: L2_VLAN_USERS
            vlan_id: 501
            traffic_type: DATA
            fabric_enabled_wireless: false
```

Example-3: Multi-VLAN Layer 2 Handoff Configuration

This example demonstrates how to configure multiple VLANs within a single Layer 2 handoff without anycast gateway, for environments requiring multiple Layer 2 segments to be extended beyond the fabric boundary.

```yaml
---
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
        l2_handoffs:
          l2_without_anycast_gateway:
            vlans:
              - name: USER_VLAN
                external_vlan: 100
              - name: IOT_VLAN
                external_vlan: 200
              - name: GUEST_VLAN
                external_vlan: 300
            interfaces:
              - GigabitEthernet1/0/10

```

Example-4: Hybrid Layer 2 Handoff Configuration

This example demonstrates how to configure both anycast gateway and non-anycast gateway Layer 2 handoffs on the same border device for environments with mixed Layer 2 extension requirements.

```yaml
---
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
        l2_handoffs:
          l2_with_anycast_gateway:
            - l3_virtual_network: SDA_VN_USERS
              ip_pool_name: USERS
              external_vlan: 470
              interfaces:
                - GigabitEthernet1/0/8
          l2_without_anycast_gateway:
            vlans:
              - name: L2_VLAN_USERS
                external_vlan: 999
            interfaces:
              - GigabitEthernet1/0/23

```
