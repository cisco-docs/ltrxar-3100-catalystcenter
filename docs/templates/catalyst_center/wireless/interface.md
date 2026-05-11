# Wireless Interface

*Location in GUI*:
`Design` » `Network Settings` » `Wireless` » `Interfaces`

{{ doc_gen }}

Wireless Interfaces define the VLAN-to-interface mappings on wireless controllers. They are used in **non-SDA-fabric** (traditional/FlexConnect) deployments and are referenced by [Wireless Network Profiles](/docs/data_models/catalyst_center/network_profiles/wireless_network_profiles) via the `interface_name` field in `ssid_details`. In SDA fabric deployments, VLAN mapping is handled by the fabric infrastructure and wireless interfaces are not needed.

### Examples

Example-1: Basic wireless interface configuration mapping a single GigabitEthernet interface to a management VLAN for wireless controller connectivity:

```yaml
catalyst_center:
  wireless:
    interfaces:
      - name: GigabitEthernet0/1
        vlan_id: 200
```

Example-2: Multiple wireless interfaces configuration for a wireless controller, demonstrating interface-to-VLAN mappings for management, guest, and corporate traffic segmentation:

```yaml
catalyst_center:
  wireless:
    interfaces:
      - name: GigabitEthernet0/1
        vlan_id: 200
      - name: GigabitEthernet0/2
        vlan_id: 201
      - name: GigabitEthernet1/0/1
        vlan_id: 100
```
