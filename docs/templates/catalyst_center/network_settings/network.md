# Network

*Location in GUI*:
`Design` » `Network Settings` » `Servers`

{{ doc_gen }}

Network settings define core infrastructure services applied to sites, including DNS servers, DHCP servers, NTP servers, domain names, timezone, syslog, and SNMP trap destinations. These settings are inherited down the site hierarchy and are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic network settings configuration with essential services including timezone, DNS, DHCP, domain name, and NTP servers for centralized network infrastructure:

```yaml
catalyst_center:
  network_settings:
    network:
      - name: BASIC_NETWORK_SETTINGS
        timezone: America/New_York
        dhcp_servers:
          - 192.168.1.10
          - 192.168.1.11
        dns_servers:
          - 8.8.8.8
          - 8.8.4.4
        domain_name: company.local
        ntp_servers:
          - 192.168.1.5
          - 192.168.1.6
```

Example-2: Enterprise network settings with comprehensive service configuration including custom banner message, multiple redundant servers, and European timezone settings for corporate infrastructure:

```yaml
catalyst_center:
  network_settings:
    network:
      - name: ENTERPRISE_NETWORK_CONFIG
        timezone: Europe/London
        dhcp_servers:
          - 10.100.1.10
          - 10.100.1.11
        dns_servers:
          - 10.100.1.5
          - 10.100.1.6
        domain_name: enterprise.corp
        banner: "Authorized Access Only - Corporate Network"
        ntp_servers:
          - 10.100.1.15
          - 10.100.1.16
```

Example-3: Global network settings deployment with multiple regional configurations supporting different time-zones, localized services, and region-specific infrastructure for worldwide enterprise operations:

```yaml
catalyst_center:
  network_settings:
    network:
      - name: AMERICAS_NETWORK_SETTINGS
        timezone: America/Chicago
        dhcp_servers:
          - 172.16.10.100
          - 172.16.10.110
        dns_servers:
          - 172.16.10.5
          - 172.16.10.6
        domain_name: americas.global.corp
        banner: "Americas Region - Authorized Personnel Only"
        ntp_servers:
          - 172.16.10.115
          - 172.16.10.116
      - name: EMEA_NETWORK_SETTINGS
        timezone: Europe/Amsterdam
        dhcp_servers:
          - 172.17.10.200
          - 172.17.10.210
        dns_servers:
          - 172.17.10.5
          - 172.17.10.6
        domain_name: emea.global.corp
        banner: "EMEA Region - Secure Access Required"
        ntp_servers:
          - 172.17.10.15
          - 172.17.10.16
      - name: APAC_NETWORK_SETTINGS
        timezone: Asia/Singapore
        dhcp_servers:
          - 172.18.10.10
          - 172.18.10.11
        dns_servers:
          - 172.18.10.5
          - 172.18.10.6
        domain_name: apac.global.corp
        banner: "APAC Region - Network Access Monitored"
        ntp_servers:
          - 172.18.10.125
          - 172.18.10.126
```

Example-4: Site assignment configuration demonstrating how to apply network settings to different geographic regions and organizational units:

```yaml
catalyst_center:
  sites:
    areas:
      - name: USA
        parent_name: Global/Americas
        network_settings:
          network: AMERICAS_NETWORK_SETTINGS
      - name: Netherlands
        parent_name: Global/EMEA
        network_settings:
          network: EMEA_NETWORK_SETTINGS
      - name: Singapore
        parent_name: Global/APAC
        network_settings:
          network: APAC_NETWORK_SETTINGS
    buildings:
      - name: Corporate Headquarters
        parent_name: Global/EMEA/UK/London
        network_settings:
          network: ENTERPRISE_NETWORK_CONFIG
      - name: Branch Office
        parent_name: Global/Americas/USA/New York
        network_settings:
          network: BASIC_NETWORK_SETTINGS
```