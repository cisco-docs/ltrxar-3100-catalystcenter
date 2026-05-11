# Anycast Gateway

*Location in GUI*:
`Provision` » `SD-Access` » `Virtual Networks` » `Anycast Gateways`

{{ doc_gen }}

Anycast Gateways provide distributed Layer 3 gateway services across the SD-Access fabric, enabling optimal traffic forwarding and seamless endpoint mobility. Each gateway is associated with a [Layer 3 Virtual Network](/docs/data_models/catalyst_center/fabric/layer_3_virtual_network) and an [IP Pool](/docs/data_models/catalyst_center/network_settings/ip_pool) reservation within a [Fabric Site](/docs/data_models/catalyst_center/fabric/fabric_site). Gateways support both wired and wireless traffic with configurable VLAN names, traffic types, and security groups. This resource is **SDA fabric only**.

### Examples

Example-1: SD-Access Fabric Site with Anycast Gateways

This example demonstrates how to configure anycast gateways within an SD-Access fabric site in Catalyst Center. Anycast gateways provide distributed Layer 3 gateway services across the fabric, enabling optimal traffic forwarding and seamless mobility for endpoints while maintaining consistent IP addressing and gateway redundancy.

The fabric site configuration includes:
* Fabric site name (Global/Canada) establishing the SD-Access fabric boundary and scope
* Authentication template (No Authentication) for simplified endpoint onboarding and testing scenarios
* Layer 3 virtual networks (SDA_VN_USERS, SDA_VN_PRINTERS, SDA_VN_CORPORATE, INFRA_VN) for network segmentation and policy enforcement
* Multiple anycast gateways providing distributed gateway services for different endpoint types
* VLAN associations with specific virtual networks for traffic classification and forwarding
* Wireless pool enablement for seamless wired and wireless endpoint mobility
* INFRA_VN pools consisting of Access point pool and Extended node pool

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Canada
        authentication_template:
          name: No Authentication
        pub_sub_enabled: true
        l3_virtual_networks:
          - SDA_VN_USERS
          - SDA_VN_PRINTERS
          - SDA_VN_CORPORATE
          - INFRA_VN
        anycast_gateways:
          - ip_pool_name: USERS
            vlan_name: VLAN_USERS
            vlan_id: 301
            traffic_type: DATA
            wireless_pool: true
            l3_virtual_network: SDA_VN_USERS
          - ip_pool_name: PRINTERS
            vlan_name: VLAN_PRINTERS
            vlan_id: 302
            traffic_type: DATA
            l3_virtual_network: SDA_VN_PRINTERS
          - ip_pool_name: CORPORATE
            vlan_name: VLAN_CORPORATE
            vlan_id: 303
            traffic_type: DATA
            l3_virtual_network: SDA_VN_CORPORATE
          - ip_pool_name: AP_POOL
            vlan_name: VLAN_AP
            pool_type: FABRIC_AP
            vlan_id: 304
            traffic_type: DATA
            l3_virtual_network: INFRA_VN
          - ip_pool_name: EXTENDED_NODE_POOL
            pool_type: EXTENDED_NODE
            vlan_name: VLAN_EXTENDED_NODE
            vlan_id: 305
            traffic_type: DATA
            l3_virtual_network: INFRA_VN
```

Example-2: IP Pool Configuration for Anycast Gateway Alignment

This example shows how to configure IP pools with reservations that align with anycast gateway `ip_pool_name`. The anycast gateway `ip_pool_name` must exactly match the IP pool reservation names to ensure proper subnet allocation and gateway addressing within the SD-Access fabric.

The IP pool configuration includes:
* Parent IP pool (IP_POOL) with IPv4 address space covering the entire fabric addressing scheme
* Specific subnet reservations matching anycast gateway names for proper association
* Prefix length specifications (/24) providing adequate address space for endpoint connectivity
* Subnet allocations ensuring non-overlapping address ranges across different virtual networks

```
---
catalyst_center:
  network_settings:
    ip_pools:
      - name: IP_POOL
        ip_address_space: IPv4
        ip_pool_cidr: 10.0.0.0/16
        ip_pools_reservations:
          - name: USERS
            prefix_length: 24
            subnet: 10.0.1.0
          - name: PRINTERS
            prefix_length: 24
            subnet: 10.0.2.0
          - name: CORPORATE
            prefix_length: 24
            subnet: 10.0.3.0
          - name: AP_POOL
            prefix_length: 24
            subnet: 10.0.4.0
          - name: EXTENDED_NODE_POOL
            prefix_length: 24
            subnet: 10.0.5.0
```

Example-3: Site IP Pool Assignment for Fabric Integration

 IP pool reservations must be explicitly associated with the fabric site and cannot rely on inheritance from parent sites.

 This example demonstrates how to assign IP pool reservations to the fabric site to enable proper anycast gateway functionality.

```yaml
---
catalyst_center:
  sites:
    areas:
      - name: Canada
        parent_name: Global
        ip_pools_reservations:
          - USERS
          - PRINTERS
          - CORPORATE
          - AP_POOL
          - EXTENDED_NODE_POOL
```

Example-4: Fabric Site with Voice and Data:

This example shows how to configure a fabric site with separate anycast gateways for voice, data, and guest traffic, demonstrating network segmentation requirements.

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Enterprise/Headquarters
        authentication_template:
          name: Closed Authentication
        pub_sub_enabled: true
        l3_virtual_networks:
          - SDA_VN_EMPLOYEES
          - SDA_VN_VOICE
          - SDA_VN_GUEST
          - INFRA_VN
        anycast_gateways:
          - ip_pool_name: EMPLOYEES
            vlan_name: VLAN_EMPLOYEES
            vlan_id: 100
            traffic_type: DATA
            wireless_pool: true
            l3_virtual_network: SDA_VN_EMPLOYEES
          - ip_pool_name: VOICE
            vlan_name: VLAN_VOICE
            vlan_id: 200
            traffic_type: VOICE
            wireless_pool: false
            l3_virtual_network: SDA_VN_VOICE
          - ip_pool_name: GUEST
            vlan_name: VLAN_GUEST
            vlan_id: 300
            traffic_type: DATA
            wireless_pool: true
            l3_virtual_network: SDA_VN_GUEST
          - ip_pool_name: AP_POOL
            vlan_name: VLAN_AP
            vlan_id: 400
            traffic_type: DATA
            pool_type: FABRIC_AP
            l3_virtual_network: INFRA_VN
          - ip_pool_name: EXTENDED_NODE_POOL
            pool_type: EXTENDED_NODE
            vlan_name: VLAN_EXTENDED_NODE
            vlan_id: 500
            traffic_type: DATA
            l3_virtual_network: INFRA_VN
```

Example-5: Multi-Site Fabric with Consistent Gateway Configuration:

This example demonstrates how to configure multiple fabric sites with consistent anycast gateway patterns for standardized deployment across distributed enterprise locations.

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/North_America/Campus_NA
        authentication_template:
          name: No Authentication
        pub_sub_enabled: true
        l3_virtual_networks:
          - SDA_VN_STAFF
          - SDA_VN_STUDENTS
          - INFRA_VN
        anycast_gateways:
          - ip_pool_name: STAFF_NA
            vlan_name: VLAN_STAFF
            vlan_id: 501
            traffic_type: DATA
            wireless_pool: true
            l3_virtual_network: SDA_VN_STAFF
          - ip_pool_name: STUDENTS_NA
            vlan_name: VLAN_STUDENTS
            vlan_id: 502
            traffic_type: DATA
            wireless_pool: true
            l3_virtual_network: SDA_VN_STUDENTS
          - ip_pool_name: ACCESS_POINT_NA
            vlan_name: VLAN_ACCESS_POINT
            vlan_id: 504
            traffic_type: DATA
            pool_type: FABRIC_AP
            l3_virtual_network: INFRA_VN

      - name: Global/Europe/Campus_EU
        authentication_template:
          name: No Authentication
        pub_sub_enabled: true
        l3_virtual_networks:
          - SDA_VN_STAFF
          - SDA_VN_STUDENTS
          - INFRA_VN
        anycast_gateways:
          - ip_pool_name: STAFF_EU
            vlan_name: VLAN_STAFF
            vlan_id: 501
            traffic_type: DATA
            wireless_pool: true
            l3_virtual_network: SDA_VN_STAFF
          - ip_pool_name: STUDENTS_EU
            vlan_name: VLAN_STUDENTS
            vlan_id: 502
            traffic_type: DATA
            wireless_pool: true
            l3_virtual_network: SDA_VN_STUDENTS
          - ip_pool_name: ACCESS_POINT_EU
            vlan_name: VLAN_ACCESS_POINT
            vlan_id: 504
            traffic_type: DATA
            pool_type: FABRIC_AP
            l3_virtual_network: INFRA_VN


```
Example-6: Fabric with advanced configurations for anycast gateway

```yaml
---
catalyst_center:
  fabric:
    fabric_sites:
      - name: Global/Canada
        authentication_template:
          name: Closed Authentication
        pub_sub_enabled: true
        l3_virtual_networks:
          - SDA_VN_USERS
          - SDA_VN_PRINTERS
          - SDA_VN_CORPORATE
          - SDA_VN_CRITICAL
          - INFRA_VN
        anycast_gateways:
          - ip_pool_name: USERS
            vlan_name: VLAN_USERS
            vlan_id: 301
            traffic_type: DATA
            wireless_pool: true
            tcp_mss_adjustment: 1400
            multiple_ip_to_mac_addresses: true
            l3_virtual_network: SDA_VN_USERS
          - ip_pool_name: PRINTERS
            vlan_name: VLAN_PRINTERS
            vlan_id: 302
            traffic_type: DATA
            layer2_flooding: true
            security_group_name: Contractors
            l3_virtual_network: SDA_VN_PRINTERS
          - ip_pool_name: CORPORATE
            vlan_name: VLAN_CORPORATE
            vlan_id: 303
            traffic_type: DATA
            layer2_flooding: true
            ip_directed_broadcast: true
            l3_virtual_network: SDA_VN_CORPORATE
          - ip_pool_name: AP_POOL
            vlan_name: VLAN_AP
            pool_type: FABRIC_AP
            vlan_id: 304
            traffic_type: DATA
            l3_virtual_network: INFRA_VN
          - ip_pool_name: FLEX_CONNECT_MERAKI
            vlan_name: VLAN_MERAKI
            vlan_id: 305
            traffic_type: DATA
            intra_subnet_routing_enabled: true
            l3_virtual_network: SDA_VN_CORPORATE
          - ip_pool_name: CRITICAL_POOL
            vlan_name: VLAN_CRITICAL
            vlan_id: 306
            traffic_type: DATA
            critical_pool: true
            l3_virtual_network: SDA_VN_CRITICAL

```
