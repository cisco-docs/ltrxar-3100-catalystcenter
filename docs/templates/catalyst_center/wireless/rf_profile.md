# RF Profile

*Location in GUI*:
`Design` » `Network Settings` » `Wireless` » `RF Profiles`

{{ doc_gen }}

RF Profiles define radio frequency settings for Access Points including channel selection, power levels, data rates, and coverage hole detection across 2.4 GHz, 5 GHz, and 6 GHz (Wi-Fi 6E) bands. RF Profiles are referenced by [Wireless Network Profiles](/docs/data_models/catalyst_center/network_profiles/wireless_network_profiles) via AP Zones and are applicable to both SDA fabric and non-fabric deployments.

### Examples

Example-1: Basic RF profile configuration with custom 5GHz radio settings for standard office environments, featuring optimized channel selection and power management:

```yaml
catalyst_center:
  wireless:
    rf_profiles:
      - name: BASIC_OFFICE_PROFILE
        enable_radio_type_a: true
        enable_radio_type_b: false
        enable_radio_type_c: false
        radio_type_a_properties:
          parent_profile: CUSTOM
          radio_channels: 36,40,44,48,149,153,157,161
          data_rates: 12,18,24,36,48,54
          mandatory_data_rates: 12,24
          power_threshold_v1: -65
          rx_sop_threshold: LOW
          min_power_level: 8
          max_power_level: 25
```

Example-2: Comprehensive dual-band RF profile with both 2.4GHz and 5GHz radio configurations optimized for enterprise environments with advanced power management and channel optimization:

```yaml
catalyst_center:
  wireless:
    rf_profiles:
      - name: ENTERPRISE_DUAL_BAND
        enable_radio_type_a: true
        enable_radio_type_b: true
        enable_radio_type_c: false
        radio_type_a_properties:
          parent_profile: LOW
          radio_channels: 36,40,44,48,52,56,60,64,144,149,153,157,161,165
          data_rates: 6,9,12,18,24,36,48,54
          mandatory_data_rates: 12,24
          power_threshold_v1: -70
          rx_sop_threshold: MEDIUM
          min_power_level: 5
          max_power_level: 30
        radio_type_b_properties:
          parent_profile: HIGH
          radio_channels: 1,6,11
          data_rates: 1,2,5.5,6,9,11,12,18,24,36,48,54
          mandatory_data_rates: 9
          power_threshold_v1: -75
          rx_sop_threshold: MEDIUM
          min_power_level: 7
          max_power_level: 30
```

Example-3: Advanced tri-band RF profile supporting Wi-Fi 6E with 6GHz radio configuration for cutting-edge wireless deployments, featuring comprehensive radio type coverage and optimized settings for maximizing performance:

```yaml
catalyst_center:
  wireless:
    rf_profiles:
      - name: WIFI6E_TRI_BAND_PROFILE
        default_rf_profile: false
        enable_radio_type_a: true
        enable_radio_type_b: true
        enable_radio_type_c: true
        radio_type_a_properties:
          parent_profile: HIGH
          radio_channels: 36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,144,149,153,157,161,165,169,173
          data_rates: 6,9,12,18,24,36,48,54
          mandatory_data_rates: 12,24
          power_threshold_v1: -67
          rx_sop_threshold: AUTO
          min_power_level: 3
          max_power_level: 30
        radio_type_b_properties:
          parent_profile: TYPICAL
          radio_channels: 1,6,11
          data_rates: 1,2,5.5,6,9,11,12,18,24,36,48,54
          mandatory_data_rates: 5.5,11
          power_threshold_v1: -70
          rx_sop_threshold: MEDIUM
          min_power_level: 3
          max_power_level: 20
        radio_type_c_properties:
          radio_channels: 1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,65,69,73,77,81,85,89,93
          data_rates: 6,9,12,18,24,36,48,54
          mandatory_data_rates: 24,36
          power_threshold_v1: -65
          rx_sop_threshold: HIGH
          min_power_level: 5
          max_power_level: 30
```