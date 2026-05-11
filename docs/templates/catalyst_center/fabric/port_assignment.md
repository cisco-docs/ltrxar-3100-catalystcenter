# Port Assignment

*Location in GUI*:
`Provision` » `SD-Access` » `Fabric Sites` » `[Site Name]` » `Port Assignment`

{{ doc_gen }}

Port Assignments define how physical switch ports on fabric edge nodes connect endpoints to the SD-Access fabric. Each assignment specifies the connected device type, [Anycast Gateway](/docs/data_models/catalyst_center/fabric/anycast_gateway) (data VLAN), voice VLAN, security group, and authentication template. Ports are assigned per device within a [Fabric Site](/docs/data_models/catalyst_center/fabric/fabric_site). This resource is **SDA fabric only**.

### Examples

Example-1: Single Interface Port Assignment

This example demonstrates how to configure a single port assignment on an SD-Access fabric edge node. Port assignments define how physical switch ports connect endpoints to the fabric, specifying the connected device type, VLAN assignment, security group, and authentication template.

```yaml
---
catalyst_center:
  inventory:
    devices:
      - name: EDGE01
        fqdn_name: EDGE01.cisco.eu
        device_ip: 198.18.130.1
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        fabric_site: Global/Poland/Krakow
        fabric_roles:
          - EDGE_NODE
        port_assignments:
          - interface_name: GigabitEthernet1/0/2
            interface_description: "User workstation port"
            connected_device_type: USER_DEVICE
            security_group_name: Employees
            data_vlan_name: "192_168_100_0-Campus"
            authenticate_template_name: "No Authentication"
```

Example-2: Interface Range Port Assignment

This example shows how to configure port assignments using an interface range, which allows applying the same configuration to multiple consecutive ports efficiently. This is useful for bulk provisioning of access ports.

The interface range format follows the pattern `InterfaceType<slot>/<module>/<start_port>-<slot>/<module>/<end_port>` (e.g., GigabitEthernet1/0/3-1/0/5 covers ports 3, 4, and 5).

```yaml
---
catalyst_center:
  inventory:
    devices:
      - name: EDGE02
        fqdn_name: EDGE02.cisco.eu
        device_ip: 198.18.130.2
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        fabric_site: Global/Poland/Krakow
        fabric_roles:
          - EDGE_NODE
        port_assignments:
          - interfaces_range: "GigabitEthernet1/0/3-1/0/5"
            interface_description: "Conference room ports"
            connected_device_type: USER_DEVICE
            security_group_name: Employees
            data_vlan_name: "192_168_100_0-Campus"
            authenticate_template_name: "No Authentication"
```

Example-3: Comprehensive Port Assignments

This example demonstrates a comprehensive port assignment configuration with multiple port types on a single edge device, including user devices with voice and data VLANs, access points, and trunking devices.

```yaml
---
catalyst_center:
  inventory:
    devices:
      - name: EDGE03
        fqdn_name: EDGE03.cisco.eu
        device_ip: 198.18.130.3
        state: PROVISION
        device_role: ACCESS
        site: Global/Enterprise/Building_C
        fabric_site: Global/Enterprise
        fabric_roles:
          - EDGE_NODE
        port_assignments:
          # User workstation ports with voice and data
          - interfaces_range: "GigabitEthernet1/0/1-1/0/20"
            interface_description: "User workstations - Floor 3"
            connected_device_type: USER_DEVICE
            data_vlan_name: "EMPLOYEES"
            voice_vlan_name: "VOICE"
            security_group_name: Employees
            authenticate_template_name: "Closed Authentication"
          # Access Point ports
          - interface_name: GigabitEthernet1/0/21
            interface_description: "Wireless AP - Floor 3"
            connected_device_type: ACCESS_POINT
            data_vlan_name: "AP_POOL"
            authenticate_template_name: "No Authentication"
          # Printer port
          - interface_name: GigabitEthernet1/0/23
            interface_description: "Network printer"
            connected_device_type: USER_DEVICE
            data_vlan_name: "PRINTERS"
            security_group_name: Printers
            authenticate_template_name: "Open Authentication"
          # Uplink to legacy switch
          - interface_name: GigabitEthernet1/0/24
            interface_description: "Legacy switch uplink"
            connected_device_type: TRUNKING_DEVICE
            data_vlan_name: "INFRASTRUCTURE"
            authenticate_template_name: "No Authentication"
```
