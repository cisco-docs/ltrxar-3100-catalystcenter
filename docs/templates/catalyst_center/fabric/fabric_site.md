# Fabric Site

*Location in GUI*:
`Provision` » `SD-Access` » `Fabric Sites`

{{ doc_gen }}

Fabric Sites define the SD-Access fabric boundary within the site hierarchy. Enabling a site as a fabric site activates Software-Defined Access functionality including micro-segmentation, policy enforcement, and automated underlay/overlay provisioning. Fabric sites contain [Border Devices](/docs/data_models/catalyst_center/fabric/border_device), [Virtual Networks](/docs/data_models/catalyst_center/fabric/layer_3_virtual_network), [Anycast Gateways](/docs/data_models/catalyst_center/fabric/anycast_gateway), and [Port Assignments](/docs/data_models/catalyst_center/fabric/port_assignment). This resource is **SDA fabric only**.

### Examples

Example-1: Basic Fabric Site with No Authentication

This example demonstrates how to configure a basic SD-Access fabric site in Catalyst Center with no authentication requirements. Fabric sites enable Software-Defined Access functionality within designated network areas, providing centralized policy enforcement and micro-segmentation capabilities.

The fabric site configuration includes:
* Site hierarchy specification (Global/Canada) for geographic and organizational structure
* Authentication template assignment (No Authentication) for simplified initial deployment
* Foundation for SD-Access fabric enablement without immediate authentication requirements
* Base configuration suitable for proof-of-concept or laboratory environments

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Canada
        authentication_template:
          name: No Authentication
        pub_sub_enabled: true

```

Example-2: Campus Fabric Site with Closed Authentication

This example demonstrates how to configure a campus fabric site with closed authentication mode for high-security environments where all network access requires explicit authentication and authorization.

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Canada
        authentication_template:
          name: Closed Authentication
        pub_sub_enabled: true

```

Example-3: Multi-Site Fabric Deployment

This example shows how to configure multiple fabric sites across different geographic locations, each with appropriate authentication templates based on local security requirements and organizational policies.

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/North_America/New_York_Office
        authentication_template:
          name: Closed Authentication
        pub_sub_enabled: true


      - name: Global/Asia_Pacific/Tokyo_Branch
        authentication_template:
          name: Open Authentication
        pub_sub_enabled: true

      - name: Global/Europe/London_Office
        authentication_template:
          name: Low Impact
        pub_sub_enabled: true


      - name: Global/Americas/Mexico_City_Branch
        authentication_template:
          name: No Authentication
        pub_sub_enabled: true

```

Example-4: Fabric Site custom authentication template

This example demonstrates how to configure a fabric site with custom options for authentication templates

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Corporate/London_Office
        authentication_template:
          name: Closed Authentication
          dot1x_to_mab_fallback_timeout: 30
          wake_on_lan: false
          number_of_hosts: Unlimited
          authentication_order: dot1x
          bpdu_guard: false
        pub_sub_enabled: true


     - name: Global/Corporate/Tokyo_Branch
        authentication_template:
        authentication_template:
          name: Low Impact
          dot1x_to_mab_fallback_timeout: 30
          wake_on_lan: false
          number_of_hosts: Unlimited
          authentication_order: mac
          bpdu_guard: false
          pre_auth_acl:
            enabled: true
            implicit_action: PERMIT
            access_contracts:
              - action: PERMIT
                port: domain
                protocol: UDP
              - action: PERMIT
                port: bootpc
                protocol: UDP
              - action: PERMIT
                port: bootps
                protocol: UDP
        pub_sub_enabled: true

```

Example-5: Fabric Site configuration with fabric zones

This example demonstrates how to configure a fabric site that has a fabric zone


:::caution
In the devices yaml file, the Edge device that will be part of the fabric zone, is configured with a fabric_zone element matching the fabric zone name
:::

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Bytom
        authentication_template:
          name: Closed Authentication
          dot1x_to_mab_fallback_timeout: 30
          wake_on_lan: false
          number_of_hosts: Unlimited
          authentication_order: dot1x
        pub_sub_enabled: false
        l2_virtual_networks:
          - name: L2_SDA_VN_1
            vlan_name: L2_VLAN_USERS
            vlan_id: 455
            traffic_type: DATA
            fabric_enabled_wireless: false
          - name: L2_VN
            vlan_name: L2VN_VLAN
            traffic_type: DATA
            fabric_enabled_wireless: false
        l3_virtual_networks:
          - SDA_VN_USERS
          - SDA_VN_PRINTERS
          - SDA_VN_CORPORATE
          - INFRA_VN
        anycast_gateways:
          - ip_pool_name: Campus
            vlan_name: Campus_VLAN
            traffic_type: DATA
            l3_virtual_network: SDA_VN_USERS
            wireless_pool: true
          - ip_pool_name: Voice
            vlan_name: Voice_VLAN
            vlan_id: 224
            traffic_type: VOICE
            l3_virtual_network: SDA_VN_USERS
          - ip_pool_name: AP
            pool_type: FABRIC_AP
            vlan_name: AP_VLAN
            vlan_id: 225
            traffic_type: DATA
            l3_virtual_network: INFRA_VN

        fabric_zones:
          - name: Global/Poland/Bytom/Bld_B
            authentication_template:
              name: No Authentication
            l3_virtual_networks:
              - SDA_VN_USERS
            l2_virtual_networks:
              - L2_SDA_VN_1
            anycast_gateways:
              - Campus


  inventory:
    devices:
      - name: LAN-EN2
        fqdn_name: LAN-EN2.cisco.eu
        device_ip: 181.1.1.43
        pid: C9KV-UADP-8P
        state: PROVISION
        device_role: ACCESS
        site: Global/Poland/Bytom/Bld_B
        fabric_zone: Global/Poland/Bytom/Bld_B
        fabric_roles:
          - EDGE_NODE
````

Example-6: Fabric Site Reconfiguration

When the IPv4 pool used by a Fabric site is modified, for example when DHCP or DNS server information is updated, the Fabric becomes out of date. The site must be re-provisioned so that the changes take effect.

Cisco Catalyst Center displays a warning on the Fabric site indicating that a reconfiguration is required.

:::caution
You modified the IP pools used by this Fabric. The Fabric is now out of date. To update, select Reconfigure Fabric. The update time depends on the number of devices.
To trigger the reconfiguration through the Data Model, add the field "reconfigure: true" under the Fabric site configuration.
:::


```yaml

---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Poland/Krakow
        reconfigure: true
```
