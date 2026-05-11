# Border Device

*Location in GUI*:
`Provision` » `SD-Access` » `Fabric Sites` » `Fabric Infrastructure`

{{ doc_gen }}

Border Devices connect the SD-Access fabric to external networks. They are provisioned within a [Fabric Site](/docs/data_models/catalyst_center/fabric/fabric_site) and support [Layer 3 Handoffs](/docs/data_models/catalyst_center/fabric/layer_3_handoff) (IP transit, SDA transit) and [Layer 2 Handoffs](/docs/data_models/catalyst_center/fabric/layer_2_handoff) for routing between fabric virtual networks and external infrastructure. The device must first be defined in the [Inventory](/docs/data_models/catalyst_center/inventory/device) data model with the appropriate fabric role. This resource is **SDA fabric only**.

### Examples


**Prerequisite**: To provision a border device, it must be specified under `Inventory` » `Devices` data model with fabric-role element values assigned [link](/docs/data_models/catalyst_center/inventory/device)

The `border_devices` name must match the name specified in the inventory data model for the specific device (inventory.devices.name)

Example-1: Layer 3 Border Device with BGP External Connectivity - LISP External Border Role

This example demonstrates how to configure a Layer 3 border device in SD-Access fabric for external network connectivity. Border devices serve as critical infrastructure components that connect the SD-Access fabric to external networks, providing routing, policy enforcement, and traffic ingress/egress capabilities.

The border device configuration includes:
* Device name (BR01) referencing a device previously configured in the inventory
* Layer 3 border type enabling IP routing and external connectivity functions
* Default exit configuration making this border the primary path for external traffic
* External route import disabled for controlled routing policy and security
* Local ASN (65013) for BGP peering and autonomous system identification
* BGP external domain routing protocol for dynamic route exchange with external networks
* ASN prepending (count: 1) for traffic engineering and path preference control
* Border priority (5) for load balancing and redundancy across multiple border devices

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BR01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65013
        external_domain_routing_protocol_name: BGP
        prepend_autonomous_system_count: 1
        border_priority: 5
```



Example-2: Layer 3 Border Device with BGP External Connectivity - LISP (External + Internal) Border Role

This example shows how to configure a border device with external route import capabilities for scenarios requiring dynamic route propagation from external networks into the SD-Access fabric.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BORDER-CORE-01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: true
        local_autonomous_system_number: 65100
        prepend_autonomous_system_count: 1
        border_priority: 5
```


Example-3: Layer 3 Border Device with Route Import - LISP (Internal) only Border Role

This example shows how to configure a border device with external route import capabilities for scenarios requiring dynamic route propagation from external networks into the SD-Access fabric.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: BORDER-CORE-01
        border_types:
          - LAYER_3
        default_exit: false
        import_external_routes: true
        local_autonomous_system_number: 65100
        prepend_autonomous_system_count: 1
        border_priority: 5
```


Example-4: Layer 2 Border Device for Campus Integration

This example demonstrates how to configure a Layer-2 only border device for campus environments where Layer 2 extension and VLAN bridging are required between the fabric and external networks.
Ensure the Fabric has an Existing Control-Plane device, before adding a LAYER_2 only Border

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: L2-BORDER-SW01
        l2_handoffs:
          l2_without_anycast_gateway:
            vlans:
              - name: L2_VLAN_USERS
                external_vlan: 550
            interfaces:
              - GigabitEthernet1/0/10
          l2_with_anycast_gateway:
            - l3_virtual_network: SDA_VN_USERS
              ip_pool_name: USERS
              external_vlan: 470
              interfaces:
                - GigabitEthernet1/0/8
```

Example-5: Multi-Border Device Configuration for High Availability

This example shows how to configure multiple Layer-3 only border devices for high availability and load distribution in large enterprise SD-Access deployments with redundant external connectivity.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: PRIMARY-BORDER-01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65200
        prepend_autonomous_system_count: 1
        border_priority: 5

      - name: SECONDARY-BORDER-01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65200
        prepend_autonomous_system_count: 1
        border_priority: 5

```

Example-6: Hybrid Border Device with Layer 2 and Layer 3 Functions

This example demonstrates how to configure a border device supporting both Layer 2 and Layer 3 border functions for complex network scenarios requiring multiple connectivity types and traffic handling capabilities.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: HYBRID-BORDER-01
        border_types:
          - LAYER_3
          - LAYER_2
        default_exit: true
        import_external_routes: false
        local_autonomous_system_number: 65300
        prepend_autonomous_system_count: 1
        affinity_id_prime: 100
        affinity_id_decider: 100
        connected_to_internet: true
        border_priority: 9
        sda_transit: TRANSIT_CONTROL_PLANE_GROUP1
```

Example-7: Border Device with SDA Transit and Multicast Over Transit

This example demonstrates how to configure a border device connected to an SDA transit network with native multicast enabled across multiple sites.

```yaml
catalyst_center:
  fabric:
    border_devices:
      - name: MULTISITE-BORDER-01
        border_types:
          - LAYER_3
        default_exit: true
        import_external_routes: true
        local_autonomous_system_number: 65400
        prepend_autonomous_system_count: 1
        border_priority: 5
        affinity_id_prime: 50
        affinity_id_decider: 50
        connected_to_internet: false
        sda_transit: SDA_MULTISITE_TRANSIT
        multicast_over_transit: true
```
