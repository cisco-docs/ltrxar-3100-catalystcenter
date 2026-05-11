# Transit

*Location in GUI*:
`Provision` » `SD-Access` » `Transits`

{{ doc_gen }}

Transits enable connectivity between SD-Access fabric sites or between a fabric site and external networks. Supported types include IP-based transits (over existing IP/WAN infrastructure) and SDA transits (LISP Pub/Sub or LISP BGP for native fabric-to-fabric connectivity with control plane devices). Transits are referenced by [Layer 3 Handoffs](/docs/data_models/catalyst_center/fabric/layer_3_handoff) on [Border Devices](/docs/data_models/catalyst_center/fabric/border_device). This resource is **SDA fabric only**.

### Examples

Example-1: IP-Based Transit Configuration

This example demonstrates how to configure an IP-based transit for connecting SD-Access fabric sites across traditional IP networks. IP-based transits enable fabric-to-fabric connectivity over existing IP infrastructure without requiring dedicated LISP control plane devices, making them suitable for WAN connectivity and inter-site communication.

The IP-based transit configuration includes:
* Transit name (IP_TRANSIT) for identification and policy assignment
* Transit type (IP_BASED_TRANSIT) specifying traditional IP routing approach
* BGP routing protocol for dynamic route exchange and path selection
* Autonomous System Number (65100) for BGP peering and routing policy
* Simple deployment model suitable for existing IP network infrastructure

```yaml
catalyst_center:
  fabric:
    transits:
      - name: IP_TRANSIT
        type: IP_BASED_TRANSIT
        routing_protocol_name: BGP
        autonomous_system_number: 65100
```

Example-2: SD-Access LISP PUB SUB Transit Configuration

This example shows how to configure an SD-Access LISP BGP transit for native fabric-to-fabric connectivity with full LISP overlay support. SDA transits provide optimized inter-fabric communication with centralized control plane services and advanced SD-Access features.

The SDA LISP PUB SUB transit configuration includes:
* Transit name (SDA_TRANSIT) for fabric interconnection
* Transit type (SDA_LISP_PUB_SUB_TRANSIT) for native SD-Access overlay connectivity
* Multicast support enabled for efficient multicast traffic distribution across fabrics
* Control plane device specification (CONTROL01.cisco.eu and CONTROL02.cisco.eu) for LISP services
* Advanced fabric services including policy propagation and mobility support

```yaml
catalyst_center:
  fabric:
    transits:
      - name: SDA_TRANSIT
        type: SDA_LISP_PUB_SUB_TRANSIT
        multicast_over_sda_transit: true
        control_plane_devices:
          - CONTROL01.cisco.eu
          - CONTROL02.cisco.eu
```

Example-3: Multiple IP-Based Transits for Different Regions

This example demonstrates how to configure multiple IP-based transits for connecting fabric sites across different geographic regions with region-specific routing policies and autonomous system numbers.

```yaml
catalyst_center:
  fabric:
    transits:
      - name: NORTH_AMERICA_TRANSIT
        type: IP_BASED_TRANSIT
        routing_protocol_name: BGP
        autonomous_system_number: 65001
      - name: EUROPE_TRANSIT
        type: IP_BASED_TRANSIT
        routing_protocol_name: BGP
        autonomous_system_number: 65002
      - name: ASIA_PACIFIC_TRANSIT
        type: IP_BASED_TRANSIT
        routing_protocol_name: BGP
        autonomous_system_number: 65003
```

Example-4: SDA Transit with Multiple Control Plane Devices

This example shows how to configure an SDA LISP BGP transit with multiple control plane devices for high availability and load distribution in large-scale fabric deployments.

```yaml
catalyst_center:
  fabric:
    transits:
      - name: ENTERPRISE_SDA_TRANSIT
        type: SDA_LISP_BGP_TRANSIT
        control_plane_devices:
          - CONTROL01.cisco.eu
          - CONTROL02.cisco.eu
```

Example-5: Hybrid Transit Configuration for Mixed Environments

This example demonstrates how to configure both IP-based and SDA transits within the same environment for supporting different connectivity requirements and migration scenarios.

```yaml
catalyst_center:
  fabric:
    transits:
      - name: LEGACY_IP_TRANSIT
        type: IP_BASED_TRANSIT
        routing_protocol_name: BGP
        autonomous_system_number: 65100

      - name: MODERN_SDA_TRANSIT
        type: SDA_LISP_PUB_SUB_TRANSIT
        multicast_over_sda_transit: true
        control_plane_devices:
          - CONTROL01.cisco.eu
          - CONTROL02.cisco.eu
```

Example-6: Service Provider SDA Transit Configuration

This example shows how to configure SDA transits for service provider environments with multicast support and multiple control plane devices for customer fabric interconnection.

```yaml
catalyst_center:
  fabric:
    transits:
      - name: SP_CUSTOMER_A_TRANSIT
        type: SDA_LISP_PUB_SUB_TRANSIT
        multicast_over_sda_transit: true
        control_plane_devices:
          - SP_CONTROL01.provider.net
          - SP_CONTROL02.provider.net

      - name: SP_CUSTOMER_B_TRANSIT
        type: SDA_LISP_PUB_SUB_TRANSIT
        multicast_over_sda_transit: false
        control_plane_devices:
          - SP_CONTROL03.provider.net
```

Example-7: Campus-to-Data Center Transit Configuration

This example demonstrates how to configure transits for connecting campus fabric sites to data center fabrics with appropriate routing protocols and control plane distribution.

```yaml
catalyst_center:
  fabric:
    transits:
      - name: CAMPUS_TO_DC_TRANSIT
        type: SDA_LISP_PUB_SUB_TRANSIT
        multicast_over_sda_transit: true
        control_plane_devices:
          - CAMPUS_CONTROL01.company.local
          - DC_CONTROL01.company.local

      - name: BRANCH_TO_DC_TRANSIT
        type: IP_BASED_TRANSIT
        routing_protocol_name: BGP
        autonomous_system_number: 65200
```
