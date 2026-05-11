# Device

*Location in GUI*:
`Provision` » `Inventory`

{{ doc_gen }}

Devices represent the network equipment managed by Catalyst Center. The device data model defines inventory attributes, site assignment, provisioning parameters, and fabric roles. Devices must be discovered (via [Discovery](/docs/data_models/catalyst_center/inventory/discovery) or manual add), [assigned to a site](/docs/data_models/catalyst_center/inventory/assign_device_to_site), and provisioned before they can participate in the network. In SDA fabric deployments, devices are additionally assigned fabric roles (edge, border, control plane) for [Fabric Site](/docs/data_models/catalyst_center/fabric/fabric_site) participation. Applicable to both SDA fabric and non-fabric deployments.

## Device Provisioning States and Lifecycle

<figure markdown>
  ![](./img/provisioing_lifecycle.png)
</figure>

The device provisioning lifecycle in Catalyst Center follows a well-defined state machine that manages devices from initial discovery through full deployment and ongoing management. Understanding these states and their transitions is crucial for effective network automation and troubleshooting.

### Device States

#### **INIT (Initial State)**
The starting state for all devices when first added to the inventory. Devices in this state are discovered but not yet assigned to any site or configured for provisioning.

**Characteristics:**
- Device is discovered and added to inventory
- No site assignment
- No configuration applied
- Basic device information collected (IP, serial number, PID)

**Possible Transitions:**
- **To ASSIGN**: Assign device to a specific site for configuration
- **To PROVISION**: Begin provisioning process for non-fabric devices as well fabric provisioning, if fabric attributes specified

#### **PNP (Plug and Play)**
Devices in this state are ready for zero-touch provisioning when they boot up and contact the Catalyst Center. This state is typically used for new devices that will be deployed in remote locations.

**Characteristics:**
- Device prepared for zero-touch deployment
- Configuration templates pre-assigned
- Waiting for device to contact Catalyst Center
- No active management until device boots

**Possible Transitions:**
- **To PROVISION**: Begin provisioning process for non-fabric devices as well fabric provisioning, if fabric attributes specified
- **To INIT**: Keep device in Inventory "as is" after PNP process
- **ASSIGN**: Assign device to a specific site

#### **ASSIGN**
Devices are assigned to a specific site but not yet provisioned with configuration. This state allows for site-specific settings preparation before actual provisioning.

**Characteristics:**
- Device assigned to a site hierarchy
- Site-specific credentials and settings applied
- Ready for provisioning process
- Configuration templates can be assigned

**Possible Transitions:**
- **To PROVISION**: Begin provisioning process for non-fabric devices as well fabric provisioning, if fabric attributes specified
- **To INIT**: Un-assign device from site

#### **PROVISION**
The active provisioning state where devices receive their full configuration and become operational network elements. This is the target state for most production devices.

**Characteristics:**
- Full configuration deployment in progress or completed
- Device actively managed by Catalyst Center
- Templates applied and configuration synchronized
- Monitoring and compliance checking active
- Fabric roles assigned (if applicable)

**Possible Transitions:**
- **To REPROVISION**: When configuration changes require redeployment
- **To INIT**: Unprovision device completely (removes from SDA fabric and/or Inventory with config clearing)

#### **REPROVISION**
A specialized state for devices that need `Network Settings` configuration updates. This state ensures network settings are refreshed while maintaining device operational status.

**Characteristics:**
- Device remains operational during re-provisioning
- Configuration templates reapplied
- Network settings updated every time
- Maintains existing fabric membership and site assignment

**Possible Transitions:**
- **To PROVISION**: Return to standard provisioned state after updates complete
- **To INIT**: Unprovision device completely (removes from SDA fabric and/or Inventory with config clearing)

### State Transition Operations

#### **Provisioning Operations**
- **Provision non-fabric devices**: Apply standard network configuration
- **Provision fabric devices**: Apply SDA fabric configuration and assign fabric roles
- Both operations move devices from INIT, ASSIGN or PNP states to PROVISION state

#### **Unprovisioning Operations**
- **Standard Unprovisioning**: Removes device from Inventory management with configuration clearing
- **SDA Fabric Removal**: Removes from both SDA fabric and Inventory with configuration clearing

### Best Practices

#### **State Management**
- Use **ASSIGN** state for devices requiring site-specific preparation
- Use **PNP** state for zero-touch deployment scenarios
- Monitor devices in **REPROVISION** state for completion

#### **Operational Considerations**
- Devices in **PROVISION** state should be monitored for compliance
- **REPROVISION** operations should be scheduled during maintenance windows
- Use proper unprovisioning procedures to avoid configuration conflicts
- Maintain device inventory accuracy across all states

### Examples

Example-1: SD-Access Border Router Device Configuration

This example demonstrates how to configure a border router device in Catalyst Center inventory with SD-Access fabric capabilities. Border routers serve as critical infrastructure components that connect the SD-Access fabric to external networks and provide advanced routing and policy enforcement functions.

The border router device configuration includes:
* Device name (BR01) for identification and inventory management
* Management IP address (192.168.10.1) for device communication and monitoring
* PROVISION state for active deployment and configuration management
* Border router role designation for network function
* Site assignment (Global/Canada) for geographic and organizational placement
* Fabric site association (Global/Canada) for SD-Access fabric membership
* Multiple fabric roles including BORDER_NODE for external connectivity and CONTROL_PLANE_NODE for fabric control plane operations

```yaml
catalyst_center:
  inventory:
    devices:
      - name: BR01
        fqdn_name: BR01.company.local
        device_ip: 192.168.10.1
        state: PROVISION
        device_role: BORDER ROUTER
        site: Global/Canada
        fabric_site: Global/Canada
        fabric_roles:
          - BORDER_NODE
          - CONTROL_PLANE_NODE
```

Example-2: Access Switch with Edge Node Functionality

This example shows how to configure an access layer switch with SD-Access edge node capabilities for endpoint connectivity and policy enforcement at the network edge.

```yaml
catalyst_center:
  inventory:
    devices:
      - name: ACCESS-SW01
        fqdn_name: ACCESS-SW01.company.local
        device_ip: 192.168.20.10
        serial_number: FOC2644021A
        pid: C9300-24P
        state: PROVISION
        device_role: ACCESS
        site: Global/North America/Campus/Building A/Floor 1
        fabric_site: Global/North America/Campus
        fabric_roles:
          - EDGE_NODE
        tags:
          - FLOOR1_DEVICES
          - EMPLOYEE_ACCESS
```

Example-3: Plug-n-Play Functionality

This example shows how to configure a device to be on-boarded into Catalyst Center inventory using plug and play.

`Note` : The below assumes that a day zero on-boarding template named `PNP_Template` has already be provisioned using the data model. The `PNP_Template` during the PNP process, switches the device's https source-interface to the device's desired management interface IP address.

```yaml
catalyst_center:
  inventory:
    devices:
      - name: PNP_DEVICE
        fqdn_name: PNP_DEVICE.cisco.eu
        device_ip: 192.158.142.20
        serial_number: FAB12345602
        pid: C9300-48P
        state: PNP
        device_role: BORDER ROUTER
        site: Global/Poland/Krakow/Bld A
        onboarding_template:
          name: PNP_Template
          variables:
            - name: device_host_name
              value: PNP_DEVICE
            - name: infra_vlan
              value: "100"
            - name: infra_vlan_network_add
              value: 181.1.1.90
            - name: infra_vlan_network_mask
              value: 255.255.255.248
            - name: loopback_0_IP
              value: 192.158.142.20
            - name: loopback_0_mask
              value: 255.255.255.255
            - name: Border_AS
              value: "65005"
            - name: peer_BGP_neigbor
              value: 181.1.1.89
            - name: peer_AS
              value: "65002"
            - name: peer_interface
              value: GigabitEthernet1/0/1
```

After the plug and play process is completed, the device state can be updated to `PROVISION` to enable full management and configuration capabilities within Catalyst Center.

```yaml
catalyst_center:
  inventory:
    devices:
      - name: PNP_DEVICE
        fqdn_name: PNP_DEVICE.cisco.eu
        device_ip: 192.158.142.20
        serial_number: FAB12345602
        pid: C9300-48P
        state: PROVISION
        device_role: BORDER ROUTER
        site: Global/Poland/Krakow/Bld A

```

Example-4: Access Point Plug-n-Play

This example shows how to configure an Access Point to be on-boarded into Catalyst Center inventory using plug and play.

`Note` : It is mandatory to provide the `type` as `AccessPoint`, `rf_profile`, and `site` in order to add and claim the device in Provision -> Plug and Play

```yaml
catalyst_center:
  inventory:
    devices:
      - name: AP_PNP
        fqdn_name: AP_PNP.cisco.eu
        pid: C9136I-E
        serial_number: FGL3727MF6Y
        state: PNP
        type: AccessPoint
        rf_profile: TYPICAL
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A/FLOOR_2
```

After the plug and play process is completed, the Access Point can be updated to `PROVISION` to provision full management and configuration capabilities within Catalyst Center.

```yaml
catalyst_center:
  inventory:
    devices:
      - name: AP_PNP
        fqdn_name: AP_PNP.cisco.eu
        pid: C9136I-E
        serial_number: FGL3727MF6Y
        state: PROVISION
        type: AccessPoint
        rf_profile: TYPICAL
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A/FLOOR_2
```


Example-5: Embedded Wireless Controller provisioning

This example demonstrates how to enable the fabric Embedded Wireless Controller (EWC) role within a fabric site

`Note` :

* It is mandatory to provide the `fabric_role` as `EMBEDDED_WIRELESS_CONTROLLER_NODE` (in addition to the existing role(s) - `EDGE`, `BORDER`)
* It is also required to populate the `primary_managed_ap_locations` field to specify the primary location(s) for managed access points (APs)

```yaml
catalyst_center:
  inventory:
    devices:
      - name: P3-EN1
        fqdn_name: P3-EN1.cisco.eu
        device_ip: 192.168.30.24
        pid: C9300-24P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
        fabric_site: Global/Poland/Krakow
        fabric_roles:
          - EDGE_NODE
          - EMBEDDED_WIRELESS_CONTROLLER_NODE
        primary_managed_ap_locations:
          - Global/Poland/Krakow/Bld A/FLOOR_2
          - Global/Poland/Krakow/Bld A/FLOOR_1
```

Example-6: Management IP Address Update

This example demonstrates how to update the management IP address of an existing device. When the `device_ip` in the data model differs from the device's current management IP in Catalyst Center, the module automatically triggers a management address update. The device must be identifiable by its `name` or `fqdn_name` (hostname match against Catalyst Center inventory).

> **Note**: This resource uses an ephemeral approach: it only appears in Terraform state when `device_ip` differs from the current Catalyst Center management IP. After a successful apply, the next apply will detect the IPs match, automatically remove the resource from state, and make no further changes. This means zero state footprint when IPs are in sync. This feature does not apply to Access Points (`type: AccessPoint`).

```yaml
catalyst_center:
  inventory:
    devices:
      - name: SW-CORE-01
        fqdn_name: SW-CORE-01.company.local
        device_ip: 10.1.1.100        # new management IP (was 10.1.1.10)
        state: PROVISION
        device_role: CORE
        site: Global/HQ/DataCenter
```

Example-7: Device Unprovisioning with `clean_up_config`

When unprovisioning a device (transitioning from `PROVISION` to `INIT`), Catalyst Center attempts to connect to the device and remove its configuration. However, if the device is unreachable (e.g. hardware failure, network outage, or the device has already been physically removed), the unprovisioning will fail because Catalyst Center cannot clean the configuration.

The `clean_up_config: false` flag instructs Catalyst Center to skip the configuration cleanup step, allowing the device to be deleted from inventory even when it is unreachable or error-free cleanup is not possible.

> **Important**: This is a two-step process:
>
> 1. **First `terraform apply`**: Set `clean_up_config: false` on the device while it is still in `PROVISION` state. This tells Catalyst Center to skip configuration cleanup on the next state change.
> 2. **Second `terraform apply`**: Change the device state to `INIT` (unprovision). Because `clean_up_config` was already set to `false`, Catalyst Center will remove the device without attempting to reach it.

**Step 1** — Set `clean_up_config: false` on the unreachable device:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: SW-UNREACHABLE-01
        fqdn_name: SW-UNREACHABLE-01.company.local
        device_ip: 10.1.1.50
        state: PROVISION
        device_role: ACCESS
        site: Global/HQ/Building A/Floor 1
        clean_up_config: false
```

Run `terraform apply` to register the flag with Catalyst Center.

**Step 2** — Unprovision the device by setting `state: INIT`:

```yaml
catalyst_center:
  inventory:
    devices:
      - name: SW-UNREACHABLE-01
        fqdn_name: SW-UNREACHABLE-01.company.local
        device_ip: 10.1.1.50
        state: INIT
        device_role: ACCESS
        site: Global/HQ/Building A/Floor 1
        clean_up_config: false
```

Run `terraform apply` again. Catalyst Center will remove the device from inventory without attempting to clean its configuration.

#### Setting `clean_up_config` globally via `defaults.yaml`

If you have multiple unreachable devices or want to apply this flag to all devices by default, you can set it in the `defaults.yaml` file instead of on each individual device:

```yaml
defaults:
  catalyst_center:
    inventory:
      devices:
        clean_up_config: false
```

When set in `defaults.yaml`, the flag applies to **all** devices that do not explicitly override it. Individual devices can still override the default by setting `clean_up_config: true` at the device level.

Example-8: RMA (Return Material Authorization) Device Replacement

This example demonstrates how to replace a faulty device using the RMA workflow. The process uses the `state` and `serial_number` attributes to coordinate with Catalyst Center's device replacement API. The replacement is a **2-step process** requiring two separate `terraform apply` runs.

**Prerequisites:**

* The faulty device must be **unreachable** in Catalyst Center
* The replacement device must be **physically connected** and reachable by Catalyst Center
* The device must have `serial_number` defined in the data model

> **How it works:** The module uses a `data.catalystcenter_device_replacement` data source to query Catalyst Center's device replacement API for the device. When the device is in `MARK_FOR_REPLACEMENT` state (Step 1), the module marks it for replacement via the API. When the device transitions back to `PROVISION` state with a new `serial_number` (Step 2), the module detects that the YAML serial number differs from the `faulty_device_serial_number` reported by the replacement API entry (created in Step 1), and triggers the replacement workflow. The faulty device's serial number is resolved from the replacement API entry. The user only provides the new replacement serial number.

**Step 1** — Mark the faulty device for replacement:

Change the device `state` from `PROVISION` to `MARK_FOR_REPLACEMENT`. All existing device resources (provisioning, fabric roles, templates, port assignments) remain untouched during this step.

```yaml
catalyst_center:
  inventory:
    devices:
      - name: SW-ACCESS-01
        fqdn_name: SW-ACCESS-01.company.local
        device_ip: 10.1.1.20
        pid: C9300-24P
        serial_number: FOC12345678
        state: MARK_FOR_REPLACEMENT
        device_role: ACCESS
        site: Global/HQ/Building A/Floor 1
        fabric_site: Global/HQ
        fabric_roles:
          - EDGE_NODE
```

Run `terraform apply`. Catalyst Center marks the device for replacement.

**Step 2** — Trigger the replacement with the new device's serial number:

Update `serial_number` to the replacement device's serial number and change `state` back to `PROVISION`.

```yaml
catalyst_center:
  inventory:
    devices:
      - name: SW-ACCESS-01
        fqdn_name: SW-ACCESS-01.company.local
        device_ip: 10.1.1.20
        pid: C9300-24P
        serial_number: FOC87654321
        state: PROVISION
        device_role: ACCESS
        site: Global/HQ/Building A/Floor 1
        fabric_site: Global/HQ
        fabric_roles:
          - EDGE_NODE
```

Run `terraform apply`. The module triggers the Catalyst Center RMA workflow, which transfers the configuration from the faulty device to the replacement device. The replacement workflow runs asynchronously in Catalyst Center.

**Convergence:** After Step 2, run `terraform apply` periodically. Once Catalyst Center finishes the replacement and updates its inventory to show the new device, the `catalystcenter_device_replacement_workflow.rma` resource will be removed from the Terraform plan. The `catalystcenter_device_replacement.mark` resource remains in Terraform state as a record of the completed replacement. The final result is a stable state with the device provisioned under the new serial number.

> **Note**: The RMA process is fully repeatable. After the workflow completes and Terraform reaches a stable state, the same 2-step process can be used again for any future replacement of the same device.
