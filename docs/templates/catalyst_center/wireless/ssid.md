# SSID

*Location in GUI*:
`Design` » `Network Settings` » `Wireless` » `SSIDs`

{{ doc_gen }}

SSIDs define the wireless network identity and security settings that clients connect to. Each SSID is created at the Global level and can then be attached to one or more [Wireless Network Profiles](/docs/data_models/catalyst_center/network_profiles/wireless_network_profiles) for site-level deployment. SSIDs are applicable to both SDA fabric and non-fabric (traditional/FlexConnect) deployments.

### Examples

Example-1: Basic WPA3 Personal SSID configuration with triple-band support, featuring modern security settings including SAE authentication, protected management frames, and optimized client management for enterprise environments:

```yaml
catalyst_center:
  wireless:
    ssids:
      - name: SSID_1
        auth_type: WPA3_PERSONAL
        passphrase: Cisco123
        fast_lane: false
        mac_filtering: false
        ssid_radio_type: Triple Band
        broadcast_ssid: true
        fast_transition: ADAPTIVE
        session_timeout_enable: true
        session_timeout: 1800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        directed_multicast_service: true
        neighbor_list: true
        mft_client_protection: OPTIONAL
        aaa_override: false
        protected_management_frame: REQUIRED
        rsn_cipher_suite_ccmp128: true
        wlan_type: Enterprise
        auth_key_sae_ext: true
        ghz24_policy: dot11-g-only
        hex: false
        random_mac_filter: false
```

Example-2: Comprehensive enterprise SSID deployment with multiple authentication types and advanced wireless features, demonstrating WPA2/WPA3 enterprise authentication, QoS settings, and detailed client management across different deployment scenarios:

```yaml
catalyst_center:
  wireless:
    ssids:
      - name: 802_1X_SSID
        wlan_type: Enterprise
        ssid_radio_type: "2.4GHz and 6GHz"
        ghz24_policy: dot11-bg-only
        fast_lane: false
        egress_qos: PLATINUM
        ingress_qos: PLATINUM-UP
        enabled: true
        broadcast_ssid: true
        auth_type: WPA2_WPA3_ENTERPRISE
        ap_beacon_protection: true
        fast_transition: ADAPTIVE
        rsn_cipher_suite_ccmp128: true
        auth_key8021x: true
        auth_key8021x_sha256: true
        auth_servers: ["198.18.133.27"]
        acct_servers: ["198.18.133.27"]
        aaa_override: true
        mac_filtering: true
        random_mac_filter: false
        posturing: false
        mft_client_protection: OPTIONAL
        protected_management_frame: REQUIRED
        neighbor_list: true
        coverage_hole_detection: true
        session_timeout_enable: true
        session_timeout: 28800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        sleeping_client_timeout: 500
        directed_multicast_service: true
        nas_options: ["System IP Address"]
        client_rate_limit: 1000000

      - name: Guest_SSID
        wlan_type: Guest
        ssid_radio_type: "Triple Band"
        ghz24_policy: dot11-bg-only
        fast_lane: false
        egress_qos: PLATINUM
        ingress_qos: PLATINUM-UP
        enabled: true
        broadcast_ssid: true
        auth_type: OPEN
        fast_transition: ADAPTIVE
        l3_auth_type: web_auth
        auth_server: auth_ise
        auth_servers: ["198.18.133.27"]
        acct_servers: ["198.18.133.27"]
        aaa_override: true
        mac_filtering: true
        random_mac_filter: false
        posturing: false
        mft_client_protection: OPTIONAL
        protected_management_frame: REQUIRED
        neighbor_list: true
        coverage_hole_detection: true
        session_timeout_enable: true
        session_timeout: 28800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        sleeping_client_timeout: 500
        directed_multicast_service: true
        nas_options: ["System IP Address"]
        client_rate_limit: 1000000

      - name: Guest_EXT_WEB_AUTH
        wlan_type: Guest
        ssid_radio_type: "2.4GHz and 6GHz"
        ghz24_policy: dot11-bg-only
        fast_lane: false
        egress_qos: PLATINUM
        ingress_qos: PLATINUM-UP
        enabled: true
        broadcast_ssid: true
        auth_type: OPEN
        fast_transition: ADAPTIVE
        l3_auth_type: web_auth
        auth_server: auth_external
        external_auth_ip_address: "https://198.18.133.27/dummy.html"
        aaa_override: true
        mac_filtering: true
        random_mac_filter: false
        posturing: false
        mft_client_protection: OPTIONAL
        protected_management_frame: REQUIRED
        neighbor_list: true
        coverage_hole_detection: true
        session_timeout_enable: true
        session_timeout: 28800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        sleeping_client_timeout: 500
        directed_multicast_service: true
        nas_options: ["System IP Address"]
        client_rate_limit: 10000
        
      - name: PSK_SSID
        wlan_type: Enterprise
        ssid_radio_type: "2.4GHz and 5GHz"
        ghz24_policy: dot11-bg-only
        fast_lane: false
        egress_qos: PLATINUM
        ingress_qos: PLATINUM-UP
        enabled: true
        broadcast_ssid: true
        auth_type: WPA2_PERSONAL
        ap_beacon_protection: false
        passphrase: PSKPass123
        fast_transition: ENABLE
        rsn_cipher_suite_ccmp128: true
        auth_key_psk: true
        auth_key_psk_plus_ft: true
        mft_client_protection: OPTIONAL
        protected_management_frame: OPTIONAL
        neighbor_list: true
        coverage_hole_detection: true
        session_timeout_enable: true
        session_timeout: 28800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        sleeping_client_timeout: 500
        directed_multicast_service: true
        nas_options: ["System IP Address"]
        client_rate_limit: 10000

      - name: PSK_SSID_ENTERPRISE
        wlan_type: Enterprise
        ssid_radio_type: "5GHz"
        ghz24_policy: dot11-bg-only
        fast_lane: false
        egress_qos: PLATINUM
        ingress_qos: PLATINUM-UP
        enabled: true
        broadcast_ssid: true
        auth_type: WPA2_WPA3_ENTERPRISE
        ap_beacon_protection: true
        fast_transition: ENABLE
        rsn_cipher_suite_ccmp128: true
        rsn_cipher_suite_gcmp256: true
        cckm: true
        cckm_tsf_tolerance: 5000
        auth_key8021x: true
        auth_key8021x_sha256: true
        auth_key_suite_b1921x: true
        auth_servers: ["198.18.133.27"]
        acct_servers: ["198.18.133.27"]
        aaa_override: true
        mac_filtering: true
        posturing: false
        mft_client_protection: OPTIONAL
        protected_management_frame: REQUIRED
        neighbor_list: true
        coverage_hole_detection: true
        session_timeout_enable: true
        session_timeout: 28800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        sleeping_client_timeout: 500
        directed_multicast_service: true
        nas_options: ["System IP Address"]
        client_rate_limit: 10000

      - name: IPSK_SSID
        wlan_type: Enterprise
        ssid_radio_type: "2.4GHz and 6GHz"
        ghz24_policy: dot11-bg-only
        fast_lane: false
        egress_qos: PLATINUM
        ingress_qos: PLATINUM-UP
        enabled: true
        broadcast_ssid: true
        auth_type: WPA2_WPA3_PERSONAL
        ap_beacon_protection: true
        passphrase: PSKPass123
        fast_transition: ENABLE
        rsn_cipher_suite_ccmp128: true
        rsn_cipher_suite_gcmp256: true
        auth_key_sae: true
        auth_key_sae_ext_plus_ft: true
        auth_key_psk: true
        auth_key_psk_plus_ft: true
        auth_servers: ["198.18.133.27"]
        acct_servers: ["198.18.133.27"]
        aaa_override: true
        posturing: false
        mft_client_protection: OPTIONAL
        protected_management_frame: REQUIRED
        neighbor_list: true
        coverage_hole_detection: true
        session_timeout_enable: true
        session_timeout: 28800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        sleeping_client_timeout: 500
        directed_multicast_service: true
        nas_options: ["System IP Address"]
        client_rate_limit: 10000
```

Example-3: Advanced fabric-enabled SSID configuration with WPA2/WPA3 Personal authentication, demonstrating comprehensive security features including multiple cipher suites, fast transition capabilities, and enhanced authentication methods for Software-Defined Access (SDA) fabric deployments:

```yaml
catalyst_center:
  wireless:
    ssids:
      - name: 802_1X_SSID_FABRIC
        wlan_type: Enterprise
        ssid_radio_type: "Triple Band"
        ghz24_policy: dot11-bg-only
        fast_lane: false
        egress_qos: PLATINUM
        ingress_qos: PLATINUM-UP
        enabled: true
        broadcast_ssid: true
        auth_type: WPA2_WPA3_PERSONAL
        ap_beacon_protection: true
        passphrase: PSKPass123
        fast_transition: ENABLE
        rsn_cipher_suite_ccmp128: true
        rsn_cipher_suite_gcmp256: true
        auth_key_sae: true
        auth_key_sae_ext_plus_ft: true
        auth_key_psk: true
        auth_key_psk_plus_ft: true
        auth_servers: ["198.18.133.27"]
        acct_servers: ["198.18.133.27"]
        aaa_override: true
        posturing: false
        mft_client_protection: OPTIONAL
        protected_management_frame: REQUIRED
        neighbor_list: true
        coverage_hole_detection: true
        session_timeout_enable: true
        session_timeout: 28800
        client_exclusion: true
        client_exclusion_timeout: 1800
        basic_service_set_max_idle: true
        basic_service_set_client_idle_timeout: 300
        sleeping_client_timeout: 500
        directed_multicast_service: true
        nas_options: ["System IP Address"]
        client_rate_limit: 10000
```