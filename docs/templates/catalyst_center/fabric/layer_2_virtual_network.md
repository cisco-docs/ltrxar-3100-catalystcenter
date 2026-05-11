# Layer 2 Virtual Network

*Location in GUI*:
`Provision` » `SD-Access` » `Virtual Networks` » `Layer 2 Virtual Networks`

{{ doc_gen }}

Layer 2 Virtual Networks enable VLAN extension across the SD-Access fabric while maintaining Layer 2 adjacency for applications that require it. They are associated with a [Fabric Site](/docs/data_models/catalyst_center/fabric/fabric_site) and a traffic type, and can be handed off to external networks via [Layer 2 Handoffs](/docs/data_models/catalyst_center/fabric/layer_2_handoff) on [Border Devices](/docs/data_models/catalyst_center/fabric/border_device). This resource is **SDA fabric only**.

### Examples

Example-1: Basic Layer 2 Virtual Network for Data Traffic

This example demonstrates how to configure a basic Layer 2 virtual network within an SD-Access fabric site. Layer 2 virtual networks enable VLAN extension across the fabric while maintaining traditional Layer 2 networking semantics for applications and services that require Layer 2 adjacency.

The Layer 2 virtual network configuration includes:
* Virtual network name (L2_SDA_VN_1) for identification and policy assignment
* VLAN name (L2_VLAN_USERS) for traditional VLAN-based network segmentation
* VLAN ID (501) for 802.1Q tagging and network isolation
* Traffic type specification (DATA) for appropriate QoS and policy treatment
* Fabric-enabled wireless disabled for wired-only network segments

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Canada
        authentication_template:
          name: No Authentication
        l2_virtual_networks:
          - name: L2_SDA_VN_1
            vlan_name: L2_VLAN_USERS
            vlan_id: 501
            traffic_type: DATA
            fabric_enabled_wireless: false
```

Example-2: Layer 2 Virtual Network with Wireless Integration

This example shows how to configure a Layer 2 virtual network with fabric-enabled wireless support for unified wired and wireless connectivity. This configuration enables seamless Layer 2 extension across both wired and wireless infrastructure within the SD-Access fabric.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/North America/Corporate Campus
        authentication_template:
          name: Closed Authentication
        l2_virtual_networks:
          - name: CORPORATE_L2_NETWORK
            vlan_name: CORPORATE_USERS
            vlan_id: 100
            traffic_type: DATA
            fabric_enabled_wireless: true
```

Example-3: Layer 2 Virtual Networks with L3 Virtual Network Association

This example demonstrates how to configure Layer 2 virtual networks associated with Layer 3 virtual networks for inter-VLAN routing within the SD-Access fabric. Associating an L2 VN with an L3 VN enables routing between Layer 2 segments while maintaining Layer 2 adjacency within each segment.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Europe/ManufacturingPlant
        authentication_template:
          name: Closed Authentication
        l3_virtual_networks:
          - CORP_VN
          - IOT_VN
        l2_virtual_networks:
          - name: PRODUCTION_L2_VN
            vlan_name: PRODUCTION_CONTROL
            vlan_id: 200
            traffic_type: DATA
            fabric_enabled_wireless: false
            associated_l3_virtual_network_name: CORP_VN
          - name: IOT_L2_VN
            vlan_name: IOT_SENSORS
            vlan_id: 300
            traffic_type: DATA
            fabric_enabled_wireless: true
            associated_l3_virtual_network_name: IOT_VN
          - name: GUEST_L2_VN
            vlan_name: GUEST_ACCESS
            vlan_id: 400
            traffic_type: DATA
            fabric_enabled_wireless: true
```

Example-4: Layer 2 Virtual Network for Voice Traffic

This example shows how to configure a Layer 2 virtual network specifically optimized for voice traffic with appropriate QoS treatment and priority handling within the SD-Access fabric.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Asia Pacific/CallCenter
        authentication_template:
          name: Closed Authentication
        l2_virtual_networks:
          - name: VOICE_L2_VN
            vlan_name: VOICE_TRAFFIC
            vlan_id: 150
            traffic_type: VOICE
            fabric_enabled_wireless: true
```


Example-5: Layer 2 Virtual Network for Legacy System Integration

This example shows how to configure Layer 2 virtual networks for integrating legacy systems that require specific VLAN configurations and Layer 2 adjacency within the modern SD-Access fabric infrastructure.

```yaml
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Europe/Legacy_Data_Center
        authentication_template:
          name: Closed Authentication
        l2_virtual_networks:
          - name: LEGACY_MAINFRAME_L2_VN
            vlan_name: MAINFRAME_ACCESS
            vlan_id: 999
            traffic_type: DATA
            fabric_enabled_wireless: false
          - name: LEGACY_STORAGE_L2_VN
            vlan_name: STORAGE_NETWORK
            vlan_id: 998
            traffic_type: DATA
            fabric_enabled_wireless: false
```
