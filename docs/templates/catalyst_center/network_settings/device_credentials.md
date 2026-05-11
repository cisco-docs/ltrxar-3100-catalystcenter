# Device Credentials

*Location in GUI*:
`Design` » `Network Settings` » `Device Credentials`

{{ doc_gen }}

Device Credentials define the authentication credentials used by Catalyst Center to communicate with network devices. This includes CLI (SSH/Telnet), SNMPv2 Read/Write, SNMPv3, HTTPS Read/Write, and NETCONF credentials. Credentials are created globally and then assigned to sites ([Areas](/docs/data_models/catalyst_center/sites/area), [Buildings](/docs/data_models/catalyst_center/sites/building), [Floors](/docs/data_models/catalyst_center/sites/floor)) for inheritance. They are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic device credentials configuration with CLI access using standard Cisco credentials and enable password for network device management:

```yaml
catalyst_center:
  network_settings:
    device_credentials:
      cli_credentials:
        - name: BASIC_CLI_ADMIN
          username: admin
          password: CiscoAdmin123!
          enable: CiscoEnable123!
```

Example-2: SNMP monitoring setup with both read and write community strings for network device monitoring and configuration management across European sites:

```yaml
catalyst_center:
  network_settings:
    device_credentials:
      cli_credentials:
        - name: EUROPE_CLI_ADMIN
          username: netadmin
          password: EuropeAdmin456!
          enable: EuropeEnable456!
      snmpv2_read_credentials:
        - name: EUROPE_SNMP_READ
          read_community: EuropeReadComm789
      snmpv2_write_credentials:
        - name: EUROPE_SNMP_WRITE
          write_community: EuropeWriteComm789
```

Example-3: Comprehensive device credentials deployment with all supported authentication methods including CLI, SNMPv2, SNMPv3 with multiple security modes, and HTTPS credentials for REST API access across global enterprise infrastructure:

```yaml
catalyst_center:
  network_settings:
    device_credentials:
      cli_credentials:
        - name: GLOBAL_CLI_ADMIN
          username: globaladmin
          password: GlobalAdmin2024!
          enable: GlobalEnable2024!
        - name: BRANCH_CLI_READONLY
          username: branchread
          password: BranchRead2024!
      snmpv2_read_credentials:
        - name: GLOBAL_SNMP_READ
          read_community: GlobalMonitorRead
        - name: BRANCH_SNMP_READ
          read_community: BranchMonitorRead
      snmpv2_write_credentials:
        - name: GLOBAL_SNMP_WRITE
          write_community: GlobalConfigWrite
      snmpv3_credentials:
        - name: SECURE_SNMPV3_AUTHPRIV
          auth_type: SHA
          privacy_type: AES256
          snmp_mode: AUTHPRIV
          username: secureuser
          auth_password: SecureAuth2024!
          privacy_password: SecurePriv2024!
        - name: STANDARD_SNMPV3_AUTHNOPRIV
          auth_type: MD5
          privacy_type: AES128
          snmp_mode: AUTHNOPRIV
          username: standarduser
          auth_password: StandardAuth2024!
          privacy_password: StandardPriv2024!
        - name: BASIC_SNMPV3_NOAUTH
          snmp_mode: NOAUTHNOPRIV
          username: basicuser
          auth_password: BasicAuth2024!
          privacy_password: BasicPriv2024!
      https_read_credentials:
        - name: API_READ_ACCESS
          username: apiread
          password: ApiRead2024!
          port: 443
        - name: MONITORING_API_ACCESS
          username: monitor
          password: Monitor2024!
          port: 8443
      https_write_credentials:
        - name: API_WRITE_ACCESS
          username: apiwrite
          password: ApiWrite2024!
          port: 443
        - name: CONFIG_API_ACCESS
          username: configapi
          password: ConfigApi2024!
          port: 9443
```

Example-4: Site assignment configuration demonstrating how to apply different credential sets to various site types and geographic locations:

```yaml
catalyst_center:
  sites:
    areas:
      - name: Corporate Headquarters
        parent_name: Global/Americas/USA/California
        cli_credentials: GLOBAL_CLI_ADMIN
        snmpv3_credentials: SECURE_SNMPV3_AUTHPRIV
        https_read_credentials: API_READ_ACCESS
        https_write_credentials: API_WRITE_ACCESS
      - name: European Operations
        parent_name: Global/Europe/Germany
        cli_credentials: EUROPE_CLI_ADMIN
        snmpv2_read_credentials: EUROPE_SNMP_READ
        snmpv2_write_credentials: EUROPE_SNMP_WRITE
        https_read_credentials: MONITORING_API_ACCESS
    buildings:
      - name: Branch Office
        parent_name: Global/Americas/USA/Texas/Austin
        address: 110 Inner Campus Dr., Austin, TX 78712, USA
        cli_credentials: BRANCH_CLI_READONLY
        snmpv2_read_credentials: BRANCH_SNMP_READ
        snmpv3_credentials: STANDARD_SNMPV3_AUTHNOPRIV
      - name: Regional Center
        parent_name: Global/Americas/USA/Texas/College Station
        address: 400 Bizzell St, College Station, TX 77840, USA
        cli_credentials: GLOBAL_CLI_ADMIN
        snmpv3_credentials: SECURE_SNMPV3_AUTHPRIV
        https_read_credentials: API_READ_ACCESS
        https_write_credentials: CONFIG_API_ACCESS
```