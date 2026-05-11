# Assign Device To Site

*Location in GUI*:
`Provision` » `Inventory` » Select Device » `Actions` » `Provision` » `Assign Device to Site`

{{ doc_gen }}

Device Site Assignment associates a discovered [Device](/docs/data_models/catalyst_center/inventory/device) with a specific location in the site hierarchy ([Area](/docs/data_models/catalyst_center/sites/area), [Building](/docs/data_models/catalyst_center/sites/building), or [Floor](/docs/data_models/catalyst_center/sites/floor)). This is a prerequisite for device provisioning and determines which network settings, credentials, and policies are applied to the device. Applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic Device Site Assignment

This example demonstrates how to assign a network device to a specific site in Catalyst Center inventory management. Device site assignment is a critical step in the provisioning workflow that establishes the geographic and logical location of devices within the network hierarchy.

The device site assignment includes:
* Device identification using name (EDGE02) and fqdn_name (EDGE02.cisco.eu) for inventory tracking
* Device IP address (198.18.130.2) for management connectivity and communication
* Product ID (C9KV-UADP-8P) for hardware identification and capability determination
* State change from INIT to ASSIGN to trigger the site assignment process
* Device role specification (ACCESS) for network function and policy application
* Site hierarchy assignment (Global/Poland/Krakow/Bld A) for geographic and organizational placement
* Foundation for subsequent provisioning and configuration deployment workflows

```yaml
---
catalyst_center:
  inventory:
    devices:
      - name: EDGE02
        fqdn_name: EDGE02.cisco.eu
        device_ip: 198.18.130.2
        pid: C9KV-UADP-8P
        state: ASSIGN
        device_role: ACCESS
        site: Global/Poland/Krakow/Bld A
```

Example-2: Multiple Device Site Assignments Across Different Locations

This example shows how to assign multiple network devices to different sites simultaneously, enabling bulk site assignment operations for distributed network deployments across various geographic locations.

```yaml
---
catalyst_center:
  inventory:
    devices:
      - name: CORE01
        fqdn_name: CORE01.hq.company.com
        device_ip: 10.1.1.10
        pid: C9500-40X
        state: ASSIGN
        device_role: CORE
        site: Global/North America/Headquarters/Data Center
      - name: DIST01.branch.company.com
        fqdn_name: DIST01.branch.company.com
        device_ip: 10.2.1.10
        pid: C9300-48P
        state: ASSIGN
        device_role: DISTRIBUTION
        site: Global/Europe/Branch Offices/London Office
      - name: ACCESS01.remote.company.com
        fqdn_name: ACCESS01.remote.company.com
        device_ip: 10.3.1.10
        pid: C9200-24P
        state: ASSIGN
        device_role: ACCESS
        site: Global/Asia Pacific/Remote Sites/Tokyo Branch
```

Example-3: Fabric-Enabled Device Site Assignment

This example demonstrates how to assign fabric-enabled devices to sites with specific fabric roles and configurations, suitable for SD-Access deployments requiring fabric node designation and policy enforcement.

```yaml
---
catalyst_center:
  inventory:
    devices:
      - name: FABRIC-BORDER01
        fqdn_name: FABRIC-BORDER01.sda.local
        device_ip: 192.168.10.10
        pid: C9500-40X
        state: ASSIGN
        device_role: BORDER_NODE
        site: Global/Campus/Main Building/Network Closet
        fabric_site: Global/Campus/Main Building
        fabric_roles:
          - BORDER_NODE
      - name: FABRIC-EDGE01
        fqdn_name: FABRIC-EDGE01.sda.local
        device_ip: 192.168.20.10
        pid: C9300-24P
        state: ASSIGN
        device_role: ACCESS
        site: Global/Campus/Building A/Floor 1
        fabric_site: Global/Campus/Building A
        fabric_roles:
          - EDGE_NODE
```

Example-4: Wireless Controller Site Assignment

`Note`: As a pre-requisite for WLC assignment or provisioning, Ensure to create a Wireless network profile which has the sites used in the `managed_ap_locations`

This example shows how to assign wireless controllers to sites with specific wireless management roles and coverage areas, enabling centralized wireless network management and policy distribution.

```yaml
---
catalyst_center:
  inventory:
    devices:
      - name: WLC01
        fqdn_name: WLC01.wireless.company.com
        device_ip: 172.16.1.100
        pid: C9800-80
        state: ASSIGN
        device_role: WIRELESS_CONTROLLER
        site: Global/CorporateCampus/Network_Operations_Center
        primary_managed_ap_locations:
          - Global/CorporateCampus/Network_Operations_Center


      - name: WLC02
        fqdn_name: WLC02.branch.company.com
        device_ip: 172.16.2.100
        pid: C9800-40
        state: ASSIGN
        device_role: WIRELESS_CONTROLLER
        site: Global/Regional Offices/West_Coast_Hub
        primary_managed_ap_locations:
          - Global/Regional Offices/West_Coast_Hub/BLD1
        secondary_managed_ap_locations
          - Global/Regional Offices/West_Coast_Hub/BLD2
```
