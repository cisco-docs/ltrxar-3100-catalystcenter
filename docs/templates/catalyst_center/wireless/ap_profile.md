# AP Profile

*Location in GUI*:
`Design` » `Network Settings` » `Wireless` » `AP Profiles`

{{ doc_gen }}

AP Profiles define device-level settings for Access Points including management access (802.1X, SSH, Telnet, CDP), security features (AWIPS, rogue detection), mesh networking, power management, and client limits. They are linked to [Wireless Network Profiles](/docs/data_models/catalyst_center/network_profiles/wireless_network_profiles) via Site Tags and are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: AP profile with AWIPS threat detection and rogue detection enabled for secure environments:

```yaml
catalyst_center:
  wireless:
    ap_profiles:
      - name: SECURE_AP_PROFILE
        description: Secure AP profile with threat detection
        awips_enabled: true
        awips_forensic_enabled: true
        rogue_detection: true
        rogue_detection_min_rssi: -90
        rogue_detection_transient_interval: 300
        rogue_detection_report_interval: 60
        pmf_denial_enabled: true
```

Example-2: AP profile with mesh networking and calendar-based power scheduling for outdoor deployments:

```yaml
catalyst_center:
  wireless:
    ap_profiles:
      - name: MESH_OUTDOOR_PROFILE
        description: Outdoor mesh AP profile with power scheduling
        mesh_enabled: true
        bridge_group_name: OUTDOOR
        backhaul_client_access: true
        range: 5000
        ghz5_backhaul_data_rates: 802.11ac
        rap_downlink_backhaul: "5 GHz"
        power_profile: LOW_POWER
        calendar_power_profiles:
          - power_profile: NIGHT_POWER_SAVE
            scheduler_type: DAILY
            scheduler_start_time: "22:00"
            scheduler_end_time: "06:00"
        country_code: US
        time_zone: Controller   
```

> **Note**: AP Profiles define device-level settings for Access Points. They are linked to Wireless Network Profiles via Site Tags (`catalystcenter_wireless_profile_site_tag`), not directly to the Wireless Profile resource. Use `power_profile` for the always-on AP power profile name and `power_profile` on each `calendar_power_profiles` row for the scheduled profile (names must match profiles under `catalyst_center.wireless.power_profiles`). The Terraform provider maps these to its API attributes internally.

Example-3: AP profile with 802.1X authentication linked to a Wireless Network Profile via a Site Tag:

```yaml
catalyst_center:
  wireless:
    ap_profiles:
      - name: DOT1X_AP_PROFILE
        description: AP profile with 802.1X authentication
        auth_type: EAP-TLS
        ssh_enabled: true
        management_user_name: admin
        management_password: AdminPass123
        management_enable_password: EnablePass123
        cdp_state: true
        client_limit: 500
        time_zone: Controller
  network_profiles:
    wireless:
      - name: ENTERPRISE_WIRELESS
        ssid_details:
          - name: CORPORATE_SSID
            enable_fabric: true
        sites:
          - Global/HQ/Building_A
          - Global/HQ/Building_B
        site_tags:
          - name: HQ_SECURE_TAG
            ap_profile_name: DOT1X_AP_PROFILE
            sites:
              - Global/HQ/Building_A
              - Global/HQ/Building_B
```

Example-4: Comprehensive AP profile with mesh networking, 802.1X authentication, rogue detection, calendar-based monthly power scheduling, and timezone offset:

```yaml
catalyst_center:
  wireless:
    ap_profiles:
      - name: COMPREHENSIVE_AP_PROFILE
        description: "AP configuration"
        remote_worker_enabled: false
        auth_type: EAP-FAST
        dot1x_username: "apuser"
        dot1x_password: "secret123"
        ssh_enabled: true
        telnet_enabled: false
        management_user_name: "admin"
        management_password: "secret123"
        management_enable_password: "enable123"
        cdp_state: false
        awips_enabled: false
        awips_forensic_enabled: false
        rogue_detection: true
        rogue_detection_min_rssi: -90
        rogue_detection_transient_interval: 0
        rogue_detection_report_interval: 10
        pmf_denial_enabled: false
        mesh_enabled: true
        bridge_group_name: "Default"
        backhaul_client_access: true
        range: 12000
        ghz5_backhaul_data_rates: 802.11ax
        ghz24_backhaul_data_rates: 802.11n
        rap_downlink_backhaul: "2.4 GHz"
        calendar_power_profiles:
          - power_profile: "moderate_power_profile"
            scheduler_type: MONTHLY
            scheduler_start_time: "18:00"
            scheduler_end_time: "08:00"
            scheduler_date:
              - "1"
              - "2"
              - "3"
              - "4"
              - "5"
              - "6"
              - "7"
              - "8"
              - "9"
              - "10"
              - "11"
              - "12"
              - "13"
              - "14"
        country_code: IN
        time_zone: Delta from Controller
        time_zone_offset_hour: 5
        time_zone_offset_minutes: 30
        client_limit: 200
```
