# Wireless Network Profiles

*Location in GUI*:
`Design` » `Network Profiles`

{{ doc_gen }}

Wireless Network Profiles bind [SSIDs](/docs/data_models/catalyst_center/wireless/ssid) to sites and define how wireless networks are deployed. Each profile contains `ssid_details` with fabric/FlexConnect mode, VLAN mappings, [802.11be Profiles](/docs/data_models/catalyst_center/wireless/dot11be_profile), and [Anchor Groups](/docs/data_models/catalyst_center/wireless/anchor_group). Profiles can also include `ap_zones` for [RF Profile](/docs/data_models/catalyst_center/wireless/rf_profile) assignment, `site_tags` for [AP Profile](/docs/data_models/catalyst_center/wireless/ap_profile) linking,  and `policy_tags` for controlling which **AP Zones** are active at specific sites. Some features applicable only on non-fabric deployments.

> **Note**: `interface_name` and `vlan_group_name` are mutually exclusive — only one can be set per SSID. Neither is applicable when `enable_fabric` is `true`.


### Examples


Example-1: Wireless Network Profile `WIRELESS_PROFILE` with fabric enabled `SSID_1` attached and multiple sites assigned

```yaml
catalyst_center:
  network_profiles:
    wireless:
      - name: WIRELESS_PROFILE
        ssid_details:
          - name: SSID_1
            enable_fabric: true
            enable_flex_connect: false
        sites:
          - Global/United States/Golden Hills Campus/Sunset Tower
          - Global/United States/Lakefront Tower/Windy City Plaza
          - Global/United States/Oceanfront Mansion/Art Deco Mansion
          - Global/United States/Desert Oasis Branch/Desert Oasis Tower
```

Example-2: Wireless Network Profile `W_Cat9800-CL` with fabric enabled `802_1X_SSID` attached, one site assigned, additional interface `Gi1/0/2`, and AP zone `AP_ZONE` with RF profile `BASIC_PROFILE_1`

```yaml
catalyst_center:
  network_profiles:
    wireless:
      - name: W_Cat9800-CL
        sites:
          - Global/Poland/Warsaw/Bld_B
        ssid_details:
          - name: 802_1X_SSID
            enable_fabric: true
        additional_interfaces:
          - Gi1/0/2
        ap_zones:
          - name: AP_ZONE
            rf_profile_name: BASIC_PROFILE_1
            ssids:
              - 802_1X_SSID
```

Example-3: Wireless Network Profile with Wi-Fi 7 (802.11be) profile assignment and Site Tags linking AP profiles to specific sites. The `dot11be_profile_name` links an SSID to a pre-configured 802.11be profile for enhanced performance features like OFDMA and MU-MIMO (requires IOS-XE 17.15+)

```yaml
catalyst_center:
  network_profiles:
    wireless:
      - name: WIFI7_ENTERPRISE_PROFILE
        sites:
          - Global/HQ/Building_A
          - Global/HQ/Building_B
        ssid_details:
          - name: WIFI7_CORPORATE_SSID
            enable_fabric: true
            dot11be_profile_name: WIFI7_HIGH_PERFORMANCE
          - name: WIFI7_GUEST_SSID
            enable_fabric: false
            enable_flex_connect: true
            local_to_vlan: 100
            dot11be_profile_name: WIFI7_STANDARD
        ap_zones:
          - name: HIGH_DENSITY_ZONE
            rf_profile_name: WIFI6E_TRI_BAND_PROFILE
            ssids:
              - WIFI7_CORPORATE_SSID
        site_tags:
          - name: WIFI7_HQ_TAG
            ap_profile_name: WIFI7_AP_PROFILE
            sites:
              - Global/HQ/Building_A
              - Global/HQ/Building_B
```

Example-4: Wireless Network Profile with Guest SSID tunneled to an Anchor Group. The `anchor_group_name` references a pre-configured Anchor Group for guest traffic tunneling to anchor WLCs. When `anchor_group_name` is set, FlexConnect settings are not applicable

```yaml
catalyst_center:
  network_profiles:
    wireless:
      - name: GUEST_ANCHOR_PROFILE
        sites:
          - Global/HQ/Building_A
        ssid_details:
          - name: GUEST_SSID
            enable_fabric: false
            anchor_group_name: AG_Guest
            interface_name: guest_vlan
```
**Note**: `interface_name` and `vlan_group_name` are mutually exclusive — only one can be set per SSID. Neither is applicable when `enable_fabric` is `true`.

Example-5: Wireless Network Profile with VLAN Group for client VLAN load-balancing. The `vlan_group_name` references a pre-configured VLAN Group on the WLC to distribute wireless clients across multiple VLANs in a round-robin fashion. Mutually exclusive with `interface_name` and not applicable when fabric is enabled.

```yaml
catalyst_center:
  network_profiles:
    wireless:
      - name: VLAN_LB_PROFILE
        sites:
          - Global/HQ/Building_A
        ssid_details:
          - name: CORPORATE_SSID
            enable_fabric: false
            vlan_group_name: CORP_VLAN_GROUP
```

Example-6: Wireless Network Profile with AP Zones and Policy Tags. Policy Tags control which AP Zones are active at specific sites. AP Zones must be defined on the Wireless Profile first, then Policy Tags reference them by name. Only relevant when AP Zones are configured.

```yaml
catalyst_center:
  network_profiles:
    wireless:
      - name: ZONED_PROFILE
        sites:
          - Global/HQ/Building_A
          - Global/HQ/Building_B
        ssid_details:
          - name: CORPORATE_SSID
            enable_fabric: false
          - name: IOT_SSID
            enable_fabric: false
        ap_zones:
          - name: INDOOR_ZONE
            rf_profile_name: HIGH_DENSITY_RF
            ssids:
              - CORPORATE_SSID
              - IOT_SSID
          - name: OUTDOOR_ZONE
            rf_profile_name: OUTDOOR_RF
            ssids:
              - CORPORATE_SSID
        policy_tags:
          - name: BUILDING_A_POLICY
            ap_zones:
              - INDOOR_ZONE
              - OUTDOOR_ZONE
            sites:
              - Global/HQ/Building_A
          - name: BUILDING_B_POLICY
            ap_zones:
              - INDOOR_ZONE
            sites:
              - Global/HQ/Building_B
```

Example-7: Two distinct wireless network profiles demonstrating fabric vs non-fabric deployments: `ENTERPRISE_FABRIC` for SDA-enabled sites with fabric SSIDs, Wi-Fi profiles, and high-density zones, and `ENTERPRISE_NON_FABRIC` for traditional branch deployments with FlexConnect SSIDs, VLAN mappings, and standard RF configurations

```yaml
catalyst_center:
  network_profiles:
    wireless:
      - name: ENTERPRISE_FABRIC
        sites:
          - Global/HQ
          - Global/Campus
        ssid_details:
          - name: CORPORATE_FABRIC_SSID
            enable_fabric: true
            enable_flex_connect: false
            wlan_profile_name: CORPORATE_FABRIC_SSID_profile
          - name: IOT_FABRIC_SSID
            enable_fabric: true
            enable_flex_connect: false
        additional_interfaces:
          - dc_interface
          - security_vlan404
        ap_zones:
          - name: CORPORATE_ZONE_HIGH_DENSITY
            rf_profile_name: HIGH_DENSITY_RF_PROFILE
            ssids:
              - CORPORATE_FABRIC_SSID
          - name: IOT_ZONE_LOW_POWER
            rf_profile_name: LOWEST_RF_PROFILE
            ssids:
              - IOT_FABRIC_SSID
      - name: ENTERPRISE_NON_FABRIC
        sites:
          - Global/Branches
        ssid_details:
          - name: GUEST_FLEXCONNECT_SSID
            enable_fabric: false
            enable_flex_connect: true
            local_to_vlan: 200
            interface_name: guest_interface
          - name: BYOD_HYBRID_SSID
            enable_fabric: false
            enable_flex_connect: false
            interface_name: byod_interface
        ap_zones:
          - name: CORPORATE_ZONE_HIGH_DENSITY
            rf_profile_name: HIGH_DENSITY_RF_PROFILE
            ssids:
              - BYOD_HYBRID_SSID
          - name: GUEST_ZONE_STANDARD
            rf_profile_name: STANDARD_RF_PROFILE
            ssids:
              - GUEST_FLEXCONNECT_SSID
        additional_interfaces:
          - branch_interface
          - vlan_202
```
