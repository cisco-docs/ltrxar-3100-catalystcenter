# IP Pool

*Location in GUI*:
`Design` » `Network Settings` » `IP Address Pools`

{{ doc_gen }}

IP Pools define global address pools and site-level reservations used for network services such as LAN automation, AP management, and endpoint addressing. Pools are created globally and then reserved at specific sites. In SDA fabric deployments, IP pools are also used by [Anycast Gateways](/docs/data_models/catalyst_center/fabric/anycast_gateway) for virtual network addressing. IP Pools are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic IPv4 IP pool configuration with Generic type, DHCP and DNS server assignments for centralized network services:

```yaml
catalyst_center:
  network_settings:
    ip_pools:
      - name: BASIC_IPv4_POOL
        ip_address_space: IPv4
        type: Generic
        dhcp_servers:
          - 192.168.1.10
          - 192.168.1.11
        dns_servers:
          - 8.8.8.8
          - 8.8.4.4
        gateway: 192.168.1.1
        ip_pool_cidr: 192.168.0.0/16
```

Example-2: Enterprise IPv4 deployment with multiple pool types and reservations for different network functions and services including LAN Automation, Access Point and Extended Nodes:

```yaml
catalyst_center:
  network_settings:
    ip_pools:
      - name: ENTERPRISE_CAMPUS_POOL
        ip_address_space: IPv4
        type: Generic
        dhcp_servers:
          - 10.100.1.10
          - 10.100.1.11
        dns_servers:
          - 10.100.1.5
          - 10.100.1.6
        ip_pool_cidr: 10.100.0.0/16
        ip_pools_reservations:
          - name: CAMPUS_LAN_AUTO
            prefix_length: 24
            subnet: 10.100.10.0
            type: LAN
          - name: CAMPUS_AP_POOL
            prefix_length: 26
            subnet: 10.100.20.0
            type: management
          - name: CAMPUS_EXTENDED_NODE_POOL
            prefix_length: 26
            subnet: 10.100.20.0
            type: management
```

Example-3: Enterprise dual-stack IPv4/IPv6 deployment showcasing comprehensive network infrastructure with multiple pool types (generic, LAN, WAN, management, service) and centralized DHCP/DNS services. This configuration demonstrates advanced network automation capabilities including LAN Automation pools, dedicated management networks, service-specific pools, and full IPv6 support for modern enterprise architectures. Note that in dual-stack deployments, IPv6 pool reservations must use matching names with their corresponding IPv4 pool reservations to ensure proper network service integration and consistent addressing across both protocol stacks:

```yaml
catalyst_center:
  network_settings:
    ip_pools:
      - name: GLOBAL_IPv4_MAIN_POOL
        ip_address_space: IPv4
        type: Generic
        dhcp_servers:
          - 172.16.1.10
          - 172.16.1.11
        dns_servers:
          - 172.16.1.5
          - 172.16.1.6
        ip_pool_cidr: 172.16.0.0/16
        ip_pools_reservations:
          - name: CORPORATE_POOL
            prefix_length: 24
            subnet: 172.16.10.0
            gateway: 172.16.10.1
            type: Generic
            dhcp_servers:
              - 172.16.1.10
              - 172.16.1.11
            dns_servers:
              - 172.16.1.5
              - 172.16.1.6
          - name: BRANCH_WAN_POOL
            prefix_length: 24
            subnet: 172.16.20.0
            gateway: 172.16.20.1
            type: WAN
            dhcp_servers:
              - 172.16.1.10
              - 172.16.1.11
            dns_servers:
              - 172.16.1.5
              - 172.16.1.6
          - name: MGMT_NETWORK_POOL
            prefix_length: 26
            subnet: 172.16.30.0
            gateway: 172.16.30.1
            type: management
            dhcp_servers:
              - 172.16.1.10
              - 172.16.1.11
            dns_servers:
              - 172.16.1.5
              - 172.16.1.6
          - name: SERVICE_NETWORK_POOL
            prefix_length: 25
            subnet: 172.16.40.0
            gateway: 172.16.40.1
            type: service
            dhcp_servers:
              - 172.16.1.10
            dns_servers:
              - 172.16.1.5
          - name: LAN_AUTOMATION_POOL
            prefix_length: 24
            subnet: 172.16.250.0
            type: LAN
      - name: GLOBAL_IPv6_POOL
        ip_address_space: IPv6
        type: Generic
        dhcp_servers:
          - "2001:db8::10"
          - "2001:db8::11"
        dns_servers:
          - "2001:db8::5"
          - "2001:db8::6"
          - "2001:4860:4860::8888"
        ip_pool_cidr: 2001:db8::/64
        ip_pools_reservations:
          - name: CORPORATE_POOL
            prefix_length: 80
            subnet: "2001:db8:0000:0000:1001::"
            gateway: "2001:db8:0000:0000:1001::1"
            type: Generic
            dhcp_servers:
              - "2001:db8::10"
              - "2001:db8::11"
            dns_servers:
              - "2001:db8::5"
              - "2001:db8::6"
          - name: MGMT_NETWORK_POOL
            prefix_length: 80
            subnet: "2001:db8:0000:0000:1002::"
            gateway: "2001:db8:0000:0000:1002::1"
            type: management
            dhcp_servers:
              - "2001:db8::10"
              - "2001:db8::11"
            dns_servers:
              - "2001:db8::5"
              - "2001:db8::6"
              - "2001:4860:4860::8888"
```

Example-4: Site assignment configuration demonstrating how to apply IP pool reservations to different site types and geographic locations for campus automation, access points, and various network services:

```yaml
catalyst_center:
  sites:
    areas:
      - name: Main Campus
        parent_name: Global/Americas
        ip_pools_reservations:
          - CORPORATE_POOL
          - MGMT_NETWORK_POOL
          - CAMPUS_EXTENDED_NODE_POOL
          - CAMPUS_AP_POOL
          - CAMPUS_LAN_AUTO
      - name: Branch Offices
        parent_name: Global/Americas
        ip_pools_reservations:
          - BRANCH_WAN_POOL
          - SERVICE_NETWORK_POOL
```